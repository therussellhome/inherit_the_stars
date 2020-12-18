import unittest
from .. import treaty
from .. import reference

class TestTreaty(unittest.TestCase):
    def test_merge1(self):
        t0 = treaty.Treaty()
        t1 = treaty.Treaty()
        for f in treaty.TREATY_BUY_SELL_FIELDS:
            t0[f] = 10
            t1[f] = 20
        t0.merge(t1)
        self.assertEqual(t0.status, 'pending')
        for f in treaty.TREATY_HALF_FIELDS:
            self.assertEqual(t0['buy' + f], 20)
            self.assertEqual(t0['sell' + f], 10)

    def test_merge2(self):
        t0 = treaty.Treaty()
        t1 = treaty.Treaty(status='rejected')
        t0.merge(t1)
        self.assertEqual(t0.status, 'rejected')

    def test_for_other_player1(self):
        p = reference.Reference('Player')
        t0 = treaty.Treaty(relation='enemy', status='active')
        for f in treaty.TREATY_HALF_FIELDS:
            t0['buy' + f] = 10
            t0['sell' + f] = 20
        t1 = t0.for_other_player(p)
        self.assertEqual(t1.other_player, p)
        self.assertEqual(t1.relation, 'enemy')
        self.assertEqual(t1.status, 'active')
        for f in treaty.TREATY_HALF_FIELDS:
            self.assertEqual(t1['buy' + f], 20)
            self.assertEqual(t1['sell' + f], 10)

    def test_for_other_player2(self):
        p = reference.Reference('Player')
        t0 = treaty.Treaty(status='pending')
        t1 = t0.for_other_player(p)
        self.assertEqual(t1.status, 'proposed')

    def test_for_other_player3(self):
        p = reference.Reference('Player')
        t0 = treaty.Treaty(status='proposed')
        t1 = t0.for_other_player(p)
        self.assertEqual(t1.status, 'pending')

    def test_is_active1(self):
        t0 = treaty.Treaty(status='signed')
        self.assertTrue(t0.is_active())

    def test_is_active2(self):
        t0 = treaty.Treaty(status='pending')
        self.assertFalse(t0.is_active())

    def test_is_draft1(self):
        t0 = treaty.Treaty(status='pending')
        self.assertTrue(t0.is_draft())

    def test_is_draft2(self):
        t0 = treaty.Treaty(status='signed')
        self.assertFalse(t0.is_draft())

    def test_is_rejected1(self):
        t0 = treaty.Treaty(status='rejected')
        self.assertTrue(t0.is_rejected())

    def test_is_rejected2(self):
        t0 = treaty.Treaty(status='pending')
        self.assertFalse(t0.is_rejected())
