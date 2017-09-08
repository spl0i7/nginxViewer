import os

import tornado.ioloop
import tornado.web

from routes import cfg


class FrontEnd:
    class Index(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(cfg.settings['view_path'], cfg.settings['index_file']))

    class Bandwidth(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(cfg.settings['view_path'], cfg.settings['bandwidth']))

    class Statuscode(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(cfg.settings['view_path'], cfg.settings['statuscode']))


def route_config():
    return [
        (r'/', FrontEnd.Index),
        (r'/statuscode', FrontEnd.Statuscode),
        (r'/bandwidth', FrontEnd.Bandwidth),
    ]
