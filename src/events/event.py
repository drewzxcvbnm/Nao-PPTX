from enum import Enum
from services import mem
from threading import Lock
from comthread import ComThread
from constants import EVENT_ARG_DELIMITER


class Event:
    mutex = Lock()

    def __init__(self, name, function, presentation, com_context=None, blocking=True):
        self.name = name
        self.function = function
        self.presentation = presentation
        self.com_context = com_context
        self.blocking = blocking

    def execute_event(self, string):
        func = self._get_execution_function(string)
        if not self.blocking:
            ComThread(target=func).start()
            return
        func = self._get_function_with_self_removal(func)
        self.add_self()
        ComThread(target=func).start()

    def _get_function_with_self_removal(self, function):
        def with_removal(*args, **kwargs):
            function(*args, **kwargs)
            Event.mutex.acquire()
            self.presentation.ongoing_events.remove(self)
            if len(self.presentation.ongoing_events) == 0:
                mem.insertData("wait", 0)
            Event.mutex.release()

        return with_removal

    def _get_execution_function(self, string):
        args = self._get_args(string)
        if self.com_context is not None:
            return lambda cc: self.function(cc, *args)
        else:
            return lambda: self.function(*args)

    def add_self(self):
        Event.mutex.acquire()
        self.presentation.ongoing_events.append(self)
        Event.mutex.release()

    def to_string(self, *args):
        s = "$event={}".format(self.name)
        s = EVENT_ARG_DELIMITER.join(([s] + [str(i) for i in args]))
        if self.blocking:
            s = "$wait=1 " + s
        return " " + s + " "

    def _get_args(self, string):
        args = string.split(EVENT_ARG_DELIMITER)[1:]
        return args

    def __del__(self):
        del self.executor
