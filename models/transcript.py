from .connect import Connect
from .interaction import Interaction


class Transcript:
    # def __init__(self, user, login, status, date, transcript_id, principal_id, type):
    #     self.user = user
    #     self.login = login
    #     self.status = status
    #     self.date = date
    #     self.transcript_id = transcript_id
    #     self.principal_id = principal_id
    #     self.type = type
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return "<Transcript {}>".format(self.transcript_id)

    @classmethod
    def fetch_by_principal_id(cls, principal_id):
        conditions = ['principal-id={}'.format(principal_id)]
        transcripts = Connect.send_request1('report-user-training-transcripts', conditions)
        return [Transcript(**transcript) for transcript in transcripts]

    def report_quiz_interactions(self, on_or_after=None, before=None):
        conditions = [
            'sco-id={}'.format(self.sco_id),
            'filter-transcript-id={}'.format(self.transcript_id)
        ]
        if on_or_after:
            conditions.append('filter-gte-date-created={}'.format(on_or_after))
        if before:
            conditions.append('filter-lt-date-created={}'.format(before))
        interactions = Connect.send_request1('report-quiz-interactions', conditions)
        return [Interaction(**interaction) for interaction in interactions]
