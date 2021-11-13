from services import behman


class BehaviorActionEvent:

    def __call__(self, name):
        print("start_custom_behavior ", name)
        try:
            behman.runBehavior(name)
        except RuntimeError as err:
            print ("Behaviour error. Aborting")
            print (err)
        print("end_custom_behavior", name)
