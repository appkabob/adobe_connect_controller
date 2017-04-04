class Transcript:
    def __init__(self, user, login, status, date, transcript_id, principal_id, type):
        self.user = user
        self.login = login
        self.status = status
        self.date = date
        self.transcript_id = transcript_id
        self.principal_id = principal_id
        self.type = type

    def __repr__(self):
        return "<Transcript {}>".format(self.transcript_id)