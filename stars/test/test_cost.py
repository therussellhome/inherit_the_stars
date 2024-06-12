import unittest
from .. import *


class CostTestCase(unittest.TestCase):
    def test_eq(self):
        c1 = cost.Cost(energy=123, silicon=2)
        c2 = cost.Cost(energy=321, silicon=3)
        c3 = cost.Cost(energy=321, silicon=3)
        self.assertNotEqual(c1, c2)
        self.assertEqual(c2, c3)

    def test_add(self):
        c1 = cost.Cost(energy=123, silicon=2)
        c2 = cost.Cost(energy=321, silicon=3)
        c3 = c1 + c2
        self.assertEqual(c3.energy, 444)
        self.assertEqual(c3.silicon, 5)

    def test_sub(self):
        c1 = cost.Cost(energy=321, silicon=3)
        c2 = cost.Cost(energy=123, silicon=2)
        c3 = c1 - c2
        self.assertEqual(c3.energy, 198)
        self.assertEqual(c3.silicon, 1)

    def test_mul(self):
        c1 = cost.Cost(energy=123, silicon=2)
        c3 = c1 * 3
        self.assertEqual(c3.energy, 369)
        self.assertEqual(c3.silicon, 6)

    def test_div(self):
        c1 = cost.Cost(energy=369, silicon=6)
        c3 = c1 / 3
        self.assertEqual(c3.energy, 123)
        self.assertEqual(c3.silicon, 2)

    def test_percent(self):
        c1 = cost.Cost(energy=100, titanium=3, silicon=1)
        c2 = cost.Cost(energy=200, titanium=6, silicon=2)
        self.assertEqual(c1.percent(c2), 50) 
    
    def test_percent2(self):
        c1 = cost.Cost(energy=100, titanium=3, silicon=1)
        c2 = cost.Cost(energy=2000, titanium=29, silicon=1)
        self.assertEqual(c1.percent(c2), 90) 

    def test_percent3(self):
        c1 = cost.Cost(energy=1000, titanium=3, lithium=24, silicon=1)
        c2 = cost.Cost(energy=2000, lithium=19, silicon=1)
        self.assertEqual(c1.percent(c2), 5)

    def test_percent4(self):
        c1 = cost.Cost(energy=1600, titanium=3, lithium=24, silicon=1)
        c2 = cost.Cost(energy=2000, titanium=60, lithium=19, silicon=1)
        self.assertEqual(c1.percent(c2), 56)

    def test_percent5(self):
        c1 = cost.Cost(energy=10, titanium=0, lithium=0, silicon=0)
        c2 = cost.Cost(energy=2000, titanium=60, lithium=19, silicon=1)
        self.assertEqual(c1.percent(c2), 99)
    
    def test_percent0(self):
        c1 = cost.Cost(energy=2000, titanium=60, lithium=19, silicon=1)
        c2 = cost.Cost(energy=2000, titanium=60, lithium=19, silicon=1)
        self.assertEqual(c1.percent(c2), 0)
    
    def test_percent000(self):
        c1 = cost.Cost(energy=2000, titanium=60, lithium=19, silicon=1)
        c2 = cost.Cost(energy=0, titanium=0, lithium=0, silicon=0)
        self.assertEqual(c1.percent(c2), 100)

    def test_is_zero1(self):
        c1 = cost.Cost()
        self.assertTrue(c1.is_zero())

    def test_is_zero2(self):
        c1 = cost.Cost(energy=123, silicon=2)
        self.assertFalse(c1.is_zero())

    def test_html1(self):
        c1 = cost.Cost()
        self.assertEqual(c1.to_html(), '')

    def test_html2(self):
        c1 = cost.Cost(energy=1, titanium=2, lithium=3, silicon=4)
        self.assertEqual(c1.to_html(), '<i class="fa-bolt" title="Energy">1</i><i class="ti" title="Titanium">2</i><i class="li" title="Lithium">3</i><i class="si" title="Silicon">4</i>')
