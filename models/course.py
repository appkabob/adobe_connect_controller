from .interaction import Interaction
from .quiz_taker import QuizTaker
from .connect import Connect


class Course:
    def __init__(self, **kwargs):
        self.quiz_takers = []
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return '<Course {}>'.format(self.name)

    @classmethod
    def fetch_by_sco_id(cls, sco_id):
        course = Connect.send_request('sco-info', 'sco-id={}'.format(sco_id))[0]
        return cls(**course)

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

        return [cls(**course) for course in all_items
            if course['icon'].lower() == 'course' and course['type'].lower() == 'content']

    def report_quiz_interactions(self, on_or_after=None, before=None):
        conditions = ['sco-id={}'.format(self.sco_id)]
        if on_or_after:
            conditions.append('filter-gte-date-created={}'.format(on_or_after))
        if before:
            conditions.append('filter-lt-date-created={}'.format(before))
        interactions = Connect.send_request('report-quiz-interactions', conditions)
        return [Interaction(**interaction) for interaction in interactions]

    def report_quiz_takers(self, on_or_after=None):
        return QuizTaker.fetch_by_sco_id(self.sco_id, on_or_after)
