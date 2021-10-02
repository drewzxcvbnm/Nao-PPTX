from collections import deque
from threading import Thread
import time
import pythoncom
import win32com


class ComThreadEventExecutor:

    def __init__(self, com_context=None):
        self.event_queue = deque()
        self.com_context = com_context
        if com_context is not None:
            self._pre_init_context()
        self.loop = True
        self.thread = Thread(target=self._run)
        self.thread.start()

    def add_event_to_queue(self, func):
        self.event_queue.append(func)

    def _run(self):
        if self.com_context is not None:
            self._init_context()
        while self.loop:
            if len(self.event_queue) != 0:
                function = self.event_queue.popleft()
                if getattr(function, 'with_com_context', False):
                    function(self.com_context)
                else:
                    function()
            time.sleep(0.1)

    def __del__(self):
        self.loop = False
        self.thread.join()

    def _pre_init_context(self):
        com_context = {}
        for name, obj in self.com_context.items():
            com_context[name] = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, obj)
        self.com_context = com_context

    def _init_context(self):
        pythoncom.CoInitialize()
        for name, id in self.com_context.items():
            self.com_context[name] = win32com.client.Dispatch(
                pythoncom.CoGetInterfaceAndReleaseStream(id, pythoncom.IID_IDispatch))
