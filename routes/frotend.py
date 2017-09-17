import os

import tornado.ioloop
import tornado.web
from utils.utils import LoginChecker
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
    class Index(LoginChecker):
        def get(self):
            return self.render(os.path.join(settings['view_path'], settings['index_file']))

    class Bandwidth(LoginChecker):
        def get(self):
            return self.render(os.path.join(settings['view_path'], settings['bandwidth']))

    class Statuscode(LoginChecker):
        def get(self):
            return self.render(os.path.join(settings['view_path'], settings['status_code']))

    class Geographic(LoginChecker):
        def get(self):
            return self.render(os.path.join(settings['view_path'], settings['geographic']))

    class Usersystem(LoginChecker):
        def get(self):
            return self.render(os.path.join(settings['view_path'], settings['user_system']))

    class Login(tornado.web.RequestHandler):
        def get(self):
            if self.get_secure_cookie('user') is not None:
                return self.redirect('/')
            else:
                return self.render(os.path.join(settings['view_path'], settings['login']))

    class Logout(LoginChecker):
        def get(self):
            self.clear_cookie('user')
            return self.redirect('/login')


def route_config():
    return [
        (r'/', FrontEnd.Index),
        (r'/statuscode', FrontEnd.Statuscode),
        (r'/bandwidth', FrontEnd.Bandwidth),
        (r'/geographic', FrontEnd.Geographic),
        (r'/usersystem', FrontEnd.Usersystem),
        (r'/login', FrontEnd.Login),
        (r'/logout', FrontEnd.Logout)
    ]
