from datetime import timedelta, datetime
import constants
from .connect import Connect
from .user import User


class Meeting:
    def __init__(self, name, date, scoid):
        self.name = name
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.scoid = scoid
        self.attendees = []

    def __repr__(self):
        return "<Meeting {} {}>".format(self.date, self.name)

    def get_attendees(self, exclude_admins=True):
        filters = {
            'sco-id': self.scoid,
            'filter-gte-date-created': self.date.isoformat(),
            'filter-lt-date-created': (self.date + timedelta(1)).isoformat()
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
    def fetch_meetings_by_folder(cls, folder_sco_id, datestring=None):
        filters = {}
        if datestring:
            date = datetime.strptime(datestring, '%Y-%m-%d')
            plus_one_day = date + timedelta(days=1)
            filters = {
                'filter-gte-date-begin': date.strftime('%Y-%m-%d'),
                'filter-lt-date-begin': plus_one_day.strftime('%Y-%m-%d')
            }
        rows = Connect.get_sco_contents(folder_sco_id, filters)
        meetings = []
        for meeting in rows:
            meetings.append(
                Meeting(
                    meeting.find('name').text,
                    meeting.find('date-begin').text[:10],
                    meeting.attrib['sco-id']
                )
            )

        if len(meetings) == 1:
            return meetings[0]
        return meetings
        # print(meetings)
