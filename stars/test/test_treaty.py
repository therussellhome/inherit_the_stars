from unittest import TestCase
from .. import treaties

class TestTreaty(TestCase):
    def setUp(self):
        self.m0 = treaties.Treaty(status = 'received',
                                  cost_p2_to_p1_titanium=0, p2_is_selling_titanium=True,
                                  cost_p2_to_p1_silicon=0, p2_is_selling_silicon=True,
                                  cost_p2_to_p1_lithium=0, p2_is_selling_lithium=True,
                                  cost_p2_to_p1_fuel=0, p2_is_selling_fuel=True,
                                  cost_p2_to_p1_stargate=0, p2_is_selling_stargate=True,
                                  cost_p2_to_p1_passage=0, p2_is_selling_passage=True,
                                  cost_p2_to_p1_intel=0, p2_is_selling_intel=True,)
        self.m1 = treaties.Treaty(status = 'received',
                                  cost_p1_to_p2_titanium=0, p1_is_selling_titanium=True,
                                  cost_p1_to_p2_silicon=0, p1_is_selling_silicon=True,
                                  cost_p1_to_p2_lithium=0, p1_is_selling_lithium=True,
                                  cost_p1_to_p2_fuel=0, p1_is_selling_fuel=True,
                                  cost_p1_to_p2_stargate=0, p1_is_selling_stargate=True,
                                  cost_p1_to_p2_passage=0, p1_is_selling_passage=True,
                                  cost_p1_to_p2_intel=0, p1_is_selling_intel=True,)
        self.t1 = treaties.Treaty(status = 'received')
        self.t2 = treaties.Treaty(status = 'received',
                                  cost_p1_to_p2_titanium=0, p1_is_selling_titanium=True,
                                  cost_p2_to_p1_titanium=0, p2_is_selling_titanium=True,
                                  cost_p1_to_p2_silicon=0, p1_is_selling_silicon=True,
                                  cost_p2_to_p1_silicon=0, p2_is_selling_silicon=True,
                                  cost_p1_to_p2_lithium=0, p1_is_selling_lithium=True,
                                  cost_p2_to_p1_lithium=0, p2_is_selling_lithium=True,
                                  cost_p1_to_p2_fuel=0, p1_is_selling_fuel=True,
                                  cost_p2_to_p1_fuel=0, p2_is_selling_fuel=True,
                                  cost_p1_to_p2_stargate=0, p1_is_selling_stargate=True,
                                  cost_p2_to_p1_stargate=0, p2_is_selling_stargate=True,
                                  cost_p1_to_p2_passage=0, p1_is_selling_passage=True,
                                  cost_p2_to_p1_passage=0, p2_is_selling_passage=True,
                                  cost_p1_to_p2_intel=0, p1_is_selling_intel=True,
                                  cost_p2_to_p1_intel=0, p2_is_selling_intel=True,)
    def test_merge(self):
        return #TODO LOTS OF BUGS
        a = self.t1.merge(self.t1)
        self.assertEqual(a[0], a[0])
        #print(1)
        self.assertEqual(a[1], a[0])
        #print(2)
        a = self.t1.merge(self.t2)
        self.assertEqual(a[0], self.m0)
        self.assertEqual(a[1], self.m1)
        a = self.t1.merge(self.m0)
        self.assertEqual(a[0], self.t1)
        self.assertEqual(a[1], self.t1)
        a = self.t1.merge(self.m1)
        self.assertEqual(a[0], self.m0)
        self.assertEqual(a[1], self.m1)
        a = self.t2.merge(self.t1)
        self.assertEqual(a[0], self.m1)
        self.assertEqual(a[1], self.m0)
        a = self.t2.merge(self.t2)
        self.assertEqual(a[0], self.t2)
        self.assertEqual(a[1], self.t2)
        a = self.t2.merge(self.m0)
        self.assertEqual(a[0], self.m1)
        self.assertEqual(a[1], self.m0)
        a = self.t2.merge(self.m1)
        self.assertEqual(a[0], self.t2)
        self.assertEqual(a[1], self.t2)
        a = self.m0.merge(self.t1)
        self.assertEqual(a[0], self.t1)
        self.assertEqual(a[1], self.t1)
        a = self.m0.merge(self.t2)
        self.assertEqual(a[0], self.m0)
        self.assertEqual(a[1], self.m1)
        a = self.m0.merge(self.m0)
        self.assertEqual(a[0], self.t1)
        self.assertEqual(a[1], self.t1)
        a = self.m0.merge(self.m1)
        self.assertEqual(a[0], self.m0)
        self.assertEqual(a[1], self.m1)
        a = self.m1.merge(self.t1)
        self.assertEqual(a[0], self.m1)
        self.assertEqual(a[1], self.m0)
        a = self.m1.merge(self.t2)
        self.assertEqual(a[0], self.t2)
        self.assertEqual(a[1], self.t2)
        a = self.m1.merge(self.m0)
        self.assertEqual(a[0], self.m1)
        self.assertEqual(a[1], self.m0)
        a = self.m1.merge(self.m1)
        self.assertEqual(a[0], self.t2)
        self.assertEqual(a[1], self.t2)
        b = treaties.Treaty(p1 = 'a', p2 = 'b')
        c = treaties.Treaty(p1 = 'c', p2 = 'a')
        a = b.merge(c)
        self.assertEqual(a[0], None)
        self.assertEqual(a[1], None)
    def test_flip(self):
        return #TODO 
        self.assertEqual(self.t1, self.t1.flip())
        self.assertEqual(self.t2, self.t2.flip())
        self.assertEqual(self.m1, self.m0.flip())
        self.assertEqual(self.m0, self.m1.flip())
        t = self.t1.flip()
        self.assertEqual(self.t1, t.flip())
        t = self.t2.flip()
        self.assertEqual(self.t2, t.flip())
        t = self.m1.flip()
        self.assertEqual(self.m1, t.flip())
        t = self.m0.flip()
        self.assertEqual(self.m0, t.flip())
        



