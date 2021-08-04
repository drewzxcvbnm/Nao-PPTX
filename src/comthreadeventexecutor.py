from collections import deque
from threading import Thread
import time
import pythoncom
import win32com


class COMThreadEventExecutor:

    def __init__(self, **com_context):
        self.eventQueue = deque()
        self.COMContext = com_context
        self.loop = True
        Thread(target=self._run).start()

    def add_event_to_queue(self, func):
        self.eventQueue.append(func)

    def _run(self):
        self._init_context()
        while self.loop:
            if len(self.eventQueue) != 0:
                self.eventQueue.popleft()(self.COMContext)
            time.sleep(0.1)

    def stop(self):
        self.loop = False

    def _init_context(self):
        pythoncom.CoInitialize()
        for name, id in self.COMContext.items():
            self.COMContext[name] = win32com.client.Dispatch(
                pythoncom.CoGetInterfaceAndReleaseStream(id, pythoncom.IID_IDispatch))
