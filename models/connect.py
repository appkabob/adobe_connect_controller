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
            raise IOError('ERROR RETRIEVING CONNECT COOKIE: {}'.format(status))
                # cls.status('ERROR RETRIEVING CONNECT COOKIE: {}'.format(status))
        else:
            cls.status = root.find('status').attrib['code']
            cls.cookie = root.find('common/cookie').text
            cls.login()

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
    def send_request(cls, action, conditions):
        url = '{}{}&session={}'.format(constants.CONNECT_BASE_URL, action, cls.cookie)
        if isinstance(conditions, list):
            url += '&{}'.format('&'.join(conditions))
        elif isinstance(conditions, str):
            url += '&{}'.format(conditions)
        else:
            raise ValueError('conditions must be string or list')

        # if isinstance(*args, str):
        #     url += '&{}'.format(*args)
        # else:
        #     url += '&'.join(*args)
        with urllib.request.urlopen(url) as response:
            xml = response.read()
        root = ET.fromstring(xml)
        status = root.find('status').attrib['code']
        if status != 'ok':
            raise IOError('ERROR SENDING {} REQUEST TO ADOBE CONNECT: {}'.format(action, status))
            cls.status = 'ERROR SENDING {} REQUEST TO ADOBE CONNECT: {}'.format(action, status)
            return cls.status
        else:
            cls.status = root.find('status').attrib['code']

            if action == 'sco-contents':
                xml_records = root.findall('scos/sco')
            elif action == 'principal-list':
                xml_records = root.findall('principal-list/principal')
            elif action == 'principal-info' or action == 'principal-update':
                xml_records = root.find('principal')
            elif action == 'report-course-status':
                xml_records = root.find('report-course-status')
            elif action == 'sco-info':
                xml_records = root.find('sco')
            elif action == 'group-membership-update':
                return True
            else:
                xml_records = root.findall('{}/row'.format(action))
            return cls.convert_xml_to_object(xml_records)

    @staticmethod
    def convert_xml_to_object(xml):
        output = []
        if not isinstance(xml, list):
            xml = [xml]
        for row in xml:
            cleaned_data = {}
            data = row.attrib
            for item in row:
                data[item.tag] = item.text
            for key in data:  # replace all dashes in parameter names so that they can be recalled more easily in Python
                cleaned_data[key.replace('-', '_')] = data[key]
            output.append(cleaned_data)
        return output
