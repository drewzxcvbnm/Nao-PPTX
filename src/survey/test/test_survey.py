from naoxml.xmltag import XmlTag
from ..survey import Survey
import unittest


class TestSurvey(unittest.TestCase):

    def test_survey(self):
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
				<q>What is the Last letter?</q>
				<timelimit>50</timelimit>
				<validoption>1</validoption>
				<options>
					<o>Z</o>
					<o>B</o>
					<o>O</o>
				</options>
			</question>
		</questions>
	</survey>
"""

        result = Survey(XmlTag(txt))

        self.assertEquals(result.type, "auto")
        self.assertEquals(result.pin, "0A2X")
        self.assertEquals(result.remote_id, None)
        self.assertEquals(result.questions, [
            {'question': 'What is the first letter of the english alphabet?', 'options': ['A', 'B', 'C'], 'validOption': '1'},
            {'question': 'What is the second letter?', 'options': ['Z', 'B', 'O'], 'validOption': '2'},
            {'question': 'What is the Last letter?', 'options': ['Z', 'B', 'O'], 'validOption': '1'}])
        self.assertEquals(result.local_sid, "2")


if __name__ == '__main__':
    unittest.main()
