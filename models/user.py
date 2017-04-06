from selenium import webdriver
from .connect import Connect


class User:
    def __init__(self, email, first_name=None, last_name=None, **kwargs):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.attributes = kwargs
        self.principalid = None
        self.fetch_detailed_user_info()
        # self.oauth_token = oauth_token
        # self.oauth_token_secret = oauth_token_secret
        # self.id = id

    def __repr__(self):
        return "<User {}>".format(self.email)

    def fetch_principal_id(self):
        filters = {'filter-login': self.email}
        user_info = Connect.send_request('principal-list', **filters)[0]
        self.principalid = user_info.attrib.get('principal-id')

    def fetch_separate_firstname_lastname(self):
        if not self.principalid:
            self.fetch_principal_id()
        if not self.first_name or not self.last_name or self.first_name == self.last_name:
            filters = {'principal-id': self.principalid}
            user_details = Connect.send_request('principal-info', **filters)
            self.first_name = user_details.find('first-name').text
            self.last_name = user_details.find('last-name').text

    def fetch_detailed_user_info(self):
        if not self.principalid:
            self.fetch_principal_id()
        self.fetch_separate_firstname_lastname()




    # @classmethod
    # def load_from_dnn(cls):
    #     browser = webdriver.Firefox()
    #     browser.get('http://seleniumhq.org/')


    # def save_to_db(self):
    #     with CursorFromConnectionFromPool() as cursor:
    #         cursor.execute('INSERT INTO users (email, first_name, last_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s, %s, %s)',
    #                        (self.email, self.first_name, self.last_name, self.oauth_token, self.oauth_token_secret))
    #
    # @classmethod
    # def load_from_db_by_email(cls, email):
    #     with CursorFromConnectionFromPool() as cursor:
    #         cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
    #         user_data = cursor.fetchone()
    #     return cls(email=user_data[1], first_name=user_data[2],
    #                last_name=user_data[3], oauth_token=user_data[4],
    #                oauth_token_secret=user_data[5], id=user_data[0])