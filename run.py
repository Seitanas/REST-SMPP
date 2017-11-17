#!/usr/bin/env python

'''
    Author: Tadas Ustinavičius
            <tadas at ring dot lt>
    2017.11.17
'''

from module import ErrorSerializer
from module import Auth
from module import SMS
from module import Config

import falcon





smsApp = falcon.API()
smsApp.set_error_serializer(ErrorSerializer.Response)
smsApp.add_route('/auth', Auth.AuthResource())
smsApp.add_route('/sms', SMS.SMSResource())
