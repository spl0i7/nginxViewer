import tornado.ioloop
import tornado.web
from pymongo import MongoClient

connection = MongoClient()
db = connection.nginxLogger

class RestHandler:


    class Bandwidth(tornado.web.RequestHandler):

        def get(self):
            query = db.access_logs.aggregate([{
                '$group': {
                    '_id': None,
                    'total': {'$sum': '$bytes_sent'}}
            }])
            query = query.next()
            self.write('{:.2f} megabytes'.format(query['total'] / (1000**2)))


def route_config():
    return [(r"/api/bandwidth*", RestHandler.Bandwidth)]