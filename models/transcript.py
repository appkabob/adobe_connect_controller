from .connect import Connect
from .interaction import Interaction


class Transcript:
    """Parameters: login, status, date-taken, transcript_id, principal_id, type, sco_id, name"""
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return "<Transcript {}>".format(self.transcript_id)

    def to_dict(self):
        return {
            'date': self.date_taken,
            'login': self.login,
            'course': self.name,
            'status': self.status,
            'score': self.score,
            'max_score': self.max_score,
            'certificate': self.certificate
        }

    @classmethod
    def fetch_by_principal_id(cls, principal_id):
        conditions = ['principal-id={}'.format(principal_id)]
        transcripts = Connect.send_request('report-user-training-transcripts', conditions)
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
        interactions = Connect.send_request('report-quiz-interactions', conditions)
        return [Interaction(**interaction) for interaction in interactions]
