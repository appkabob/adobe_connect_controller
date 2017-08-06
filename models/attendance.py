from datetime import datetime

import constants
from .connect import Connect


class Attendance:
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return "<Attendance {} {} {}>".format(self.sco_name, self.participant_name, self.date_created[:10])

    @classmethod
    def fetch_by_meeting_sco_id(cls, sco_id, on_or_after=None, before=None, exclude_admins=True):
        conditions = ['sco-id={}'.format(sco_id)]
        if on_or_after: conditions.append('filter-gte-date-created={}'.format(on_or_after))
        if before: conditions.append('filter-lt-date-created={}'.format(before))
        attendances = Connect.send_request('report-meeting-attendance', conditions)
        users_to_exclude = []
        if exclude_admins: users_to_exclude = constants.CONNECT_ADMIN_USERS
        for attendance in attendances:
            if 'login' not in attendance:  # if user attended as guest without being logged in
                attendance['login'] = None
                attendance['participant_name'] = attendance['session_name']
        return [cls(**attendance) for attendance in attendances if attendance['login'] not in users_to_exclude]

    def duration_in_seconds(self):
        date_created = datetime.strptime(' '.join(self.date_created[:19].split('T')), '%Y-%m-%d %H:%M:%S')
        date_end = datetime.strptime(' '.join(self.date_end[:19].split('T')), '%Y-%m-%d %H:%M:%S')
        return (date_end - date_created).total_seconds()

    def duration_in_minutes(self):
        return self.duration_in_seconds() / 60
