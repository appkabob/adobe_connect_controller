from .attendance import Attendance
from .connect import Connect
from .user import User


class Meeting:
    def __init__(self, sco_id, **kwargs):
        self.sco_id = sco_id
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return "<Meeting {} {}>".format(self.name, self.date_begin[:10])

    def get_attendances(self, on_or_after=None, before=None, exclude_admins=True):
        return Attendance.fetch_by_meeting_sco_id(self.sco_id, on_or_after, before, exclude_admins)

    def get_attendees(self, on_or_after=None, before=None, exclude_admins=True):
        return User.fetch_by_meeting_attendance(self.sco_id, on_or_after, before, exclude_admins)

    @classmethod
    def fetch_by_folder_sco_id(cls, sco_id, on_or_after=None, before=None, sort='desc', limit=0, recursive=False):
        conditions = ['sco-id={}'.format(sco_id)]
        if on_or_after: conditions.append('filter-gte-date-begin={}'.format(on_or_after))
        if before: conditions.append('filter-lt-date-begin={}'.format(before))
        if sort: conditions.append('sort-date-begin={}'.format(sort))
        if limit: conditions.append('filter-rows={}'.format(limit))

        folder_items = Connect.send_request('sco-contents', conditions)
        all_items = folder_items
        for item in folder_items:
            if recursive and item['type'].lower() == 'folder':
                conditions[0] = 'sco-id={}'.format(item['sco_id'])
                all_items.extend(Connect.send_request('sco-contents', conditions))

        return [cls(**meeting) for meeting in all_items
                if meeting['type'].lower() == 'meeting']

    @classmethod
    def fetch_summary_by_sco_id(cls, sco_id):
        conditions = ['sco-id={}'.format(sco_id)]
        meetings = Connect.send_request('report-meeting-summary', conditions)
        return [Meeting(**meeting) for meeting in meetings][0]
