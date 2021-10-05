import time

from web.webinterface import WebInterface


class SurveyEvent:

    def __init__(self, presentation):
        self.pid = presentation.presentation_id
        self.surveys = presentation.surveys

    def __call__(self, com_context, sid):
        survey = self.surveys[sid]
        WebInterface.create_survey(survey, self.pid)
        WebInterface.open_survey(survey)
        st = WebInterface.get_survey_status(survey)
        while st.lower() != 'closed':
            time.sleep(3)
            st = WebInterface.get_survey_status(survey)
