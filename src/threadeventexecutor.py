from collections import deque
from threading import Thread
import time


class ThreadEventExecutor:

    def __init__(self):
        self.eventQueue = deque()
        Thread(target=self._run).start()

    def addEventToQueue(self, func):
        self.eventQueue.append(func)

    def _run(self):
        while True:
            if len(self.eventQueue) != 0:
                self.eventQueue.popleft()()
            time.sleep(0.1)
