from naoxml.xmltag import XmlTag
from naoxml.xmltagvalidator import XmlTagValidator, XmlValidationException
import unittest


class TestXmlValidator(unittest.TestCase):

    def test_validation(self):
        txt = """<survey id="2">
	<pin>0A2X</pin>
	<type>auto</type>
	<questions>
		<question>
			<q>What is the first letter of the english alphabet?</q>
			<validoption>1</validoption>
			<options>
				<o>A</o>
				<o>B</o>
				<o>C</o>
			</options>
		</question>
		<question>
			<q>What is the second letter?</q>
			<timelimit>10</timelimit>
			<validoption>2</validoption>
			<options>
				<o>Z</o>
				<o>B</o>
				<o>O</o>
			</options>
		</question>
		<question>
			<q>What is the last letter?</q>
			<timelimit>50</timelimit>
			<validoption>1</validoption>
			<options>
			</options>
		</question>
	</questions>
</survey>"""

        with self.assertRaises(XmlValidationException) as cm:
            XmlTagValidator.validate(XmlTag(txt), ['type', 'questions.question.q', 'questions.question.options.o', ])
        self.assertEquals('[questions.question.options.o]: Tag options is missing field', cm.exception.message)

        XmlTagValidator.validate(XmlTag(txt), ['type', 'questions.question.q', 'questions.question.options', ])


if __name__ == '__main__':
    unittest.main()
