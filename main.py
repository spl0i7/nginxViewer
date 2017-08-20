import tornado.web
import tornado
from Routes import api

def make_app():
    api_routes = api.route_config()
    return tornado.web.Application(api_routes)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print('Started Web server on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()
