from services import atts, tts, session, mem
import qi, win32com
from eventmanager import Eventloop, changedValuePredicate, Event
import pythoncom
from eventmap import eventmap
from translation.slidetranslator import SlideTranslationSystem

class SlideReader:

    def __init__(self, slideShow):
        self.slideShow = slideShow
        # mem.declareEvent("event")
        # self.subscriber = mem.subscriber("event")
        global eventmap
        gen = self._next()
        eventmap["next"] = lambda: next(gen) 
        self.ssID = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slideShow)

    def readSlide(self, slide):
        textNote = slide.notes_slide.notes_text_frame.text
        notes = textNote.encode('utf-8')
        print "Before translation:{}".format(str(notes))
        notes = SlideTranslationSystem.translate(notes)
        print "After translation:{}".format(str(notes))
        say = qi.async(atts.say, (str(notes)), delay=100)
        say.wait()
    
    def _next(self):
        mem.insertData("event", None)
        pythoncom.CoInitialize()
        ss = win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(self.ssID, pythoncom.IID_IDispatch))
        ss.View.Next()
        yield
        while True:
            mem.insertData("event", None)
            ss.View.Next()
            yield

    def __del__(self):
        global eventmap
        eventmap.pop("next")
