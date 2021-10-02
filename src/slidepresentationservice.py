import time

import qi
import pythoncom
from services import atts, mem
from events.event import Event
from translation.texttranslator import TextTranslationSystem
from events.surveyevent import SurveyEvent
from events.mediapresentationevent import MediaPresentationEvent
from events.behavioractionevent import BehaviorActionEvent


class SlidePresentationService:

    def __init__(self, presentation):
        self.slide_show = presentation.com_slide_show
        self.translation_system = TextTranslationSystem(presentation)
        com_context = {'slideshow': self.slide_show}
        event_map = presentation.event_map
        event_map["next"] = Event("next", self._next, presentation, com_context, blocking=False)
        event_map["startmedia"] = Event("startmedia", MediaPresentationEvent(), presentation, com_context)
        event_map["startsurvey"] = Event("startsurvey", SurveyEvent(presentation), presentation, com_context)
        event_map["behaviour"] = Event("behaviour", BehaviorActionEvent(), presentation, com_context)

    def read_slide(self, slide):
        text_note = slide.notes_slide.notes_text_frame.text
        notes = text_note.encode('utf-8')
        print("Before translation:{}".format(str(notes)))
        notes = self.translation_system.translate(notes)
        print("After translation:{}".format(str(notes)))
        for chunk in notes.split("<split/>"):
            say = qi.async(atts.say, (str(chunk)), delay=100)
            say.wait()
            self._wait_for_ongoing_events_to_stop()

    def _wait_for_ongoing_events_to_stop(self):
        while mem.getData('wait') != 0:
            time.sleep(0.1)

    def _next(self, com_context):
        ss = com_context["slideshow"]
        ss.View.Next()
