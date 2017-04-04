import urllib.request
import xml.etree.ElementTree as ET
import constants


class Connect:
    cookie = None

    @classmethod
    def __init__(cls):
        cls.cookie = None
        with urllib.request.urlopen('{}common-info'.format(constants.CONNECT_BASE_URL)) as response:
            xml = response.read()
        root = ET.fromstring(xml)
        status = root.find('status').attrib['code']
        if status != 'ok':
            cls.status('ERROR RETRIEVING CONNECT COOKIE: {}'.format(status))
        else:
            cls.status = root.find('status').attrib['code']
            cls.cookie = root.find('common/cookie').text
            cls.login()

    # def __repr__(self):
    #     return "<Connect {}>".format(self.status)

    @classmethod
    def login(cls):
        with urllib.request.urlopen(
                '{}login&login={}&password={}&session={}'.format(constants.CONNECT_BASE_URL,
                                                                 constants.CONNECT_LOGIN,
                                                                 constants.CONNECT_PWD,
                                                                 cls.cookie)) as response:
            xml = response.read()
        root = ET.fromstring(xml)
        status = root.find('status').attrib['code']
        if status != 'ok':
            cls.status = 'ERROR LOGGING IN TO ADOBE CONNECT: {}'.format(status)
        else:
            cls.status = root.find('status').attrib['code']

    @classmethod
    def send_request(cls, action, **kwargs):
        url = '{}{}&session={}'.format(constants.CONNECT_BASE_URL, action, cls.cookie)
        for key in kwargs:
            url += "&{0}={1}".format(key, kwargs[key])
        with urllib.request.urlopen(url) as response:
            xml = response.read()
        root = ET.fromstring(xml)
        status = root.find('status').attrib['code']
        if status != 'ok':
            cls.status = 'ERROR SENDING {} REQUEST TO ADOBE CONNECT: {}'.format(action, status)
            return cls.status
        else:
            cls.status = root.find('status').attrib['code']
            return root.findall('{}/row'.format(action))
