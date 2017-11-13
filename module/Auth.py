import json
import io
import falcon
from .Database import QueryDB
from module import Config
import hashlib
from random import choice
from string import digits
from datetime import datetime, timedelta



def TokenGen(json_data):

    """Checks user credentials, generates Auth token"""

    db = QueryDB()
    reply = db.execute("SELECT id, password FROM users WHERE username = \"%s\"" % json_data["auth"]["username"])
    if len(reply):
        cfg = Config.ReadConfig()
        salt = cfg.config.get('security', 'salt')
        md5hash = hashlib.md5( str(salt).encode('utf-8') + str(json_data["auth"]["password"]).encode('utf-8') ).hexdigest()
        for pw in reply:
            if pw[1] != md5hash:
                raise falcon.HTTPError(falcon.HTTP_400, title = None, description = "Wrong username/password")
            else:
                curr_time = datetime.now()
                created = curr_time.strftime("%Y-%m-%d %H:%M:%S")
                expires = curr_time + timedelta(days=1)
                expires = expires.strftime("%Y-%m-%d %H:%M:%S")
                token = (''.join(choice("abcdef" + digits) for i in range(26)))
                db.commit("INSERT INTO tokens (userid, token, created, expires) VALUES (\"%s\", \"%s\", \"%s\", \"%s\")" % (pw[0], token, created, expires))
                reply = {}
                reply['token'] = {}
                reply['token']['id'] = token
                reply['token']['created_at'] = created
                reply['token']['expires_at'] = expires
                return reply

class AuthResource:

    def on_post(self, req, resp):
        try:
             post_data = req.stream.read().decode('utf-8')
        except Exception as ex:
             raise falcon.HTTPError(falcon.HTTP_400, title = None, description = ex.message)
        try:
             json_data = json.loads(post_data, encoding='utf-8')
        except ValueError:
             raise falcon.HTTPError(falcon.HTTP_400, title = None, description = "Invalid JSON")
        if "auth" in json_data:
            if "username" in json_data["auth"] and "password" in json_data["auth"]:
                result = TokenGen(json_data)
                resp.body = json.dumps(result)

        else:
            raise falcon.HTTPError(falcon.HTTP_400, title = None, description = "Missing user credentials in JSON")

    def on_get(self, req, resp):
        raise falcon.HTTPError(falcon.HTTP_400, title = None, description='Non-POST request')

