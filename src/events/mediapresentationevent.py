import pythoncom
import time


class MediaPresentationEvent:

    def __init__(self, slide_presentor):
        self.slide_presentor = slide_presentor
        self.slide_presentor.ongoing_events.append(self)

    def __call__(self, com_context):
        ss = com_context["slideshow"]
        sh = self._get_media_shape(ss.View.Slide)
        time.sleep(ss.View.Slide.SlideShowTransition.Duration)
        pl = ss.View.Player(sh.Id)

        pl.Play()
        while pl.State != 2:
            time.sleep(0.5)
        self.slide_presentor.ongoing_events.remove(self)

    def _get_media_shape(self, slide):
        for s in slide.Shapes:
            if s.Type == 16:
                return s
