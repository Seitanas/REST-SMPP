import json
import io
import falcon
from .Database import QueryDB
from module import Config
import smpplib2.gsm
import smpplib2.client
import smpplib2.consts
import sys


class SendSMS:

    def __init__(self, json_data):

        self.json_data = json_data
        cfg = Config.ReadConfig()
        self.smpp_user_id = cfg.config.get('smpp', 'userid')
        self.smpp_password = cfg.config.get('smpp', 'password')
        self.smpp_address = cfg.config.get('smpp', 'address')
        self.smpp_port = cfg.config.get('smpp', 'port')

    def run(self):

        try:
            def received_message_handler(pdu):
                return sys.stdout.write('SMSC has sent a request {} {}\n'.format(pdu.sequence, pdu.message_id))

            def smsc_message_resp_handler(pdu):
                return sys.stdout.write('SMSC has sent a response to our request {} {}\n'.format(pdu.sequence, pdu.message_id))

            def esme_sent_msg_handler(ssm):
                return sys.stdout.write('we are about to send message: {} with sequence_number:{} to phone_number: {}'.format(ssm.short_message, ssm.sequence, ssm.destination_addr))

            message = self.json_data['sendsms']['text']
            sender = self.json_data['sendsms']['sender']
            number = self.json_data['sendsms']['number']
            parts, encoding_flag, msg_type_flag = smpplib2.gsm.make_parts(message)
            client = smpplib2.client.Client(self.smpp_address, self.smpp_port)
            client.set_message_response_handler(smsc_message_resp_handler)
            client.set_message_received_handler(received_message_handler)
            client.set_esme_sent_msg_handler(esme_sent_msg_handler)
            client.connect()
            client.bind_transceiver(system_id=self.smpp_user_id.decode("utf-8"), password=self.smpp_password.decode("utf-8"))
            for part in parts:
                pdu = client.send_message(
                    source_addr_ton=smpplib2.consts.SMPP_TON_ALNUM,
                    source_addr=sender,
                    dest_addr_ton=smpplib2.consts.SMPP_TON_INTL,
                    dest_addr_npi=smpplib2.consts.SMPP_NPI_ISDN,
                    destination_addr=number.replace('+', ''),
                    short_message=part,
                    esm_class=msg_type_flag,
                    data_coding=encoding_flag,
                    registered_delivery=False,
                )
                print(pdu.sequence)
            return 0
        except Exception, e:
            print (e)
            return 1



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
            db = QueryDB()
            reply = db.execute("SELECT id FROM tokens WHERE token = \"%s\" AND expires > NOW()" % token)
            if not len(reply):
                raise falcon.HTTPError(falcon.HTTP_401, title = None, description = "Token not found")
            sms = SendSMS(json_data)
            if sms.run():
                reply = {}
                reply['status'] = 'error'
            else:
                reply = {}
                reply['status'] = 'success'
            resp.body = json.dumps(reply)

    def on_get(self, req, resp):
        raise falcon.HTTPError(falcon.HTTP_400, title = None, description='Non-POST request')

