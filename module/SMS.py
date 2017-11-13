import json
import io
import falcon
from .Database import QueryDB
from module import Config


def SendSMS(json_data, token):

    db = QueryDB()
    reply = db.execute("SELECT id FROM tokens WHERE token = \"%s\" AND expires > NOW()" % token)
    if not len(reply):
        raise falcon.HTTPError(falcon.HTTP_401, title = None, description = "Token not found")


class SMSResource:

    def on_post(self, req, resp):
        try:
             post_data = req.stream.read().decode('utf-8')
        except Exception as ex:
             raise falcon.HTTPError(falcon.HTTP_400, title = None, description = ex.message)
        try:
             json_data = json.loads(post_data, encoding='utf-8')
        except ValueError:
             raise falcon.HTTPError(falcon.HTTP_400, title = None, description = "Invalid JSON")
        if "sendsms" in json_data:
            token = req.get_header('X-Auth-Token')
            result = SendSMS(json_data, token)
            resp.body = json.dumps(result)

    def on_get(self, req, resp):
        raise falcon.HTTPError(falcon.HTTP_400, title = None, description='Non-POST request')

