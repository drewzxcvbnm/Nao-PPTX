# coding=utf-8
from ..texttranslator import TextTranslationSystem
import unittest


class TestTranslator(unittest.TestCase):

    def test_translation(self):
        txt = """
So, how do I work? <do animation="/test/anim"> It’s <do animation="/another/test"> quite </do> simple, 
</do> I have a head <pause time="200"/> and a computer inside of it.
This computer works like a human brain, but with a lot of limitations and a lack of conscience,
and I am only capable of doing what was programmed into me and <pause time="150"/>  nothing more. So unfortunately <pause time="100"/> I can’t
conquer the world without human approval, <emph word="for" pos="2"/> now <pause time="150"/> that is.
<video> The Era of machines is upon <tt/> us Humans! </video> Now gettings back to the topic at hand!
"""
        result = TextTranslationSystem.translate(txt)
        expected = """
So, how do I work? ^start(/test/anim) It’s ^start(/another/test) quite ^wait(/another/test) simple, 
 ^wait(/test/anim) I have a head \pau=200\ and a computer inside of it.
This computer works like a human brain, but with a lot of limitations and a lack of conscience,
and I am only capable of doing what was programmed into me and \pau=150\ nothing more. So unfortunately \pau=100\ I can’t
conquer the world without human approval, \emph=2\ for now \pau=150\ that is.
 $event=startmedia The Era of machines is upon <tt/> us Humans! <split/> Now gettings back to the topic at hand!
"""
        self.assertEquals(result, expected)


if __name__ == '__main__':
    unittest.main()