import constants
from connect import Connect
from module import Module

report = input('Which report: Summary, Assessment, or Survey? ').lower()

Connect()

if report == 'assessment' or report == 'survey':
    module_name = input('Which module? ').upper()
    after = input('Starting after what date (yyyy-mm-dd)? Or say "All Time" ').lower()
    if after != 'all time' and after != 'alltime':
        before = input('Ending before what date? (yyyy-mm-dd) ')
        module = Module(name=module_name, after=after, before=before)
    else:
        module = Module(name=module_name)

if report == 'assessment':
    module.get_assessments()
    module.get_assessment_answers()
    print('Your files were added to the "output" folder')
elif report == 'survey':
    module.get_learning_modules()
    module.get_learning_module_survey_answers()
    print('Your files were added to the "output" folder')
elif report == 'summary':
    for module_name in constants.MODULE_NAMES:
        module = Module(module_name)
        module.get_quiz_takers()
        if module_name == 'TE3' or module_name == 'PE3':
            print('{} Accessed Both Parts: {}'.format(module_name, module.quiz_passers_count))
        else:
            print('{} Passed: {}'.format(module_name, module.quiz_passers_count))
            print('{} In Progress: {}'.format(module_name, module.quiz_in_progress_count))


# after = '2016-09-01'
# before = '2016-09-10'