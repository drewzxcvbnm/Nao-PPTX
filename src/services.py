import qi
from collections import deque
from threading import Thread
import time

class EventQueue:

    def __init__(self):
        self.eventQueue = deque()

    def start(self):
        Thread(target=self._run).start()

    def add(self, func):
        self.eventQueue.append(func)

    def _run(self):
        while True:
            if len(self.eventQueue) != 0:
                self.eventQueue.popleft()()
            time.sleep(0.1)

eventqueue = EventQueue()
eventqueue.start()
session = qi.Session()
# session.connect("tcp://" + "192.168.253.155" + ":" + "9559")
session.connect("tcp://" + "192.168.252.226" + ":" + "9559")
# session.connect("tcp://" + "192.168.253.68" + ":" + "9559")
#global tts, atts, touch
tts = session.service("ALTextToSpeech")
atts = session.service("ALAnimatedSpeech")
alife = session.service("ALAutonomousLife")
motion = session.service("ALMotion")
asr = session.service("ALSpeechRecognition")
touch = session.service("ALTouch")
mem = session.service("ALMemory")
posture = session.service( "ALRobotPosture" )


