import unittest
from .. import *

class NewGameTestCase(unittest.TestCase):
    def setUp(self):
        self.ng = new_game.NewGame()
    def test_calc_num_systems(self):
        self.assertEqual(self.ng.calc_num_systems(), 50)
        self.ng.new_game_x = 0
        self.assertEqual(self.ng.calc_num_systems(), 99)#round(((4/3)*3.14159)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**2) * self.ng.new_game_density)
        self.ng.new_game_y = 50
        self.assertEqual(self.ng.calc_num_systems(), 50)#round(((4/3)*3.14159)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**2) * self.ng.new_game_density)
        self.ng.new_game_z = 50
        self.ng.new_game_x = 50
        self.assertEqual(self.ng.calc_num_systems(), 6)#ound(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**2) * self.ng.new_game_density)        
        self.ng.new_game_density = 50
        self.assertEqual(self.ng.calc_num_systems(), 3)#round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))        
        self.ng.new_game_x = 25
        self.ng.new_game_y = 25
        self.ng.new_game_z = 100
        self.assertEqual(self.ng.calc_num_systems(), 2)#round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))        
        self.ng.new_game_x = 25
        self.ng.new_game_y = 50
        self.ng.new_game_z = 100
        self.assertEqual(self.ng.calc_num_systems(), 3)#round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))        
        self.ng.new_game_x = 1
        self.ng.new_game_y = 1
        self.ng.new_game_z = 1
        self.assertEqual(self.ng.calc_num_systems(), 209)#round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))        
    def test_create_systems(self):
        self.assertEqual(len(self.ng.create_systems(round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))), round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))
        self.ng.new_game_x = 80
        self.assertEqual(len(self.ng.create_systems(round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))), round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))
        self.ng.new_game_y = 16
        self.assertEqual(len(self.ng.create_systems(round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))), round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))
        self.ng.new_game_z = 59
        self.ng.new_game_x = 2
        self.assertEqual(len(self.ng.create_systems(round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))), round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))
        self.ng.new_game_density = 50
        self.assertEqual(len(self.ng.create_systems(round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))), round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))
        self.ng.new_game_x = 95
        self.ng.new_game_y = 65
        self.ng.new_game_z = 25
        self.assertEqual(len(self.ng.create_systems(round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))), round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))
        self.ng.new_game_x = 20
        self.ng.new_game_y = 57
        self.ng.new_game_z = 90
        self.assertEqual(len(self.ng.create_systems(round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))), round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))
        self.ng.new_game_x = 10
        self.ng.new_game_y = 100
        self.ng.new_game_z = 1
        self.assertEqual(len(self.ng.create_systems(round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))), round(((4/3)*3.14159)*(self.ng.new_game_x/2)*(self.ng.new_game_y/2)*(self.ng.new_game_z/2)/(100**3) * self.ng.new_game_density))
    def test_generate_home_systems(self):
        system = []
        system.append(star_system.StarSystem(name='antheu 0', x=0, y=0, z=0))
        system.append(star_system.StarSystem(name='antheu 1', x=0, y=0, z=0))
        system.append(star_system.StarSystem(name='antheu 2', x=0, y=0, z=0))
        system.append(star_system.StarSystem(name='antheu 3', x=0, y=0, z=0))
        system.append(star_system.StarSystem(name='antheu 4', x=0, y=0, z=0))
        s = star_system.StarSystem(name='antheu 5', x=100, y=50, z=100)
        system.append(s)
        homes = self.ng.generate_home_systems(2, system, 50)
        self.assertIn(s, homes)
        t = star_system.StarSystem(name='rc,g 0', x=-100, y=-50, z=-100)
        system.append(t)
        homes = self.ng.generate_home_systems(3, system, 50)
        self.assertIn(t, homes)
        self.assertIn(s, homes)