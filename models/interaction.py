class Interaction:
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self):
        return '<Interaction {}>'.format(self.interaction_id)



# class Interaction:
#     def __init__(self, user, question, answer, score, date, transcript_id, interaction_id, display_seq):
#         self.user = user
#         self.question = question
#         self.answer = answer
#         self.score = score
#         self.date = date
#         self.transcript_id = transcript_id
#         self.interaction_id = interaction_id
#         self.display_seq = display_seq
#
#     def __repr__(self):
#         return "<Interaction {}>".format(self.interaction_id)