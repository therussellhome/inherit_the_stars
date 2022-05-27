import unittest
from .. import *

class TerraformTestCase(unittest.TestCase):
    def test_cost1(self):
        t = terraform.Terraform(hab='gravity')
        self.assertEqual(t.cost.energy, 2500)

    def test_cost2(self):
        p = reference.Reference('Planet')
        p.gravity_terraform = 9
        t = terraform.Terraform(hab='gravity', planet=p)
        self.assertEqual(t.cost.energy, 44456)

    def test_cost3(self):
        p = reference.Reference('Planet')
        p.player.race.lrt_Bioengineer = True
        t = terraform.Terraform(hab='gravity', planet=p)
        self.assertEqual(t.cost.energy, 1800)

    def test_build1(self):
        p = reference.Reference('Planet')
        t = terraform.Terraform(hab='gravity', planet=p)
        t.build()
        self.assertEqual(p.gravity_terraform, 0)

    def test_build2(self):
        p = reference.Reference('Planet')
        t = terraform.Terraform(hab='gravity', planet=p)
        t.build(t.cost)
        self.assertEqual(p.gravity_terraform, 1)
