from datetime import timedelta, date, datetime
import constants
from .connect import Connect
from .user import User


class Meeting:
    def __init__(self, name, date_begin, scoid):
        self.name = name
        self.date = datetime.strptime(date_begin[:-10], '%Y-%m-%dT%H:%M:%S')  # datetime.strptime(date, '%Y-%m-%dT%')
        self.scoid = scoid
        self.attendees = []

    def __repr__(self):
        return "<Meeting {} {}>".format(self.date, self.name)

    def get_attendees(self, exclude_admins=True):
        filters = {
            'sco-id': self.scoid,
            'filter-gte-date-created': self.date.strftime('%Y-%m-%d'),
            'filter-lt-date-created': (self.date + timedelta(1)).strftime('%Y-%m-%d')
        }
        rows = Connect.send_request(action='report-meeting-attendance', **filters)

        users_to_exclude = []
        if exclude_admins: users_to_exclude = constants.MOODLE_ADMIN_USERS

        for attendee in rows:
            if attendee.find('login').text not in [user.email for user in self.attendees] and \
                            attendee.find('login').text not in users_to_exclude:
                self.attendees.append(
                    User(
                        email=attendee.find('login').text,
                        first_name=attendee.find('participant-name').text,
                        last_name=attendee.find('participant-name').text,
                        date_created=attendee.find('date-created').text,
                        date_end=attendee.find('date-end').text
                    )
                )

        return self.attendees


    @classmethod
    def fetch_meetings_by_folder(cls, folder_sco_id, on_or_after=None, before=None, sort='desc', limit=0):
        filters = {}
        if on_or_after:
            filters['filter-gte-date-begin'] = on_or_after
        if before:
            filters['filter-lt-date-begin'] = before
        if sort:
            filters['sort-date-begin'] = sort
        if limit > 0:
            filters['filter-rows'] = limit

        rows = Connect.get_sco_contents(folder_sco_id, filters)
        meetings = []
        for meeting in rows:
            meetings.append(
                Meeting(
                    meeting.find('name').text,
                    meeting.find('date-begin').text,
                    meeting.attrib['sco-id']
                )
            )

        if len(meetings) == 1:
            return meetings[0]
        return meetings
        # print(meetings)
