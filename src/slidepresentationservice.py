import time

import qi
from services import atts, mem
from events.event import Event
from translation.texttranslator import TextTranslationSystem
from events.surveyevent import SurveyEvent
from events.mediapresentationevent import MediaPresentationEvent
from events.behavioractionevent import BehaviorActionEvent


class SlidePresentationService:

    def __init__(self, presentation):
        mem.insertData('wait', 0)
        self.slide_show = presentation.com_slide_show
        self.translation_system = TextTranslationSystem(presentation)
        event_map = presentation.event_map
        event_map["next"] = Event("next", self._next, presentation, blocking=False)
        event_map["startmedia"] = Event("startmedia", MediaPresentationEvent(self.slide_show), presentation)
        event_map["startsurvey"] = Event("startsurvey", SurveyEvent(presentation), presentation)
        event_map["behaviour"] = Event("behaviour", BehaviorActionEvent(), presentation)

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

    def _next(self, ):
        ss = self.slide_show
        ss.View.Next()
