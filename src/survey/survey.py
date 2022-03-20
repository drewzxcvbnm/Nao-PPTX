from naoxml.xmltagvalidator import XmlTagValidator

# local id -> Survey Object
# surveys = {}


class Survey:
    mandatory_fields = ['type', 'questions.question.q', 'questions.question.options.o', ]

    def __init__(self, survey_xmltag):
        XmlTagValidator.validate(survey_xmltag, self.mandatory_fields)
        self.remote_id = None
        self.local_sid = survey_xmltag.attributes['id']
        self.type = survey_xmltag.get_child_tag_content('type')
        self.pin = survey_xmltag.get_child_tag_content('pin')
        self.questions = self._questions(survey_xmltag.get_child_tag('questions'))

    @staticmethod
    def _questions(questions_tag):
        questions = []
        for ques in questions_tag.get_child_tag_list('question'):
            options = [op.content for op in ques.get_child_tag('options').get_child_tag('o')]
            question = {"question": ques.get_child_tag_content('q'), "options": options}
            question['validoptions'] = []
            valid_options = ques.get_child_tag("validoptions")
            if valid_options is not None:
                for valid_opt in valid_options.get_child_tag_list('validoption'):
                    question['validoptions'].append(int(valid_opt.content))
            questions.append(question)
        return questions
