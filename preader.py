import win32com.client as win32
from eventmanager import *
from pptx import Presentation
import time
from services import atts, tts, touch, motion
import qi
from sreader import SlideReader
langs = {
    "rus" : "Alyona22Enhanced",
    "eng" : "naoenu"
}

class PresentationReader:

    def __init__(self, path, lang = "eng"):
        self.stop = False
        tts.setVoice(langs[lang])
        self.path = path
        self.ppoint = win32.gencache.EnsureDispatch('Powerpoint.Application')
        self.ppoint.Visible = True
        self.presentation = self.ppoint.Presentations.Open(path)
        # self.presentation.SlideShowSettings.ShowWithAnimation = False
        self.slideShow = self.presentation.SlideShowSettings.Run()
        self.eventHandler = Eventloop()
        self.eventHandler.addEvent(Event(self._stop, [], binaryPredicate(lambda: touch.getStatus()[8][1], False, True)))
        self.eventHandler.addEvent(Event(self._nextSlide, [], binaryPredicate(lambda: touch.getStatus()[7][1], False, True)))
        self.eventHandler.addEvent(Event(self._prevSlide, [], binaryPredicate(lambda: touch.getStatus()[9][1], False, True)))
        self.slideReader = SlideReader(self.slideShow)

    def readSlides(self):
        self.ppt=Presentation(self.path)
        self.iSlide = 0
        self.eventHandler.start()
        while self.iSlide < len(self.ppt.slides):
            if self.stop:
                break
            self.slideShow.View.GotoSlide(self.iSlide + 1)
            self.slideReader.readSlide(self.ppt.slides[self.iSlide])
            self.iSlide += 1
            time.sleep(1)

    def close(self):
        self.eventHandler.stop()
        self.presentation.Close()
        self.ppoint.Quit()
        self.eventHandler.join()

    def _stop(self):
        self.stop = True
        tts.stopAll()
   
    def _nextSlide(self):
        global tts
        tts.stopAll()

    def _prevSlide(self):
        global tts
        self.iSlide -= 2
        tts.stopAll()
