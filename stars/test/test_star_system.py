import unittest
from .. import *

class StarSystemTestCase(unittest.TestCase):
    def test_ID_planet(self):
        s = star_system.StarSystem(ID='Tribond')
        s.create_system(race=reference.Reference(race.Race()), num_planets=2)
        self.assertEqual(s.ID, 'Tribond')
        self.assertEqual(s.planets[0].ID, "Tribond's Star")
        self.assertEqual(s.planets[1].ID, 'Tribond I')
        self.assertEqual(s.planets[2].ID, 'Tribond II')

    # bringing test coverage to 100%
    def test_no_inputs(self):
        s = star_system.StarSystem(ID='Tribond')
        s.create_system()
        self.assertEqual(s.ID, 'Tribond')
        self.assertEqual(s.planets[0].ID, "Tribond's Star")

    def test_player_is_paanuri(self):
        s = star_system.StarSystem(ID='Tribond')
        r = race.Race(primary_race_trait='Pa\'anuri')
        s.create_system(race=reference.Reference(r), num_planets=2)
        self.assertEqual(s.ID, 'Tribond')
        self.assertEqual(s.planets[0].ID, "Tribond's Star")
        self.assertEqual(s.planets[1].ID, 'Tribond I')
        self.assertEqual(s.planets[2].ID, 'Tribond II')

    def test_get_outer_system(self):
        s = star_system.StarSystem()
        l = location.Location(1, 0, 0)
        pos = s.get_outer_system(l)
        right_pos = location.location(stars_math.TERAMETER_2_LIGHTYEAR, 0, 0)
        self.assertEqual(pos, right_pos)
    
    # testing the lay_mines function
    def test_lay_mines(self):
        s = star_system.StarSystem()
        p1 = player.Player()
        s.lay_mines(200, p1)
        self.assertEqual(s.minefield, 200)
        self.assertEqual(s.minefield_owner.ID, p1.ID)

    #TODO testing the sweep_mines function
    def test_sweep_mines(self):
        s = star_system.StarSystem()
        p1 = player.Player()
        s.lay_mines(200, p1)

    #TODO testing the mines_decay function
    def test_mines_decay(self):
        s = star_system.StarSystem()
        p1 = player.Player()
        s.lay_mines(200, p1)
