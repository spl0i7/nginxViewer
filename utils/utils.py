import datetime
from motor import MotorClient
from tornado import gen
import tornado.web
import json
import re
import bcrypt


connection = MotorClient()
db = connection.nginxLogger

class LoginChecker(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

    def prepare(self):
        if not self.current_user:
            if re.match(r'^/api', self.request.path):
                return self.write(json.dumps({'success': False}, default=str))
            else:
                return self.redirect('/login')

async def get_aggregration_count(x, field):
    results = []
    async for doc in x:
        results.append(doc)
    try:
        return results[0][field]
    except:
        return 0


def get_since_today(timespan):
    since = datetime.datetime.min
    today = datetime.datetime.today()

    if timespan == 'day':
        since = today - datetime.timedelta(days=1)
    elif timespan == 'week':
        since = today - datetime.timedelta(days=7)
    elif timespan == 'month':
        since = today - datetime.timedelta(days=30)
    return since
