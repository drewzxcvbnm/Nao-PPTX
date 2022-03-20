# ver 1.1.3
import time
from threading import Thread

def selfloop(f):
    def decorator(self):
        while self.loop:
            f(self)
            time.sleep(self.sleep_time)
    return decorator

def getPhraseGenerator(randomphrasesupplier):
    old = [""]
    def phraseGenerator():
        new = randomphrasesupplier()
        while old[0] == new:
            new = randomphrasesupplier()
        old[0] = new
        return new
    return phraseGenerator


def binaryPredicate(getstate, zeroToOne = False, oneToZero = False):
    old_state = [getstate()]
    def predicate():
        new_state = getstate()
        ret = (zeroToOne and old_state[0] == 0 and new_state == 1) or (oneToZero and old_state[0] == 1 and new_state == 0)
        if new_state != old_state[0]:
            old_state[0] = new_state
        return ret
    return predicate

def changedValuePredicate(valuesupplier):
    old = [-1]
    def pred():
        new = valuesupplier()
        if new == old[0]:
            return False
        old[0] = new
        return new > 0.5
    return pred

class Event:
    def __init__(self, function, args = [], predicate = lambda: False,  single_use = False, threadable = False, cooldown = 0):
        self.predicate = predicate
        self.function = function
        self.args = args
        self.single_use = single_use
        self.threadable = threadable
        self.started_on_thread = False 
        self.cooldown = cooldown
        self.cooldown_deadline = time.time() + cooldown
        self.event_group = []


class EventGroup:
    def __init__(self, predicate = lambda: True, cooldown = 0):
        self.events = []
        self.predicate = predicate
        self.cooldown = cooldown
        self.cooldown_deadline = time.time() + cooldown

    def addEvent(self, event):
        event.event_group = self
        self.events.append(event)

class Eventloop:

    def __init__(self, sleep_time = 0.05):
        self.generalGroup = EventGroup()
        self.event_groups = [self.generalGroup]
        self.sleep_time = sleep_time
        self.threads = []

    @selfloop
    def _checkEventGroups(self):
        [self._dispatchEventGroup(eg) for eg in self.event_groups if eg.predicate() and eg.cooldown_deadline <= time.time()]

    def _dispatchEventGroup(self, event_group):
        if [self._dispatchEvent(e) for e in event_group.events if not e.started_on_thread and e.predicate() and e.cooldown_deadline <= time.time()]:
            self._updateCooldown(event_group)

    def _dispatchEvent(self, event):
        self._updateCooldown(event)
        if not event.threadable:
            self._startFunction(event)
            return
        self._startFunctionOnThread(event)
        
    def _updateCooldown(self, item):
        item.cooldown_deadline = time.time() + item.cooldown

    @selfloop
    def _checkThreadStatus(self):
        if len(self.threads)>100:
            self.stop()
            raise Exception("logical error, to much threads >100") 
        for t in [t for t in self.threads]:
            if not t.is_alive():
                t.event.started_on_thread = False
                self.threads.remove(t)

    def _startFunction(self, event):
        event.function(*event.args)
        if event.single_use == False:
            return
        event.event_group.events.remove(event)

    def _startFunctionOnThread(self, event):
        t = Thread(target=event.function, args=event.args)
        t.start()
        if event.single_use:
            event.event_group.events.remove(event)
            return
        t.event = event
        self.threads.append(t)
        event.started_on_thread = True

    def addEvent(self, event):
        self.generalGroup.addEvent(event)

    def addEventGroup(self, event_group):
        self.event_groups.append(event_group)

    def start(self):
        self.loop = True
        self.ct = Thread(target=self._checkThreadStatus, args=())
        self.ct.start()
        self.ts = Thread(target=self._checkEventGroups) 
        self.ts.start()

    def join(self):
        self.ts.join()
        self.ct.join()

    def stop(self):
        self.loop = False