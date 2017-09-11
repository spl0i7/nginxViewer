import tornado
import tornado.web

from routes import api
from routes import frotend


def make_app():
    routes = api.route_config() + frotend.route_config()
    return tornado.web.Application(routes, **frotend.settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print('Started Web server on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()
