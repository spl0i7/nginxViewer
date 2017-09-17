import os

import tornado.ioloop
import tornado.web

settings = {
    'view_path': '../views',
    'index_file': 'index.html',
    'bandwidth': 'bandwidth.html',
    'status_code': 'status_code.html',
    'geographic': 'geographic.html',
    'user_system': 'user_system.html',
    'login' : 'login.html',
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
            self.render(os.path.join(settings['view_path'], settings['status_code']))

    class Geographic(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(settings['view_path'], settings['geographic']))

    class Usersystem(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(settings['view_path'], settings['user_system']))


    class Login(tornado.web.RequestHandler):
        def get(self):
            self.render(os.path.join(settings['view_path'], settings['login']))


def route_config():
    return [
        (r'/', FrontEnd.Index),
        (r'/statuscode', FrontEnd.Statuscode),
        (r'/bandwidth', FrontEnd.Bandwidth),
        (r'/geographic', FrontEnd.Geographic),
        (r'/usersystem', FrontEnd.Usersystem),
        (r'/login', FrontEnd.Login),
    ]
