import tornado.ioloop
import tornado.web
from pymongo import MongoClient
import json
import re
import datetime
import utils.utils as utils


connection = MongoClient()
db = connection.nginxLogger


class RestHandler:
    class Summary(tornado.web.RequestHandler):
        def get(self):
            stats = {}

            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            # find the total number of records since a timestamp
            total_req = db.access_logs.count(
                {'timestamp': {'$gt': since}}
            )

            # find response code starting with 1xx , 2xx or 3xx
            valid_req = db.access_logs.count(
                {'response_code': re.compile(r'^[123]'), 'timestamp': {'$gt': since}}
            )
            # find response code starting with 4xx or 5xx
            invalid_req = db.access_logs.count(
                {'response_code': re.compile(r'^[45]'), 'timestamp': {'$gt': since}}
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

            # find out 404 page not found errors
            total_404 = db.access_logs.count(
                {'timestamp': {'$gt': since}, 'response_code': '404'}
            )

            # these are simply an int
            stats['total_requests'] = total_req
            stats['valid_req'] = valid_req
            stats['invalid_req'] = invalid_req
            stats['total_404'] = total_404

            # extract count from the results of query
            stats['unique_visitor'] = utils.get_aggregration_count(unique_visitor, 'count')
            stats['total_bandwidth'] = utils.get_aggregration_count(total_bandwidth, 'count')

            self.write(json.dumps(stats))

    class Bandwidth(tornado.web.RequestHandler):
        def get(self):
            query = db.access_logs.aggregate([
                {'$group': {'_id': {'$month': "$timestamp"}, 'count': {'$sum': '$size'}}},
                {'$sort': {'_id': 1}}
            ])
            self.write(json.dumps(list(query)))

    class Statuscode(tornado.web.RequestHandler):
        def get(self):

            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            hits_query = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': '$response_code', 'count': {'$sum': 1}}}
            ])

            self.write(json.dumps(list(hits_query)))

    class UserSystem(tornado.web.RequestHandler):
        def get(self):
            stats = {}

            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            self.write(json.dumps(list([])))

    class Geographic(tornado.web.RequestHandler):
        def get(self):
            timespan = self.get_argument('timespan', None)
            since = utils.get_since_today(timespan)

            geolocation_query = db.access_logs.aggregate([
                {'$match': {'timestamp': {'$gt': since}}},
                {'$group': {'_id': '$remote_ip.country_code', 'count': {'$sum': 1}}},
                {'$project': {'_id': 0, 'c_code': {'$toLower' : '$_id'}, 'count': 1}},
            ])
            self.write(json.dumps(list(geolocation_query)))



def route_config():
    return [(r"/api/bandwidth*", RestHandler.Bandwidth),
            (r"/api/statuscode*", RestHandler.Statuscode),
            (r"/api/summary*", RestHandler.Summary),
            (r"/api/geographic*", RestHandler.Geographic)]
