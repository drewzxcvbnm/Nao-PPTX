from services import behman


class BehaviorActionEvent:

    def __call__(self, name):
        print("start_custom_behavior ", name)
        behman.runBehavior(name)
        print("end_custom_behavior", name)
