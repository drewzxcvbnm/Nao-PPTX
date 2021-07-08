from services import atts, tts, session, mem
import qi, win32com
from eventmanager import Eventloop, changedValuePredicate, Event
import pythoncom
from eventmap import eventmap

class SlideReader:

    def __init__(self, slideShow):
        self.slideShow = slideShow
        # mem.declareEvent("event")
        # self.subscriber = mem.subscriber("event")
        global eventmap
        gen = self._next()
        eventmap["next"] = lambda: next(gen) 
        # self.disconnect = self.subscriber.signal.connect(lambda x: eventmap[x]())
        # self.evm = Eventloop()
        self.ssID = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, slideShow)
        # gen = self._next()
        # self.evm.addEvent(Event(lambda: next(gen), [], lambda: mem.getData("event") == "next"))
        # self.evm.start()

    def readSlide(self, slide):
        textNote = slide.notes_slide.notes_text_frame.text
        notes = textNote.encode('utf-8')
        print str(notes)
        say = qi.async(atts.say, (str(notes)), delay=100)
        say.wait()
        print "DATA: "+str(mem.getData("event")) + "|"
    
    # def fun(self, x):
    #     x()
    #     return True
        
    def _next(self):
        print "NEEEXT"
        mem.insertData("event", None)
        pythoncom.CoInitialize()
        ss = win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(self.ssID, pythoncom.IID_IDispatch))
        ss.View.Next()
        yield
        while True:
            print "NEEEXT"
            mem.insertData("event", None)
            ss.View.Next()
            yield

    # def __del__(self):
    #     self.subscriber.signal.disconnect(self.disconnect)