from adobe_connect_controller.src.models.connect import Connect
from adobe_connect_controller.src.models.course import Course
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

Connect()
course = Course('Variable Test', 67862271, '2016-12-01', '2017-01-01')
course.report_quiz_interactions()
course.save_to_csv()

# doc = SimpleDocTemplate("output/ex.pdf",pagesize=letter,
#                         rightMargin=72,leftMargin=72,
#                         topMargin=72,bottomMargin=18)
#
# Story=[]
# styles=getSampleStyleSheet()
# styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
# for interaction in course.interactions:
#     ptext = '<font size=12>%s:</font>' % interaction.answer
#     Story.append(Paragraph(ptext, styles["Normal"]))
#     Story.append(Spacer(1, 12))
# doc.build(Story)

# doc = SimpleDocTemplate("output/ex.pdf",pagesize=letter,
#                         rightMargin=72,leftMargin=72,
#                         topMargin=72,bottomMargin=18)
#
# Story=[]
#
# formatted_time = '2016-12-14'
# full_name = "Mike Driscoll"
# address_parts = ["411 State St.", "Marshalltown, IA 50158"]
# magName = 'CEC Magazine'
# issueNum = '1'
# subPrice = '$10'
# limitedDate = '2016-12-01'
# freeGift = 'My Free Gift'
#
# styles=getSampleStyleSheet()
# styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
# ptext = '<font size=12>%s</font>' % formatted_time
# Story.append(Paragraph(ptext, styles["Normal"]))
# Story.append(Spacer(1, 12))
#
# ptext = '<font size=12>%s</font>' % full_name
# Story.append(Paragraph(ptext, styles["Normal"]))
# for part in address_parts:
#     ptext = '<font size=12>%s</font>' % part.strip()
#     Story.append(Paragraph(ptext, styles["Normal"]))
#
# Story.append(Spacer(1, 12))
# ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
# Story.append(Paragraph(ptext, styles["Normal"]))
# Story.append(Spacer(1, 12))
#
# ptext = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine! \
#         You will receive %s issues at the excellent introductory price of $%s. Please respond by\
#         %s to start receiving your subscription and get the following free gift: %s.</font>' % (magName,
#                                                                                                 issueNum,
#                                                                                                 subPrice,
#                                                                                                 limitedDate,
#                                                                                                 freeGift)
# Story.append(Paragraph(ptext, styles["Justify"]))
# Story.append(Spacer(1, 12))
#
# ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
# Story.append(Paragraph(ptext, styles["Justify"]))
# Story.append(Spacer(1, 12))
# ptext = '<font size=12>Sincerely,</font>'
# Story.append(Paragraph(ptext, styles["Normal"]))
# Story.append(Spacer(1, 48))
# ptext = '<font size=12>Ima Sucker</font>'
# Story.append(Paragraph(ptext, styles["Normal"]))
# Story.append(Spacer(1, 12))
# doc.build(Story)