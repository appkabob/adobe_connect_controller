from .attendance import Attendance
from .connect import Connect


class User:
    # def __init__(self, email, first_name=None, last_name=None, **kwargs):
    #     self.email = email
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.attributes = kwargs
    #     self.principalid = None
    #     self.fetch_detailed_user_info()
    #     # self.oauth_token = oauth_token
    #     # self.oauth_token_secret = oauth_token_secret

    def __init__(self, **kwargs):
        self.attendances = {}
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return "<User {}>".format(self.login)

    @classmethod
    def fetch_by_principal_id(cls, principal_id):
        conditions = 'principal-id={}'.format(principal_id)
        return [cls(**user) for user in Connect.send_request('principal-info', conditions)][0]

    @classmethod
    def fetch_quick_by_login(cls, login):
        conditions = 'filter-login={}'.format(login)
        return [cls(**user) for user in Connect.send_request('principal-list', conditions)][0]

    @classmethod
    def fetch_full_by_login(cls, login):
        user = cls.fetch_quick_by_login(login)
        return cls.fetch_by_principal_id(user.principal_id)

    @classmethod
    def fetch_by_meeting_attendance(cls, sco_id, on_or_after=None, before=None, exclude_admins=True):
        attendances = Attendance.fetch_by_meeting_sco_id(sco_id, on_or_after, before, exclude_admins)
        user_principal_ids = []
        users = []
        for attendance in attendances:
            if attendance.principal_id not in user_principal_ids:
                users.append(cls(login=attendance.login, principal_id=attendance.principal_id, name=attendance.participant_name))
                user_principal_ids.append(attendance.principal_id)
        return users

    def get_attendances_by_meeting_sco_id(self, sco_id, on_or_after=None, before=None):
        attendances = Attendance.fetch_by_meeting_sco_id(sco_id, on_or_after, before)
        self.attendances[sco_id] = {
            'on_or_after': on_or_after,
            'before': before,
            'attendances': [attendance for attendance in attendances if attendance.principal_id == self.principal_id]
        }
        return self.attendances[sco_id]




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