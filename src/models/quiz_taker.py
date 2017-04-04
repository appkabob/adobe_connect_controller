class QuizTaker:
    def __init__(self, user, login, status, date, transcript_id, principal_id):
        # score, attempts, version,
        self.user = user
        self.login = login
        self.status = status
        self.date = date
        # self.score = score
        # self.attempts = attempts
        # self.version = version
        self.transcript_id = transcript_id
        self.principal_id = principal_id

    def __repr__(self):
        return "<QuizTaker {}>".format(self.login)