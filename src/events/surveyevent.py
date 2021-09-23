import time

from survey.survey import surveys
from web.webinterface import WebInterface


class SurveyEvent:

    def __init__(self, slide_presentor, sid, pid):
        self.slide_presentor = slide_presentor
        self.slide_presentor.ongoing_events.append(self)
        self.sid = sid
        self.pid = pid

    def __call__(self, com_context):
        survey = surveys[self.sid]
        WebInterface.create_survey(survey, self.pid)
        WebInterface.open_survey(survey)
        st = WebInterface.get_survey_status(survey)
        while st.lower() != 'closed':
            time.sleep(3)
            st = WebInterface.get_survey_status(survey)
        self.slide_presentor.ongoing_events.remove(self)
