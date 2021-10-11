import sys
from constants import EVENT_ARG_DELIMITER
import unittest
from mock import Mock

sys.modules['pythoncom'] = Mock()
sys.modules['win32com'] = Mock()
sys.modules['services'] = Mock()


class EventTestCase(unittest.TestCase):

    def test_tostring(self):
        from events.event import Event
        e = Event("nm", Mock(), Mock())
        self.assertEqual(" $wait=1 $event=nm{0}{1}{0}{2} ".format(EVENT_ARG_DELIMITER, 1, 2), e.to_string(1, 2))
        e = Event("nm", Mock(), Mock(), blocking=False)
        self.assertEqual(" $event=nm ", e.to_string())

    if __name__ == '__main__':
        unittest.main()
