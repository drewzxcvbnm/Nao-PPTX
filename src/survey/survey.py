from naoxml.xmltagvalidator import XmlTagValidator

# id -> Survey Object
surveys = {}


class Survey:
    mandatory_fields = ['type', 'questions.q', 'questions.options.o', ]

    def __init__(self, survey_xmltag):
        XmlTagValidator.validate(survey_xmltag, self.mandatory_fields)
        self.type = survey_xmltag.get_child_tag_content('type')
        self.pin = survey_xmltag.get_child_tag_content('pin')
        self.questions = self._questions(survey_xmltag.get_child_tag('questions'))

    def _questions(self, questions_tag):
        questions = []
        for ques in questions_tag.get_child_tag('question'):
            options = [op.get_child_tag_content('o') for op in ques.get_child_tag('options').get_child_tag('option')]
            question = {"question": ques.get_child_tag_content('q'), "options": options}
            if ques.get_child_tag_content('validoption') is not None:
                question['validOption'] = ques.get_child_tag_content('validOption')
            questions.append(question)
        return questions
