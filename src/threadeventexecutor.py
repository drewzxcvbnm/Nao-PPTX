from collections import deque
from threading import Thread
import time
import pythoncom
import win32com


class ThreadEventExecutor:

    def __init__(self, **COMContext):
        self.eventQueue = deque()
        self.COMContext = COMContext
        self.loop = True
        Thread(target=self._run).start()

    def addEventToQueue(self, func):
        self.eventQueue.append(func)

    def _run(self):
        self._initContext()
        while self.loop:
            if len(self.eventQueue) != 0:
                self.eventQueue.popleft()(self.COMContext)
            time.sleep(0.1)

    def stop(self):
        self.loop = False

    def _initContext(self):
        pythoncom.CoInitialize()
        for name, id in self.COMContext.items():
            self.COMContext[name] = win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(id, pythoncom.IID_IDispatch))
