import time

from services import atts, tts, session, mem
from threadeventexecutor import ThreadEventExecutor
import qi, win32com
import pythoncom
from eventmap import eventmap
from translation.texttranslator import TextTranslationSystem
from mediapresentation import MediaPresentation


class SlidePresentor:

    def __init__(self, slideShow):
        self.slideShow = slideShow
        self.ongoingEvents = []
        executor = ThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slideShow))
        executor2 = ThreadEventExecutor(
            slideshow=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slideShow))
        eventmap["next"] = lambda: executor.addEventToQueue(self._next)
        eventmap["startmedia"] = lambda: executor2.addEventToQueue(MediaPresentation(self))

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
