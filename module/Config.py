from configparser import ConfigParser


class ReadConfig:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read('sms.cfg')
