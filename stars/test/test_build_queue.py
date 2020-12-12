import unittest
from .. import *

class BuildQueueTestCase(unittest.TestCase):
    def test_finish1(self):
        # Method does nothing so just verifying that no errors are thrown
        b = build_queue.BuildQueue()
        b.finish()
        self.assertTrue(True)
