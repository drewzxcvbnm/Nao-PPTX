import time

from survey.survey import surveys
from web.webinterface import WebInterface


class SurveyEvent:

    def __init__(self, pid):
        self.pid = pid

    def __call__(self, com_context, sid):
        survey = surveys[sid]
        WebInterface.create_survey(survey, self.pid)
        WebInterface.open_survey(survey)
        st = WebInterface.get_survey_status(survey)
        while st.lower() != 'closed':
            time.sleep(3)
            st = WebInterface.get_survey_status(survey)
