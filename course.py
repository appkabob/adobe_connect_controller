import constants
import urllib.request
import xml.etree.ElementTree as ET
import sys
from connect import Connect
from interaction import Interaction
from quiz_taker import QuizTaker
import csv

class Course:
    def __init__(self, name, sco_id, after, before):
        self.name = name
        self.sco_id = sco_id
        self.after = after
        self.before = before
        self.interactions = []
        self.quiz_takers = []

        # self.report_quiz_interactions()

    def __repr__(self):
        return "<Course {}>".format(self.name)

    # @classmethod
    # def load_from_connect_by_sco_id(cls, name):
    #
    #     sco_id = constants.module_scos[name]
    #
    #     return cls(name=name, sco_id=sco_id)

    def report_quiz_interactions(self):
        with urllib.request.urlopen(
                '{}report-quiz-interactions&sco-id={}&filter-gte-date-created={}&filter-lt-date-created={}&session={}'.format(
                    constants.CONNECT_BASE_URL,
                    self.sco_id,
                    self.after,
                    self.before,
                    Connect.cookie)) as response:
            xml = response.read().decode('utf-8')

        root = ET.fromstring(xml)
        status = root.find('status').attrib['code']

        if status != 'ok':
            sys.exit('ERROR: "{}" RETRIEVING ANSWERS FOR SCO {}'.format(root.find('status').attrib['code'], self.sco_id))

        for interaction in root.findall('report-quiz-interactions/row'):
            user = interaction.find('name').text
            score = interaction.attrib['score']
            date = interaction.find('date-created').text
            interaction_id = interaction.attrib['interaction-id']
            transcript_id = interaction.attrib['transcript-id']
            display_seq = interaction.attrib['display-seq']
            question = None
            answer = None

            if interaction.find('description') != None:
                # question = interaction.find('description').text.decode('utf-8')
                question = repr(interaction.find('description').text)
            if interaction.find('response') != None:
                answer = interaction.find('response').text

            self.interactions.append(
                Interaction(user=user,
                            question=question,
                            answer=answer,
                            score=score,
                            date=date,
                            interaction_id=interaction_id,
                            transcript_id=transcript_id,
                            display_seq=display_seq))

    def save_to_csv(self):
        with open('./output/{}_raw_answers_{}_{}.csv'.format(self.name, self.after, self.before), 'w', newline="\n") as f:
            a = csv.writer(f, delimiter=",")
            a.writerow(['Date', 'Interaction ID', 'User', 'Display Seq', 'Question', 'Answer', 'Score'])
            for interaction in self.interactions:
                a.writerow([interaction.date,
                            interaction.interaction_id,
                            interaction.user,
                            interaction.display_seq,
                            interaction.question,
                            interaction.answer,
                            interaction.score])

    def get_quiz_takers(self):
        with urllib.request.urlopen(
                '{}report-quiz-takers&sco-id={}&session={}'.format(
                    constants.CONNECT_BASE_URL,
                    self.sco_id,
                    Connect.cookie)) as response:
            xml = response.read()

        root = ET.fromstring(xml)
        status = root.find('status').attrib['code']

        if status != 'ok':
            sys.exit('ERROR RETRIEVING USERS FOR SCO {}'.format(self.sco_id))

        for quiz_taker in root.findall('report-quiz-takers/row'):
            if quiz_taker.find('login').text.split('@')[1] not in constants.USERS_TO_EXCLUDE_FROM_TOTALS:
                self.quiz_takers.append(
                    QuizTaker(user=quiz_taker.find('principal-name').text,
                              login=quiz_taker.find('login').text,
                              status=quiz_taker.attrib['status'],
                              date=quiz_taker.find('date-created').text,
                              transcript_id=quiz_taker.attrib['transcript-id'],
                              principal_id=quiz_taker.attrib['principal-id']
                              )
                )