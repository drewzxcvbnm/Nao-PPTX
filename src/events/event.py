from enum import Enum
from constants import EVENT_ARG_DELIMITER
from comthreadeventexecutor import ComThreadEventExecutor
from threading import Lock
from services import mem


class ExecutionModel(Enum):
    GLOBAL = 1  # event executed on global thread executor
    SEPARATE = 2  # event executed on newly created thead executor


class Event:
    global_executor = ComThreadEventExecutor()
    mutex = Lock()

    def __init__(self, name, function, presentation, com_context=None, execution_model=ExecutionModel.SEPARATE,
                 blocking=True):
        self.name = name
        self.function = function
        self.presentation = presentation
        self.com_context = com_context
        self.blocking = blocking
        if execution_model == ExecutionModel.SEPARATE:
            self.executor = ComThreadEventExecutor(com_context)
        if execution_model == ExecutionModel.GLOBAL:
            self.executor = Event.global_executor
        self.execution_model = execution_model

    def execute_event(self, string):
        func = self._get_execution_function(string)
        if not self.blocking:
            self.add_to_executor(func)
            return
        func = self._get_function_with_self_removal(func)
        self.add_self()
        self.add_to_executor(func)

    def add_to_executor(self, func):
        if self.com_context is not None:
            func.with_com_context = True
        self.executor.add_event_to_queue(func)

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

    def remove_self(self):
        Event.mutex.acquire()
        self.presentation.ongoing_events.remove(self)
        if len(self.presentation.ongoing_events) == 0:
            mem.insertData("wait", 0)
        Event.mutex.release()

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
