from services import atts, session

class SlideReader:

    def __init__(self, slideShow):
        self.slideShow = slideShow
        mem = session.service("ALMemory")
        sub = mem.subscriber("ALTextToSpeech/CurrentBookMark")
        sub.signal.connect(self._next())

    def readSlide(self, slide):
        textNote = slide.notes_slide.notes_text_frame.text
        notes = textNote.encode('utf-8')
        print str(notes)
        say = qi.async(atts.say, (str(notes)), delay=100)
        say.wait()

    def _next(self):
        def next(val):
            self.slideShow.View.Next()
        return next
