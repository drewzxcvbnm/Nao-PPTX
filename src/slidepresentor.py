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

    def read_slide(self, slide):
        text_note = slide.notes_slide.notes_text_frame.text
        notes = text_note.encode('utf-8')
        print "Before translation:{}".format(str(notes))
        notes = TextTranslationSystem.translate(notes)
        print "After translation:{}".format(str(notes))
        for chunk in notes.split("<split/>"):
            say = qi.async(atts.say, (str(chunk)), delay=100)
            say.wait()
            self._wait_for_ongoing_events_to_stop()

    def _wait_for_ongoing_events_to_stop(self):
        while len(self.ongoingEvents) != 0:
            time.sleep(0.1)

    def _next(self, com_context):
        ss = com_context["slideshow"]
        ss.View.Next()

    def _startvideo(self):
        pass

    def __del__(self):
        eventmap.pop("next")
        eventmap.pop("startvideo")
