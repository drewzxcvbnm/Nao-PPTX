import pythoncom
import time


class MediaPresentation:

    def __init__(self, slidePresentor):
        self.slidePresentor = slidePresentor
        self.slidePresentor.ongoingEvents.append(self)

    def __call__(self, COMContext):
        ss = COMContext["slideshow"]
        sh = self._getMediaShape(ss.View.Slide)
        time.sleep(ss.View.Slide.SlideShowTransition.Duration)
        pl = ss.View.Player(sh.Id)

        pl.Play()
        while pl.State != 2:
            time.sleep(0.5)
        self.slidePresentor.ongoingEvents.remove(self)

    def _getMediaShape(self, slide):
        for s in slide.Shapes:
            if s.Type == 16:
                return s