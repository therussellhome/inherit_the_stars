import unittest
from .. import *

class BuildQueueTestCase(unittest.TestCase):
    def test_build1(self):
        b = build_queue.BuildQueue(cost=cost.Cost(energy=123))
        c = b.build(cost.Cost(energy=23))
        self.assertEqual(c.energy, 100)

    def test_cancel1(self):
        b = build_queue.BuildQueue()
        # Method does nothing so just verifying that no errors are thrown
        b.cancel()
        self.assertTrue(True)

    def test_html1(self):
        b = build_queue.BuildQueue()
        self.assertEqual(b.to_html(), '??? mystery item ???')
