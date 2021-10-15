import pythoncom


class ComThread:

    def __init__(self, target):
        self.run = target

    def start(self):
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
        self.run()
        pythoncom.CoUninitialize()
