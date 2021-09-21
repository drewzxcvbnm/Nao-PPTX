from services import behman


class BehaviorActionEvent:
    def __init__(self, slide_presentor, name):
        self.slide_presentor = slide_presentor
        self.slide_presentor.ongoing_events.append(self)
        self.name = name

    def __call__(self, *args, **kwargs):
        print ("start_custom_behavior")
        behman.runBehavior(self.name)
        print ("end_custom_behavior")
        self.slide_presentor.ongoing_events.remove(self)
