import tornado.ioloop
import tornado.web
from motor import MotorClient
import json
import re
import utils.utils as utils
from tornado import gen

connection = MotorClient()
db = connection.nginxLogger


class RestHandler:
    class Summary(tornado.web.RequestHandler):
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

            self.write(json.dumps(stats, default=str))

    class Bandwidth(tornado.web.RequestHandler):
        def get(self):
            query = db.access_logs.aggregate([
                {'$group': {'_id': {'$month': "$timestamp"}, 'count': {'$sum': '$size'}}},
                {'$sort': {'_id': 1}}
            ])
            self.write(json.dumps(list(query)))

    class Statuscode(tornado.web.RequestHandler):
        @gen.coroutine
        def get(self):

            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            hits_query = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': '$response_code', 'count': {'$sum': 1}}}
            ])
            results = []
            while (yield hits_query.fetch_next):
                results.append(hits_query.next_object())

            self.write(json.dumps(results, default=str))

    class UserSystem(tornado.web.RequestHandler):
        @gen.coroutine
        def get(self):
            stats = {}
            # TODO
            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            query = yield db.access_logs.find_one({'response_code':'404'})
            self.write(json.dumps(query, default=str))

    class Geographic(tornado.web.RequestHandler):
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

            self.write(json.dumps(results, default=str))



def route_config():
    return [(r"/api/bandwidth*", RestHandler.Bandwidth),
            (r"/api/statuscode*", RestHandler.Statuscode),
            (r"/api/summary*", RestHandler.Summary),
            (r"/api/geographic*", RestHandler.Geographic),
            (r"/api/usersystem*", RestHandler.UserSystem)]
