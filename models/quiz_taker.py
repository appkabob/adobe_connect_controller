from .connect import Connect


class QuizTaker():
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return "<QuizTaker {}>".format(self.login)

    @classmethod
    def fetch_by_sco_id(cls, sco_id, on_or_after=None, before=None):
        conditions = ['sco-id={}'.format(sco_id)]
        if on_or_after: conditions.append('filter-gte-date-created={}'.format(on_or_after))
        if before: conditions.append('filter-lt-date-created={}'.format(before))
        return [cls(**quiz_taker) for quiz_taker in Connect.send_request('report-quiz-takers', conditions)]
