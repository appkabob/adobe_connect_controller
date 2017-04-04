from connect import Connect
from course import Course

Connect()
course = Course('TE 3', 3489311, '2017-01-01', '2017-03-06')
course.report_user_training_transcripts()
print(course.transcripts)
course.save_to_csv()
