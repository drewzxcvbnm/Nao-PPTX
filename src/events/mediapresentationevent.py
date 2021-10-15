import time


class MediaPresentationEvent:

    def __init__(self, slide_show):
        self.ss = slide_show

    def __call__(self):
        ss = self.ss
        sh = self._get_media_shape(ss.View.Slide)
        time.sleep(ss.View.Slide.SlideShowTransition.Duration)
        pl = ss.View.Player(sh.Id)

        pl.Play()
        while pl.State != 2:
            time.sleep(0.5)

    def _get_media_shape(self, slide):
        for s in slide.Shapes:
            if s.Type == 16:
                return s
