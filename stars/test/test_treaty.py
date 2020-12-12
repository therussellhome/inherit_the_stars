import unittest
from .. import treaties

class TestTreaty(unittest.TestCase):
    def setUp(self):
        self.m0 = treaties.Treaty(buy_ti=0, buy_ti_at=True,
                                  buy_si=0, buy_si_at=True,
                                  buy_li=0, buy_li_at=True,
                                  buy_fuel=0, buy_fuel_at=True,
                                  buy_gate=0, buy_gate_at=True,
                                  buy_passage=0, buy_passage_at=True,
                                  buy_intel=0, buy_intel_at=True,)
        self.m1 = treaties.Treaty(sell_ti=0, sell_ti_at=True,
                                  sell_si=0, sell_si_at=True,
                                  sell_li=0, sell_li_at=True,
                                  sell_fuel=0, sell_fuel_at=True,
                                  sell_gate=0, sell_gate_at=True,
                                  sell_passage=0, sell_passage_at=True,
                                  sell_intel=0, sell_intel_at=True,)
        self.t1 = treaties.Treaty()
        self.t2 = treaties.Treaty(sell_ti=0, sell_ti_at=True,
                                  buy_ti=0, buy_ti_at=True,
                                  sell_si=0, sell_si_at=True,
                                  buy_si=0, buy_si_at=True,
                                  sell_li=0, sell_li_at=True,
                                  buy_li=0, buy_li_at=True,
                                  sell_fuel=0, sell_fuel_at=True,
                                  buy_fuel=0, buy_fuel_at=True,
                                  sell_gate=0, sell_gate_at=True,
                                  buy_gate=0, buy_gate_at=True,
                                  sell_passage=0, sell_passage_at=True,
                                  buy_passage=0, buy_passage_at=True,
                                  sell_intel=0, sell_intel_at=True,
                                  buy_intel=0, buy_intel_at=True,)
    def test_merge(self):
        a = self.t1.merge(self.t1)
        self.t1.name=a.name
        self.assertEqual(a, self.t1)
        #print(1)
        a = self.t1.merge(self.t2)
        self.m0.name=a.name
        self.assertEqual(a, self.m0)
        a = self.t1.merge(self.m0)
        self.t1.name=a.name
        self.assertEqual(a, self.t1)
        a = self.t1.merge(self.m1)
        self.m0.name=a.name
        self.assertEqual(a, self.m0)
        a = self.t2.merge(self.t1)
        self.m1.name=a.name
        self.assertEqual(a, self.m1)
        a = self.t2.merge(self.t2)
        self.t2.name=a.name
        self.assertEqual(a, self.t2)
        a = self.t2.merge(self.m0)
        self.m1.name=a.name
        self.assertEqual(a, self.m1)
        a = self.t2.merge(self.m1)
        self.t2.name=a.name
        self.assertEqual(a, self.t2)
        a = self.m0.merge(self.t1)
        self.t1.name=a.name
        self.assertEqual(a, self.t1)
        a = self.m0.merge(self.t2)
        self.m0.name=a.name
        self.assertEqual(a, self.m0)
        a = self.m0.merge(self.m0)
        self.t1.name=a.name
        self.assertEqual(a, self.t1)
        a = self.m0.merge(self.m1)
        self.m0.name=a.name
        self.assertEqual(a, self.m0)
        a = self.m1.merge(self.t1)
        self.m1.name=a.name
        self.assertEqual(a, self.m1)
        a = self.m1.merge(self.t2)
        self.t2.name=a.name
        self.assertEqual(a, self.t2)
        a = self.m1.merge(self.m0)
        self.m1.name=a.name
        self.assertEqual(a, self.m1)
        a = self.m1.merge(self.m1)
        self.t2.name=a.name
        self.assertEqual(a, self.t2)

    def test_flip(self):
        self.assertEqual(self.t1, self.t1.flip())
        self.assertEqual(self.t2, self.t2.flip())
        self.m1.name=self.m0.name
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
        
    

