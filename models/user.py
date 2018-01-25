from .attendance import Attendance
from .connect import Connect


class User:
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
        users = [cls(**user) for user in Connect.send_request('principal-list', conditions)]
        if users: return users[0]
        return None

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

    @classmethod
    def create_in_connect(cls, login, first_name, last_name, password):
        conditions = 'login={}&email={}&first-name={}&last-name={}&password={}&has-children=false&type=user'.format(
            login, login, first_name, last_name, password)
        return [cls(**user) for user in Connect.send_request('principal-update', conditions)][0]

    def add_to_group(self, group_id):
        # PEC 2268963
        conditions = 'group-id={}&principal-id={}&is-member=true'.format(group_id, self.principal_id)
        return Connect.send_request('group-membership-update', conditions)

    @classmethod
    def fetch_by_group_id(cls, group_id):
        conditions = 'group-id={}&filter-is-member=true'.format(group_id)
        return [cls(**user) for user in Connect.send_request('principal-list', conditions)]

    def reset_password(self, password):
        conditions = 'user-id={}&password={}&password-verify={}'.format(self.principal_id, password, password)
        result = Connect.send_request('user-update-pwd', conditions)
        return True

    ##for Nick.....

