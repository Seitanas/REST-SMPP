#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Author: Tadas Ustinavičius
            <tadas at ring dot lt>
    2017.11.20
    https://github.com/Seitanas/REST-SMPP
'''

from module import ErrorSerializer
from module import Auth
from module import SMS
from module import Config
import logging
import logging.config
import os
import falcon



logdir = "/var/log/SMS";
if not os.path.exists(logdir):
    os.makedirs(logdir)
logging.config.fileConfig('sms.cfg')
logger = logging.getLogger('REST-SMPP')
logger.debug("Starting REST-SMPP")

smsApp = falcon.API()
smsApp.set_error_serializer(ErrorSerializer.Response)
smsApp.add_route('/auth', Auth.AuthResource())
smsApp.add_route('/sms', SMS.SMSResource())
