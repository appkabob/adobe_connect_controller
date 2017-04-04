import os

import constants
from .src.models.connect import Connect
from .src.models.module import Module
from .src.models.user import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import shutil


def waitForLoad(inputXPath, PATIENCE_TIME):
    Wait = WebDriverWait(browser, PATIENCE_TIME)
    Wait.until(EC.presence_of_element_located((By.XPATH, inputXPath)))

baseurl1 = "http://www.growththroughlearningillinois.org/Home/tabid/160/ctl/Login/Default.aspx"
baseurl2 = "http://www.growththroughlearningillinois.org/Admin/UserImportExportModule.aspx"
username = "xXxXxXxXxXx"
password = "xXxXxXxXxXx"

xpaths = { 'usernameTxtBox' : "//input[@name='dnn$ctr$Login$Login_DNN$txtUsername']",
           'passwordTxtBox' : "//input[@name='dnn$ctr$Login$Login_DNN$txtPassword']",
           'submitButton' :   "//a[@id='dnn_ctr_Login_Login_DNN_cmdLogin']"
         }

browser = webdriver.Firefox()
browser.get(baseurl1)
browser.maximize_window()

#Write Username in Username TextBox
browser.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(username)
#Write Password in password TextBox
browser.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)
#Click Login button
browser.find_element_by_xpath(xpaths['submitButton']).click()

waitForLoad("//div[@id='RibbonBar_adminMenus']", 10)

browser.get(baseurl2)

waitForLoad("//a[@id='dnn_ctr559_UserExport_cmdExport']", 10)

cbFields = [0,2,3,5,6,7,8,13,14,15,17,18,29,30,31,32,33,34,35,36,37,38,39,40,41,42]
cbRoles = [1,2,3,4,7,8,10,11]

for field_id in cbFields:
    browser.find_element_by_id('dnn_ctr559_UserExport_cbFields_{}'.format(field_id)).click()
for field_id in cbRoles:
    browser.find_element_by_id('dnn_ctr559_UserExport_cbRoles_{}'.format(field_id)).click()

browser.find_element_by_id('dnn_ctr559_UserExport_txtDel').clear()
browser.find_element_by_id('dnn_ctr559_UserExport_txtDel').send_keys('#@@#')

browser.find_element_by_id('dnn_ctr559_UserExport_cmdExport').click()

waitForLoad("//span[@id='dnn_ctr559_ctl01_lblMessage']", 120)

download_link = browser.find_element_by_xpath("//a[text()='here']").get_attribute("href")

print(download_link)

browser.close()

output_loc = './output/gtl_full_user_list.txt'

# response = urllib.request.urlopen(download_link)
with urllib.request.urlopen(download_link) as response, open(output_loc, 'wb') as out_file:
    response.info().get_param('charset', 'utf-8')
    shutil.copyfileobj(response, out_file)

newfile = './output/gtl_full_user_list.tsv'

with open(newfile, 'w') as outfile, open(output_loc, 'r', encoding='latin-1') as infile:
    for line in infile:
        line = line.replace("\t", "")
        line = line.replace("#@@#", "\t")
        # line = line.encode('utf-8').strip()
        outfile.write(line)

os.remove(output_loc)

# report = input('Which report: Summary, Assessment, or Survey? ').lower()
#
# Connect()
#
# if report == 'assessment' or report == 'survey':
#     module_name = input('Which module? ').upper()
#     after = input('Starting after what date (yyyy-mm-dd)? Or say "All Time" ').lower()
#     if after != 'all time' and after != 'alltime':
#         before = input('Ending before what date? (yyyy-mm-dd) ')
#         module = Module(name=module_name, after=after, before=before)
#     else:
#         module = Module(name=module_name)
#
# if report == 'assessment':
#     module.get_assessments()
#     module.get_assessment_answers()
#     print('Your files were added to the "output" folder')
# elif report == 'survey':
#     module.get_learning_modules()
#     module.get_learning_module_survey_answers()
#     print('Your files were added to the "output" folder')
# elif report == 'summary':
#     for module_name in constants.MODULE_NAMES:
#         module = Module(module_name)
#         module.get_quiz_takers()
#         if module_name == 'TE3' or module_name == 'PE3':
#             print('{} Accessed Both Parts: {}'.format(module_name, module.quiz_passers_count))
#         else:
#             print('{} Passed: {}'.format(module_name, module.quiz_passers_count))
#             print('{} In Progress: {}'.format(module_name, module.quiz_in_progress_count))


# after = '2016-09-01'
# before = '2016-09-10'