import time

from services import atts
from comthreadeventexecutor import COMThreadEventExecutor
import qi
import pythoncom
from eventmap import eventmap
from translation.texttranslator import TextTranslationSystem
from events.surveyevent import SurveyEvent
from events.mediapresentationevent import MediaPresentationEvent


class SlidePresentor:

    def __init__(self, slide_show, pid):
        self.slideShow = slide_show
        self.ongoingEvents = []
        executor = COMThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slide_show))
        executor2 = COMThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slide_show))
        executor3 = COMThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slide_show))
        eventmap["next"] = lambda: executor.add_event_to_queue(self._next)
        eventmap["startmedia"] = lambda: executor2.add_event_to_queue(MediaPresentationEvent(self))
        eventmap["startsurvey"] = lambda sid: executor3.add_event_to_queue(SurveyEvent(self, sid, pid))

    def readSlide(self, slide):
        textNote = slide.notes_slide.notes_text_frame.text
        notes = textNote.encode('utf-8')
        print "Before translation:{}".format(str(notes))
        notes = TextTranslationSystem.translate(notes)
        print "After translation:{}".format(str(notes))
        for chunk in notes.split("<split/>"):
            say = qi.async(atts.say, (str(chunk)), delay=100)
            say.wait()
            self._waitForOngoingEventsToStop()

    def _waitForOngoingEventsToStop(self):
        while len(self.ongoingEvents) != 0:
            time.sleep(0.1)

    def _next(self, COMContext):
        ss = COMContext["slideshow"]
        ss.View.Next()

    def _startvideo(self):
        pass

    def __del__(self):
        eventmap.pop("next")
        eventmap.pop("startvideo")
