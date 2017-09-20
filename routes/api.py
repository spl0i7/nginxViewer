from utils import utils
from utils.utils import LoginChecker
from motor import MotorClient
from tornado import gen
import tornado.ioloop
import tornado.web
import json
import re
import bcrypt


connection = MotorClient()
db = connection.nginxLogger


class RestHandler:

    class Summary(LoginChecker):
        @gen.coroutine
        def get(self):
            stats = {}

            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            # find the total number of records since a timestamp
            total_req = yield db.access_logs.count(
                {'timestamp': {'$gt': since}}
            )

            # find response code starting with 1xx , 2xx or 3xx
            valid_req = yield db.access_logs.count(
                {'response_code': re.compile(r'^[123]'), 'timestamp': {'$gt': since}}
            )
            # find response code starting with 4xx or 5xx
            invalid_req = yield db.access_logs.count(
                {'response_code': re.compile(r'^[45]'), 'timestamp': {'$gt': since}}
            )

            # find out 404 page not found errors
            total_404 = yield db.access_logs.count(
                {'timestamp': {'$gt': since}, 'response_code': '404'}
            )
            # count number of unique ip address
            unique_visitor = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': '$remote_ip.ip'}},
                {'$group': {'_id': None, 'count': {'$sum': 1}}}
            ])

            # find out total bytes sent by the server
            total_bandwidth = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': None, 'count': {'$sum': '$size'}}}
            ])

            # these are simply an int
            stats['total_requests'] = total_req
            stats['valid_req'] = valid_req
            stats['invalid_req'] = invalid_req
            stats['total_404'] = total_404

            # extract count from the results of query
            stats['unique_visitor'] = yield utils.get_aggregration_count(unique_visitor, 'count')
            stats['total_bandwidth'] = yield utils.get_aggregration_count(total_bandwidth, 'count')

            return self.write(json.dumps(stats, default=str))

    class Bandwidth(LoginChecker):

        @gen.coroutine
        def get(self):
            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)
            usage = self.get_argument('usage', None)

            if usage == 'hourday':
                bandwidth_query = db.access_logs.aggregate([
                    {'$match': {'timestamp': {'$gt': since}}},
                    {'$group': {'_id': {'$hour': '$timestamp'}, 'count': {'$sum': '$size'}}},
                    {'$project': {'_id': 0, 'hourday': '$_id', 'count': 1}}
                ])


            elif usage == 'dayweek':
                bandwidth_query = db.access_logs.aggregate([
                    {'$match': {'timestamp': {'$gt': since}}},
                    {'$group': {'_id': {'$dayOfWeek': '$timestamp'}, 'count': {'$sum': '$size'}}},
                    {'$project': {'_id': 0, 'dayweek': '$_id', 'count': 1}}
                ])

            elif usage == 'month':
                bandwidth_query = db.access_logs.aggregate([
                    {'$match': {'timestamp': {'$gt': since}}},
                    {'$group': {'_id': {'$month': '$timestamp'}, 'count': {'$sum': '$size'}}},
                    {'$project': {'_id': 0, 'month': '$_id', 'count': 1}}
                ])

            elif usage =='url':
                bandwidth_query = db.access_logs.aggregate([
                    {'$match': {'timestamp': {'$gt': since}}},
                    {'$group': {'_id': '$request', 'count': {'$sum': '$size'}}},
                    {'$project': {'_id': 0, 'url': '$_id', 'count': 1}},
                    {'$sort': {'count' : -1}},
                    {'$limit': 15}
                ])
            else :
                return self.write(json.dumps({'success':False}, default=str))

            results = []
            while (yield bandwidth_query.fetch_next):
                results.append(bandwidth_query.next_object())

            return self.write(json.dumps(results, default=str))

    class Statuscode(LoginChecker):

        @gen.coroutine
        def get(self):
            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            hits_query = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': '$response_code', 'count': {'$sum': 1}, 'size' : {'$sum': '$size'}}}
            ])
            results = []
            while (yield hits_query.fetch_next):
                results.append(hits_query.next_object())

            return self.write(json.dumps(results, default=str))

    class UserSystem(LoginChecker):
        @gen.coroutine
        def get(self):
            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            results = {
                'device':[],
                'ua':[],
                'os':[]
            }

            user_os_query = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': '$client.os.family', 'count' : { '$sum': 1}}},
                {'$limit': 15},
                {'$project': {'_id': 0, 'os': '$_id', 'count': 1}},
                {'$sort' : {'count': -1}}
            ])

            while (yield user_os_query.fetch_next):
                results['os'].append(user_os_query.next_object())

            user_device_query = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': '$client.device.family', 'count': {'$sum': 1}}},
                {'$limit': 15},
                {'$project': {'_id': 0, 'device': '$_id', 'count': 1}},
                {'$sort': {'count': -1}}
            ])

            while (yield user_device_query.fetch_next):
                results['device'].append(user_device_query.next_object())

            user_ua_query = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': '$client.user_agent.family', 'count': {'$sum': 1}}},
                {'$limit': 15},
                {'$project': {'_id': 0, 'user_agent': '$_id', 'count': 1}},
                {'$sort': {'count': -1}}
            ])

            while (yield user_ua_query.fetch_next):
                results['ua'].append(user_ua_query.next_object())

            return self.write(json.dumps(results, default=str))

    class Geographic(LoginChecker):
        @gen.coroutine
        def get(self):
            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)
            # group by country code and it's name
            # project the results of grouping
            # sort and send it back
            geolocation_query = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': {'c_code': '$remote_ip.country_code', 'name':'$remote_ip.country'}, 'count': {'$sum': 1}}},
                {'$project': {'_id': 0, 'country': '$_id.name' ,'c_code': {'$toLower' : '$_id.c_code'}, 'count': 1}},
                {'$sort': {'count': -1}}
            ])

            results = []
            while (yield geolocation_query.fetch_next):
                results.append(geolocation_query.next_object())

            return self.write(json.dumps(results, default=str))

    class LoginHandler(tornado.web.RequestHandler):
        @gen.coroutine
        def post(self):
            if self.current_user is not None:
                # user is already logged in
                self.redirect('/')
            else:
                username = self.get_body_argument('username', None)
                password = self.get_body_argument('password', None)

                if username is None or password is None:
                    # forms fields were empty
                    return self.redirect('/login')

                # look up that username
                query_username = yield db.user.find_one(
                    {'username': username}
                )

                if query_username is None :
                    # database did not find that username
                    return self.redirect('/login')
                else:
                    # Now check hashed passwords
                    if bcrypt.checkpw(password, query_username['secret']):
                        self.set_secure_cookie('user', username)
                        # Login Successful
                        return self.redirect('/')
                    else:
                        return self.redirect('/login')


def route_config():
    return [(r"/api/bandwidth*", RestHandler.Bandwidth),
            (r"/api/statuscode*", RestHandler.Statuscode),
            (r"/api/summary*", RestHandler.Summary),
            (r"/api/geographic*", RestHandler.Geographic),
            (r"/api/usersystem*", RestHandler.UserSystem),
            (r"/api/login*", RestHandler.LoginHandler)]

