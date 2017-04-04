import urllib
from connect import Connect
from user import User
from datetime import date, timedelta, datetime


class Meeting:
    def __init__(self, name, date, scoid):
        self.name = name
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.scoid = scoid
        self.attendees = []

    def __repr__(self):
        return "<Meeting {} {}>".format(self.date, self.name)

    def get_attendees(self):
        filters = {
            'sco-id': self.scoid,
            'filter-gte-date-created': self.date.isoformat(),
            'filter-lt-date-created': (self.date + timedelta(1)).isoformat()
        }
        rows = Connect.send_request(action='report-meeting-attendance', **filters)
        users_to_exclude = ['xXxXxXxXxXx',
                            'crystal.conley@cecillinois.org',
                            'terri.carman@cecillinois.org'
                            ]
        for attendee in rows:
            if attendee.find('login').text not in [user.email for user in self.attendees] and \
                            attendee.find('login').text not in users_to_exclude:
                self.attendees.append(
                    User(
                        email=attendee.find('login').text,
                        first_name=attendee.find('participant-name').text,
                        last_name=attendee.find('participant-name').text,
                        date_created=attendee.find('date-created').text,
                        date_end=attendee.find('date-end').text
                    )
                )

        return self.attendees



        # with urllib.request.urlopen(
        #         '{}report-quiz-interactions&sco-id={}&filter-gte-date-created={}&filter-lt-date-created={}&session={}'.format(
        #             constants.CONNECT_BASE_URL,
        #             self.sco_id,
        #             self.after,
        #             self.before,
        #             Connect.cookie)) as response:
        #     xml = response.read().decode('utf-8')
        #
        # root = ET.fromstring(xml)
        # status = root.find('status').attrib['code']
        #
        # if status != 'ok':
        #     sys.exit('ERROR: "{}" RETRIEVING ANSWERS FOR SCO {}'.format(root.find('status').attrib['code'], self.sco_id))
        #
        # for interaction in root.findall('report-quiz-interactions/row'):
        #     user = interaction.find('name').text
        #     score = interaction.attrib['score']
        #     date = interaction.find('date-created').text
        #     interaction_id = interaction.attrib['interaction-id']
        #     transcript_id = interaction.attrib['transcript-id']
        #     display_seq = interaction.attrib['display-seq']
        #     question = None
        #     answer = None
        #
        #     if interaction.find('description') != None:
        #         # question = interaction.find('description').text.decode('utf-8')
        #         question = repr(interaction.find('description').text)
        #     if interaction.find('response') != None:
        #         answer = interaction.find('response').text
        #
        #     self.interactions.append(
        #         Interaction(user=user,
        #                     question=question,
        #                     answer=answer,
        #                     score=score,
        #                     date=date,
        #                     interaction_id=interaction_id,
        #                     transcript_id=transcript_id,
        #                     display_seq=display_seq))