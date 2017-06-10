try:
    import constants
except ImportError:
    pass
from datetime import datetime
from .course import Course

class Module:
    def __init__(self, name, after='2012-01-01', before=datetime.today().strftime("%Y-%m-%d")):

        self.after = after
        self.before = before

        self.name = name
        self.learning_modules = []
        self.assessments = []
        self.quiz_takers = {}
        self.quiz_passers_count = 0
        self.quiz_in_progress_count = 0

        self.get_learning_modules()
        self.get_assessments()

    def __repr__(self):
        return "<Module {}>".format(self.name)

    def get_learning_modules(self):
        for i in constants.LEARNING_MODULE_SCOS[self.name]:
            sco_id = constants.LEARNING_MODULE_SCOS[self.name][str(i)]
            self.learning_modules.append(Course(name='{}p{}'.format(self.name, i),
                                                sco_id=sco_id,
                                                after=self.after,
                                                before=self.before))

    def get_assessments(self):
        if self.name != 'TE3' and self.name != 'PE3':
            for letter in constants.ASSESSMENT_SCOS[self.name]:
                sco_id = constants.ASSESSMENT_SCOS[self.name][letter]
                self.assessments.append(Course(name='{}{}'.format(self.name, letter),
                                               sco_id=sco_id,
                                               after=self.after,
                                               before=self.before))

    def get_learning_module_survey_answers(self):
        for course in self.learning_modules:
            course.report_quiz_interactions()
            course.save_to_csv()

    def get_assessment_answers(self):
        for course in self.assessments:
            course.report_quiz_interactions()
            course.save_to_csv()

    def get_quiz_takers(self):
        if self.name == 'TE3' or self.name == 'PE3':
            for course in self.learning_modules:
                course.get_quiz_takers()
                for quiz_taker in course.quiz_takers:
                    if quiz_taker.login in self.quiz_takers:
                        self.quiz_passers_count += 1
                    self.quiz_takers[quiz_taker.login] = quiz_taker
        else:
            # self.quiz_takers = {}
            # quiz_passers = 0
            # quiz_in_progress = 0
            for course in self.assessments:
                course.get_quiz_takers()

                for quiz_taker in course.quiz_takers:

                    if quiz_taker.login in self.quiz_takers: # IF WE'VE SEEN THIS USER BEFORE
                        if quiz_taker.status == 'user-passed' and self.quiz_takers[quiz_taker.login].status != 'user-passed':
                            self.quiz_takers[quiz_taker.login] = quiz_taker
                            self.quiz_passers_count += 1

                    else: # IF WE HAVE NOT SEEN THIS USER BEFORE
                        self.quiz_takers[quiz_taker.login] = quiz_taker
                        if quiz_taker.status == 'user-passed':
                            self.quiz_passers_count += 1
                        else:
                            self.quiz_in_progress_count += 1
            self.quiz_in_progress_count = len(self.quiz_takers) - self.quiz_passers_count
            # print(len(self.quiz_takers))
            # print(self.quiz_passers_count)
            # print(self.quiz_in_progress_count)