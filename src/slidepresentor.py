import time

from services import atts
from comthreadeventexecutor import COMThreadEventExecutor
import qi
import pythoncom
from eventmap import eventmap
from translation.texttranslator import TextTranslationSystem
from events.surveyevent import SurveyEvent
from events.mediapresentationevent import MediaPresentationEvent
from events.behavioractionevent import BehaviorActionEvent


class SlidePresentor:

    def __init__(self, slide_show, pid):
        self.slide_show = slide_show
        self.ongoing_events = []
        executor = COMThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slide_show))
        executor2 = COMThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slide_show))
        executor3 = COMThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slide_show))
        executor4 = COMThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slide_show))
        eventmap["next"] = lambda: executor.add_event_to_queue(self._next)
        eventmap["startmedia"] = lambda: executor2.add_event_to_queue(MediaPresentationEvent(self))
        eventmap["startsurvey"] = lambda sid: executor3.add_event_to_queue(SurveyEvent(self, sid, pid))
        eventmap["behavior"] = lambda name: executor4.add_event_to_queue(BehaviorActionEvent(self, name))

    def read_slide(self, slide):
        text_note = slide.notes_slide.notes_text_frame.text
        notes = text_note.encode('utf-8')
        print ("Before translation:{}".format(str(notes)))
        notes = TextTranslationSystem.translate(notes)
        print ("After translation:{}".format(str(notes)))
        for chunk in notes.split("<split/>"):
            say = qi.async(atts.say, (str(chunk)), delay=100)
            say.wait()
            self._wait_for_ongoing_events_to_stop()

    def _wait_for_ongoing_events_to_stop(self):
        while len(self.ongoing_events) != 0:
            time.sleep(0.1)

    def _next(self, com_context):
        ss = com_context["slideshow"]
        ss.View.Next()

    def _startvideo(self):
        pass  # empty init

    def __del__(self):
        eventmap.pop("next")
        eventmap.pop("startvideo")
