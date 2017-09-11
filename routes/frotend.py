import os

import tornado.ioloop
import tornado.web

settings = {
    'view_path': '../views',
    'index_file': 'index.html',
    'bandwidth': 'bandwidth.html',
    'statuscode': 'status_code.html',
    'geographic': 'geographic.html',
    'static_path': 'static'
}



class FrontEnd:
    class Index(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(settings['view_path'], settings['index_file']))

    class Bandwidth(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(settings['view_path'], settings['bandwidth']))

    class Statuscode(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(settings['view_path'], settings['statuscode']))

    class Geographic(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(settings['view_path'], settings['geographic']))


def route_config():
    return [
        (r'/', FrontEnd.Index),
        (r'/statuscode', FrontEnd.Statuscode),
        (r'/bandwidth', FrontEnd.Bandwidth),
        (r'/geographic', FrontEnd.Geographic),
    ]
