import os
from datetime import timedelta, date, datetime

from .attendance import Attendance
from .connect import Connect
from .user import User


class Meeting:
    def __init__(self, sco_id, **kwargs):
        self.sco_id = sco_id
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
    # def __init__(self, name, date_begin, scoid):
        # self.name = name
        # self.date = datetime.strptime(date_begin[:-10], '%Y-%m-%dT%H:%M:%S')  # datetime.strptime(date, '%Y-%m-%dT%')
        # self.scoid = scoid
        # self.attendees = []


    def __repr__(self):
        return "<Meeting {} {}>".format(self.name, self.date_begin[:10])

    def get_attendances(self, on_or_after=None, before=None, exclude_admins=True):
        return Attendance.fetch_by_meeting_sco_id(self.sco_id, on_or_after, before, exclude_admins)

    def get_attendees(self, on_or_after=None, before=None, exclude_admins=True):
        return User.fetch_by_meeting_attendance(self.sco_id, on_or_after, before, exclude_admins)


    # def get_attendees(self, exclude_admins=True, on_or_after=None, before=None):
    #     # filters = {
    #     #     'sco-id': self.scoid,
    #     #     'filter-gte-date-created': self.date.strftime('%Y-%m-%d'),
    #     #     'filter-lt-date-created': (self.date + timedelta(1)).strftime('%Y-%m-%d')
    #     # }
    #     # rows = Connect.send_request(action='report-meeting-attendance', **filters)
    #     conditions = ['sco-id={}'.format(self.sco_id)]
    #     if on_or_after: conditions.append('filter-gte-date-created={}'.format(on_or_after))
    #     if before: conditions.append('filter-lt-date-created={}'.format(before))
    #
    #     attendees = Connect.send_request1('report-meeting-attendance', conditions)
    #     print(attendees)
    #
    #     users_to_exclude = []
    #     if exclude_admins: users_to_exclude = constants.MOODLE_ADMIN_USERS
    #
    #     for attendee in rows:
    #         if attendee.find('login').text not in [user.email for user in self.attendees] and \
    #                         attendee.find('login').text not in users_to_exclude:
    #             self.attendees.append(
    #                 User(
    #                     email=attendee.find('login').text,
    #                     first_name=attendee.find('participant-name').text,
    #                     last_name=attendee.find('participant-name').text,
    #                     date_created=attendee.find('date-created').text,
    #                     date_end=attendee.find('date-end').text
    #                 )
    #             )
    #
    #     return self.attendees

    @classmethod
    def fetch_by_folder_sco_id(cls, sco_id, on_or_after=None, before=None, sort='desc', limit=0):
        conditions = ['sco-id={}'.format(sco_id)]
        if on_or_after: conditions.append('filter-gte-date-begin={}'.format(on_or_after))
        if before: conditions.append('filter-lt-date-begin={}'.format(before))
        if sort: conditions.append('sort-date-begin={}'.format(sort))
        if limit: conditions.append('filter-rows={}'.format(limit))

        return [cls(**meeting) for meeting in Connect.send_request1('sco-contents', conditions)]

    # @classmethod
    # def fetch_meetings_by_folder(cls, folder_sco_id, on_or_after=None, before=None, sort='desc', limit=0):
    #     filters = {}
    #     if on_or_after:
    #         filters['filter-gte-date-begin'] = on_or_after
    #     if before:
    #         filters['filter-lt-date-begin'] = before
    #     if sort:
    #         filters['sort-date-begin'] = sort
    #     if limit > 0:
    #         filters['filter-rows'] = limit
    #
    #     rows = Connect.get_sco_contents(folder_sco_id, filters)
    #     if not rows:
    #         raise ValueError('No meetings found on date {}'.format(on_or_after))
    #     meetings = []
    #     for meeting in rows:
    #         meetings.append(
    #             Meeting(
    #                 meeting.find('name').text,
    #                 meeting.find('date-begin').text,
    #                 meeting.attrib['sco-id']
    #             )
    #         )
    #
    #     if len(meetings) == 1:
    #         return meetings[0]
    #     return meetings
    #     # print(meetings)

    @classmethod
    def fetch_summary_by_sco_id(cls, sco_id):
        conditions = ['sco-id={}'.format(sco_id)]
        meetings = Connect.send_request1('report-meeting-summary', conditions)
        return [Meeting(**meeting) for meeting in meetings][0]
