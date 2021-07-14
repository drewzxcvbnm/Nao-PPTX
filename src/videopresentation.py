import pythoncom
import time


class VideoPresentation:

    def __init__(self, slidePresentor):
        self.slidePresentor = slidePresentor
        self.slidePresentor.ongoingEvents.append(self)

    def __call__(self, COMContext):
        ss = COMContext["slideshow"]
        pl = ss.View.Player(self._getVideoShape(ss.View.Slide))
        pl.Play()
        while pl.State == 0:
            time.sleep(0.5)
        self.slidePresentor.ongoingEvents.remove(self)

    def _getVideoShape(self, slide):
        for s in slide.Shapes:
            if s.Type == 16:
                return s
