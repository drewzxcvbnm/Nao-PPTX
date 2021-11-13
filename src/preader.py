import sys
import threading
from eventmanager import Eventloop, Event, binaryPredicate
import time
from services import tts, touch
from slidepresentationservice import SlidePresentationService

langs = {
    "rus": "Alyona22Enhanced",
    "eng": "naoenu"
}


class PresentationReadingService:

    def __init__(self, lang="eng"):
        self.lock = threading.Lock()
        self.stop = False
        self.slide_reader = None
        tts.setVoice(langs[lang])
        self.event_handler = Eventloop()
        self.event_handler.addEvent(
            Event(self._pause, [], binaryPredicate(lambda: touch.getStatus()[8][1], False, True)))
        self.event_handler.addEvent(
            Event(self._next_slide, [], binaryPredicate(lambda: touch.getStatus()[7][1], False, True)))
        self.event_handler.addEvent(
            Event(self._prev_slide, [], binaryPredicate(lambda: touch.getStatus()[9][1], False, True)))

    def read_presentation(self, presentation):
        self.slide_reader = SlidePresentationService(presentation)
        presentation.com_ppoint.Visible = True
        self.i_slide = 0
        self.event_handler.start()
        while self.i_slide < len(presentation.slides):
            if self.stop:
                break
            self.lock.acquire()
            presentation.com_slide_show.View.GotoSlide(self.i_slide + 1)
            self.slide_reader.read_slide(presentation.slides[self.i_slide])
            self.i_slide += 1
            self.lock.release()
            time.sleep(1)

    def __del__(self):
        self.i_slide = sys.maxint
        self.slide_reader.__del__()
        self.event_handler.stop()
        self.event_handler.join()

    def _pause(self):
        print("pause")
        tts.stopAll()
        self.lock.acquire()
        while not touch.getStatus()[8][1]:
            time.sleep(0.1)
        print("resume")
        self.lock.release()
        time.sleep(1)

    def _stop(self):
        self.stop = True
        tts.stopAll()

    def _next_slide(self):
        tts.stopAll()

    def _prev_slide(self):
        self.i_slide -= 2
        tts.stopAll()
