## Purpose

A small, object-oriented library for interacting with Adobe Connect
courses, meetings, users, and transcripts via the Adobe Connect API.

## Motivation

Adobe Connect's built-in reporting leaves something to be desired. This library allows you to get data out so you can build your own reports and do your own analysis.

## Getting Started

First, rename constants_sample.py to constants.py and move it into your Project's root directory. Then open it and replace all placeholders in curly brackets {}, including your Adobe Connect login credentials.

At the start of your script, create a new `Connect()` object. This will authenticate you via the API. Then you are ready to start making calls.

```python
from models.connect import Connect
from models.attendance import Attendance
from models.transcript import Transcript
from models.interaction import Interaction
from models.meeting import Meeting

Connect()  # authenticates with your Connect instance, now we're ready to make calls

# PRINT A LIST OF ATTENDANCES FOR A MEETING, AND THE TOTAL COMBINED DURATION
attendances = Attendance.fetch_by_meeting_sco_id(123456)
for attendance in attendances:
	print(attendance)
print(sum([attendance.duration_in_minutes() for attendance in attendances]))

# PRINT THE DATE AND STATUS OF EVERY TRANSCRIPT FOR A USER
transcripts = Transcript.fetch_by_principal_id(34567)
for transcript in transcripts:
	print(transcript.date_taken, transcript.login, transcript.status)

# PRINT EVERY ANSWER A USER GAVE TO EACH QUIZ OR SURVEY QUESTION ON A PARTICULAR TRANSCRIPT
interactions = transcripts[0].report_quiz_interactions()
for interaction in interactions:
	print(interaction.display_seq, interaction.description, interaction.response)

# GET A LIST OF ALL MEETINGS IN A PARTICULAR FOLDER IN CONNECT, THEN PRINT A LIST OF ATTENDEES
meetings = Meeting.fetch_by_folder_sco_id(56789)
for meeting in meetings:
    print(meeting.name, meeting.date_begin)
    for attendee in meeting.get_attendees(exclude_admins=False):
	print(attendee)
```

## Object Definitions

### Attendees vs. Attendances

An Attendance is created in Connect every time a user accesses a meeting. If a user got disconnected from a meeting and then rejoined, they are considered to have 2 Attendances.

That means if you wanted to tally up their total attendance time, you would need to find all of their Attendances for that meeting and get the combined sum.

An Attendee, on the other hand, is a unique person who joined the meeting (regardless of the number of times). But attendees are not exactly the same as Users:

### Attendees vs. Users

Users in this library correspond to registered users in the system, who have a principal-id and a login. However, not all Attendees correspond Users, because they could have attended a Meeting as a Guest, in which case they just enter their name upon joining the meeting, and do not have all the same information as a regular User.

## Syntax

In Adobe Connect, when XML parameters consist of more than one word, the words are typically separated with a dash. This doesn't work well as Python parameters, so when the XML is parsed, all dashes are converted to underscores. For example:

- `sco-id` becomes `sco_id`
- `display-seq` becomes `display_seq`
- `date-created` becomes `date_created`

and so on.

## Supported Actions

Designed to work with Adobe Connect 8 and later. Supported Adobe Connect actions currently include:

- common-info
- login
- report-user-training-transcripts
- report-quiz-interactions
- report-meeting-attendance
- sco-contents
- principal-list
- principal-info

See [Adobe's documentation](http://help.adobe.com/en_US/connect/8.0/webservices/WS26a970dc1da1c212717c4d5b12183254583-8000_SP1.html "Adobe Connect API Actions") about actions available in Adobe Connect.

## License

MIT
