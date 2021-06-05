import unittest
from unittest.mock import patch
from .. import *

class FleetCase(unittest.TestCase):
    def test_add_1(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
        self.assertTrue(ship_1 in fleet_one.ships)
        self.assertTrue(ship_2 in fleet_one.ships)
    
    def test_add_2(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + [ship_2, ship_2]
        self.assertTrue(ship_2 in fleet_one.ships)
        self.assertEqual(len(fleet_one.ships), 1)
    
    def test_add_3(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + ship_1
        fleet_one._stats()
        fleet_one += ship_2
        self.assertTrue(ship_1 in fleet_one.ships)
        self.assertTrue(ship_2 in fleet_one.ships)
    
    def test_add_4(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
        fleet_two = fleet.Fleet() + fleet_one
        self.assertTrue(ship_1 in fleet_two.ships)
        self.assertTrue(ship_2 in fleet_two.ships)
    
    def test_add_5(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship(location=location.Location(1, 1, 1))
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
        self.assertTrue(ship_1 in fleet_one.ships)
        self.assertFalse(ship_2 in fleet_one.ships)

    def test_sub_1(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
        fleet_one._stats()
        fleet_one -= ship_2
        self.assertTrue(ship_1 in fleet_one.ships)
        self.assertFalse(ship_2 in fleet_one.ships)
        self.assertEqual(len(fleet_one.ships), 1)

    def test_sub_2(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
        fleet_one -= [ship_2]
        self.assertTrue(ship_1 in fleet_one.ships)
        self.assertFalse(ship_2 in fleet_one.ships)
        self.assertEqual(len(fleet_one.ships), 1)

    def test_sub_3(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
        fleet_two = fleet.Fleet() + [ship_1, ship_2]
        fleet_one -= fleet_two
        self.assertEqual(len(fleet_one.ships), 0)

    def test_duplicate1(self):
        f0 = fleet.Fleet() + ship.Ship()
        f0.location = location.Location(1, 0, 0)
        f0.orders.append(order.Order())
        f1 = f0.duplicate()
        self.assertEqual(f0.location, f1.location)
        self.assertEqual(len(f0.ships), 1)
        self.assertEqual(len(f1.ships), 0)

    def test_next_hundreth(self):
        f = fleet.Fleet()
        f._stats()
        f.next_hundreth()
        self.assertTrue('stats' not in f.__cache__)

    def test_read_orders1(self):
        f = fleet.Fleet() + ship.Ship()
        f.read_orders()
        self.assertEqual(f.__cache__['move'], None)
        self.assertEqual(f.__cache__['move_in_system'], location.Location())

    def test_read_orders2(self):
        f = fleet.Fleet() + ship.Ship(engines=[engine.Engine()])
        f.location = location.Location(1, 0, 0)
        with patch.object(ship.Ship, 'is_space_station', return_value=True) as mock:
            f.read_orders()
        self.assertEqual(f.__cache__['move'], None)
        self.assertEqual(f.__cache__['move_in_system'].xyz, (1, 0, 0))

    def test_read_orders3(self):
        f = fleet.Fleet() + ship.Ship(engines=[engine.Engine()])
        f.location = location.Location(1, 0, 0)
        with patch.object(order.Order, 'move_calc', return_value=(location.Location(), location.Location())):
            f.read_orders()
        self.assertEqual(f.__cache__['move'], location.Location())
        self.assertEqual(f.__cache__['move_in_system'], location.Location())

    def test_colonize1(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        s.create_system(num_planets=1)
        f = fleet.Fleet() + ship.Ship()
        f.colonize()
        self.assertEqual(len(f.ships), 1)
        self.assertFalse(s.planets[1].is_colonized())

    def test_colonize2(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True)
        s.create_system(num_planets=1)
        f.colonize()
        self.assertEqual(len(f.ships), 1)
        self.assertFalse(s.planets[1].is_colonized())

    def test_colonize3(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True, cargo_max=500)
        f.ships[0].cargo.people = 500
        s.create_system(num_planets=1)
        f.colonize()
        self.assertEqual(len(f.ships), 1)
        self.assertFalse(s.planets[1].is_colonized())

    def test_colonize4(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True, cargo_max=500)
        f.ships[0].cargo.people = 500
        f.location = location.Location(reference=s)
        s.create_system(num_planets=1)
        s.planets[1].on_surface.people = 1
        f.colonize()
        self.assertEqual(len(f.ships), 1)

    def test_colonize5(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True, cargo_max=500)
        f.ships[0].cargo.people = 500
        f.location = location.Location(reference=s)
        s.create_system(num_planets=1)
        f.order.colonize_manual = True
        f.colonize()
        self.assertEqual(len(f.ships), 1)
        self.assertFalse(s.planets[1].is_colonized())

    def test_colonize6(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True, cargo_max=500)
        f.ships[0].cargo.people = 500
        f.location = location.Location(reference=s)
        s.create_system(num_planets=1)
        f.order.colonize_manual = True
        f.order.location = location.Location(reference=s.planets[1])
        f.colonize()
        self.assertEqual(len(f.ships), 0)
        self.assertTrue(s.planets[1].is_colonized())
        self.assertTrue(s.planets[1].on_surface.people, 500)

    def test_colonize7(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True, cargo_max=500)
        f.ships[0].cargo.people = 500
        f.location = location.Location(reference=s)
        s.create_system(num_planets=1)
        s.planets[1].temperature = -1
        f.colonize()
        self.assertEqual(len(f.ships), 1)
        self.assertFalse(s.planets[1].is_colonized())

    def test_colonize8(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True, cargo_max=500)
        f.ships[0].cargo.people = 500
        f.location = location.Location(reference=s)
        s.create_system(num_planets=1)
        s.planets[1].temperature = (f.ships[0].player.race.hab_temperature_stop + f.ships[0].player.race.hab_temperature) / 2
        s.planets[1].gravity = (f.ships[0].player.race.hab_gravity_stop + f.ships[0].player.race.hab_gravity) / 2
        s.planets[1].radiation = (f.ships[0].player.race.hab_radiation_stop + f.ships[0].player.race.hab_radiation) / 2
        f.colonize()
        self.assertEqual(len(f.ships), 0)
        self.assertTrue(s.planets[1].is_colonized())
        self.assertTrue(s.planets[1].on_surface.people, 500)

    def test_colonize9(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True, cargo_max=500)
        f.ships[0].cargo.people = 500
        f.location = location.Location(reference=s)
        s.create_system(num_planets=2)
        # Planet 1 is less ideal
        s.planets[1].temperature = (f.ships[0].player.race.hab_temperature_stop + f.ships[0].player.race.hab_temperature) / 2 - 1
        s.planets[1].gravity = (f.ships[0].player.race.hab_gravity_stop + f.ships[0].player.race.hab_gravity) / 2 - 1
        s.planets[1].radiation = (f.ships[0].player.race.hab_radiation_stop + f.ships[0].player.race.hab_radiation) / 2 - 1
        s.planets[2].temperature = (f.ships[0].player.race.hab_temperature_stop + f.ships[0].player.race.hab_temperature) / 2
        s.planets[2].gravity = (f.ships[0].player.race.hab_gravity_stop + f.ships[0].player.race.hab_gravity) / 2
        s.planets[2].radiation = (f.ships[0].player.race.hab_radiation_stop + f.ships[0].player.race.hab_radiation) / 2
        f.colonize()
        self.assertEqual(len(f.ships), 0)
        self.assertTrue(s.planets[2].is_colonized())
        self.assertTrue(s.planets[2].on_surface.people, 500)

    def test_colonize10(self):
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f = fleet.Fleet() + ship.Ship(is_colonizer=True, cargo_max=500, commissioning=101) + ship.Ship(is_colonizer=True, cargo_max=500, commissioning=100)
        f.ships[0].cargo.people = 500
        f.ships[1].cargo.people = 500
        f.location = location.Location(reference=s)
        s.create_system(num_planets=1)
        s.planets[1].temperature = (f.ships[0].player.race.hab_temperature_stop + f.ships[0].player.race.hab_temperature) / 2
        s.planets[1].gravity = (f.ships[0].player.race.hab_gravity_stop + f.ships[0].player.race.hab_gravity) / 2
        s.planets[1].radiation = (f.ships[0].player.race.hab_radiation_stop + f.ships[0].player.race.hab_radiation) / 2
        f.colonize()
        self.assertEqual(len(f.ships), 1)
        self.assertEqual(f.ships[0].commissioning, 101)
        print(s.planets[1].ID)
        self.assertTrue(s.planets[1].is_colonized())
        self.assertTrue(s.planets[1].on_surface.people, 500)

    def test_hyperdenial1(self):
        f = fleet.Fleet() + ship.Ship()
        with patch.object(hyperdenial.HyperDenial, 'activate') as mock:
            f.hyperdenial()
            self.assertEqual(mock.call_count, 0)

    def test_hyperdenial2(self):
        f = fleet.Fleet() + ship.Ship()
        stats = f._stats()
        stats.hyperdenial.radius = 1
        with patch.object(hyperdenial.HyperDenial, 'activate') as mock:
            f.hyperdenial()
            self.assertEqual(mock.call_count, 1)

    def test_hyperdenial3(self):
        f = fleet.Fleet() + ship.Ship()
        stats = f._stats()
        stats.hyperdenial.range = 1
        f.__cache__['move'] = location.Location()
        with patch.object(hyperdenial.HyperDenial, 'activate') as mock:
            f.hyperdenial()
            self.assertEqual(mock.call_count, 0)

    def test_move1(self):
        f = fleet.Fleet()
        f.location = location.Location(1, 2, 3)
        f.__cache__['move'] = None
        f.move()
        self.assertEqual(f.location.xyz, (1, 2, 3))

    def test_move2(self):
        f = fleet.Fleet()
        f.location = location.Location(1, 2, 3)
        f.__cache__['move'] = location.Location(2, 3, 4)
        f.order.speed = -2
        f.move()
        self.assertEqual(f.location.xyz, (1, 2, 3))

    def test_move3(self):
        f = fleet.Fleet()
        f.location = location.Location(1, 2, 3)
        f.__cache__['move'] = location.Location(2, 3, 4)
        f.order.speed = -1
        with patch.object(fleet.Fleet, '_stargate_check', return_value=True):
            f.move()
        self.assertEqual(f.location.xyz, (1, 2, 3))

    def test_move4(self):
        f = fleet.Fleet()
        stats = f._stats()
        f.location = location.Location(1, 2, 3)
        f.__cache__['move'] = location.Location(1.5, 2 , 3)
        stats.fuel = 100
        stats.fuel_max = 100
        f.order.speed = -1
        with patch.object(fleet.Fleet, '_fuel_calc', return_value=42):
            f.move()
        self.assertEqual(f.location.xyz, (1.5, 2, 3))
        self.assertEqual(stats.fuel, 58)

    def test_move5(self):
        f = fleet.Fleet() + ship.Ship()
        stats = f._stats()
        f.ships[0].engines.append(engine.Engine())
        f.location = location.Location(1, 2, 3)
        f.__cache__['move'] = location.Location(3, 2 , 3)
        stats.fuel = 100
        stats.fuel_max = 100
        f.order.speed = -1
        with patch.object(fleet.Fleet, '_fuel_calc', side_effect=[120, 42, 42]):
            f.move()
        self.assertEqual(f.location.xyz, (1.81, 2, 3))
        self.assertEqual(stats.fuel, 58)

    def test_move6(self):
        f = fleet.Fleet()
        stats = f._stats()
        f.location = location.Location(1, 2, 3)
        f.__cache__['move'] = location.Location(3, 2 , 3)
        stats.fuel = 100
        stats.fuel_max = 100
        f.order.speed = 1
        with patch.object(fleet.Fleet, '_fuel_calc', return_value=42):
            f.move()
        self.assertEqual(f.location.xyz, (1.01, 2, 3))
        self.assertEqual(stats.fuel, 58)

    def test_move7(self):
        f = fleet.Fleet()
        stats = f._stats()
        f.location = location.Location(1, 2, 3)
        f.__cache__['move'] = location.Location(3, 2 , 3)
        stats.fuel = 100
        stats.fuel_max = 100
        f.order.speed = 10
        with patch.object(fleet.Fleet, '_fuel_calc', side_effect=[120, 42, 42]):
            f.move()
        self.assertEqual(f.location.xyz, (1.01, 2, 3))
        self.assertEqual(stats.fuel, 58)

    def test_move_in_system1(self):
        f = fleet.Fleet()
        f.move_in_system()
        self.assertEqual(f.location.xyz, (0, 0, 0))

    def test_move_in_system2(self):
        f = fleet.Fleet()
        f.__cache__['move_in_system'] = location.Location(1, 0, 0)
        f.move_in_system()
        self.assertEqual(f.location.xyz, (0, 0, 0))

    def test_move_in_system1(self):
        # Use multiple fleets to "simulate" system location hierarchy
        system = fleet.Fleet()
        f = fleet.Fleet()
        f.location = location.Location(1, 0, 0, reference=system)
        f.__cache__['move_in_system'] = location.Location(-1, 0, 0, reference=system)
        f.move_in_system()
        self.assertEqual(f.location.xyz, (-1, 0, 0))

    def test_repair1(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].armor_damage = 15
        f.ships[0].armor = 100
        f.ships[0].repair = 10
        f.repair()
        self.assertEqual(f.ships[0].armor_damage, 5)

    def test_repair2(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].armor_damage = 15
        f.ships[0].armor = 100
        f.ships[0].repair = 10
        f.ships[0].hull.repair = 5
        f.__cache__['moved'] = True
        f.repair()
        self.assertEqual(f.ships[0].armor_damage, 10)

    def test_repair3(self):
        f = fleet.Fleet() + [ship.Ship(), ship.Ship()]
        f.ships[0].armor_damage = 10
        f.ships[0].armor = 100
        f.ships[0].repair = 5
        f.ships[1].armor_damage = 10
        f.ships[1].armor = 20
        f.ships[1].repair = 5
        f.repair()
        self.assertEqual(f.ships[0].armor_damage, 9)
        self.assertEqual(f.ships[1].armor_damage, 1)

    def test_damage_level1(self):
        f = fleet.Fleet() + [ship.Ship(), ship.Ship()]
        f.ships[0].armor_damage = 10
        f.ships[0].armor = 100
        f.ships[1].armor_damage = 10
        f.ships[1].armor = 20
        self.assertEqual(f.damage_level(), 20 / 120)

    def test_orbital_extraction1(self):
        f = fleet.Fleet() + ship.Ship(cargo_max=100)
        with patch.object(planet.Planet, 'extract_minerals') as mock:
            f.orbital_extraction()
            self.assertEqual(mock.call_count, 0)

    def test_orbital_extraction2(self):
        f = fleet.Fleet() + ship.Ship(cargo_max=100, extraction_rate=20)
        with patch.object(planet.Planet, 'extract_minerals') as mock:
            f.orbital_extraction()
            self.assertEqual(mock.call_count, 0)

    def test_orbital_extraction3(self):
        f = fleet.Fleet() + ship.Ship(cargo_max=100, extraction_rate=20)
        p = planet.Planet()
        f.location = location.Location(reference=p)
        t = tech.Tech(extraction_rate=20)
        f.ships[0].add_component(t)
        m = minerals.Minerals(titanium=10, lithium=10, silicon=10)
        with patch.object(planet.Planet, 'extract_minerals', return_value=m) as mock:
            f.orbital_extraction()
            self.assertEqual(f._stats().cargo.sum(), 30)

    def test_lay_mines1(self):
        f = fleet.Fleet() + ship.Ship()
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f.location = location.Location(reference=s)
        f.lay_mines()
        self.assertEqual(s.minefield, 0)

    def test_lay_mines2(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].mines_laid = 100
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f.lay_mines()
        self.assertEqual(s.minefield, 0)

    def test_lay_mines3(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].mines_laid = 100
        f.__cache__['moved'] = True
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f.location = location.Location(reference=s)
        f.lay_mines()
        self.assertEqual(s.minefield, 0)

    def test_lay_mines4(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].mines_laid = 100
        s = star_system.StarSystem(location=location.Location(is_system=True))
        f.location = location.Location(reference=s)
        f.lay_mines()
        self.assertEqual(s.minefield, 1)

    def test_bomb1(self):
        f = fleet.Fleet() + ship.Ship()
        p = planet.Planet()
        f.location = location.Location(reference=p)
        with patch.object(planet.Planet, 'bomb') as mock:
            f.bomb()
            self.assertEqual(mock.call_count, 0)

    def test_bomb2(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].bombs.append(bomb.Bomb(percent_pop_kill=10))
        p = planet.Planet()
        with patch.object(planet.Planet, 'bomb') as mock:
            f.bomb()
            self.assertEqual(mock.call_count, 0)

    def test_bomb3(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].bombs.append(bomb.Bomb(percent_pop_kill=10))
        p = planet.Planet()
        f.location = location.Location(reference=p)
        with patch.object(planet.Planet, 'bomb') as mock:
            f.bomb()
            self.assertEqual(mock.call_count, 0)

    def test_bomb4(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].bombs.append(bomb.Bomb(percent_pop_kill=10))
        p = planet.Planet()
        p.on_surface.people = 100000
        f.location = location.Location(reference=p)
        with patch.object(planet.Planet, 'bomb') as mock:
            with patch.object(player.Player, 'get_relation', return_value='me'):
                f.bomb()
            self.assertEqual(mock.call_count, 0)

    def test_bomb5(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].bombs.append(bomb.Bomb(percent_pop_kill=10))
        f.ships[0].bombs.append(bomb.Bomb(percent_pop_kill=10))
        p = planet.Planet()
        p.on_surface.people = 100000
        f.location = location.Location(reference=p)
        with patch.object(planet.Planet, 'bomb') as mock:
            with patch.object(player.Player, 'get_relation', return_value='enemy'):
                f.bomb()
            self.assertEqual(mock.call_count, 2)

    def test_piracy1(self):
        pass #TODO

    def test_unload1(self):
        f = fleet.Fleet() + ship.Ship()
        f.__cache__['moved'] = True
        with patch.object(fleet.Fleet, '_other_cargo') as mock:
            f.unload()
            self.assertEqual(mock.call_count, 0)

    def test_unload2(self):
        f = fleet.Fleet() + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f2 = fleet.Fleet() + ship.Ship(cargo_max=10)
        f2.ships[0].player = reference.Reference(player.Player())
        f.location = location.Location(reference=f2)
        f.order.unload_ti = 1
        f.order.unload_li = 0
        f.order.unload_si = -1
        f.unload()
        self.assertEqual(f._stats().cargo.sum(), 6)
        self.assertEqual(f2._stats().cargo.sum(), 0)

    def test_unload3(self):
        f = fleet.Fleet() + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f2 = fleet.Fleet() + ship.Ship(cargo_max=0)
        f2.ships[0].player = f.ships[0].player
        f.location = location.Location(reference=f2)
        f.order.unload_ti = 1
        f.order.unload_li = 0
        f.order.unload_si = -1
        f.unload()
        self.assertEqual(f._stats().cargo.sum(), 6)
        self.assertEqual(f2._stats().cargo.sum(), 0)

    def test_unload4(self):
        f = fleet.Fleet() + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f2 = fleet.Fleet() + ship.Ship(cargo_max=10)
        f2.ships[0].player = f.ships[0].player
        f.location = location.Location(reference=f2)
        f.order.unload_ti = 1
        f.order.unload_li = 0
        f.order.unload_si = -1
        f.unload()
        self.assertEqual(f._stats().cargo.sum(), 3)
        self.assertEqual(f2._stats().cargo.sum(), 3)

    def test_unload5(self):
        f = fleet.Fleet() + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        p = planet.Planet()
        p.player = f.ships[0].player
        f.location = location.Location(reference=p)
        f.order.unload_ti = 1
        f.order.unload_li = 0
        f.order.unload_si = -1
        f.unload()
        self.assertEqual(f._stats().cargo.sum(), 3)
        self.assertEqual(p.on_surface.sum(), 3)

    def test_buy1(self):
        pass #TODO

    def test_scrap1(self):
        pass #TODO

    def test_load1(self):
        f = fleet.Fleet() + ship.Ship()
        f.__cache__['moved'] = True
        with patch.object(fleet.Fleet, '_other_cargo') as mock:
            f.load()
            self.assertEqual(mock.call_count, 0)

    def test_load2(self):
        f = fleet.Fleet() + ship.Ship(cargo_max=10)
        f2 = fleet.Fleet() + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f2.ships[0].player = reference.Reference(player.Player())
        f.location = location.Location(reference=f2)
        f.order.load_ti = 1
        f.order.load_li = 0
        f.order.load_si = -1
        f.load()
        self.assertEqual(f._stats().cargo.sum(), 0)
        self.assertEqual(f2._stats().cargo.sum(), 6)

    def test_load3(self):
        f = fleet.Fleet() + ship.Ship(cargo_max=0)
        f2 = fleet.Fleet() + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f2.ships[0].player = f.ships[0].player
        f.location = location.Location(reference=f2)
        f.order.load_ti = 1
        f.order.load_li = 0
        f.order.load_si = -1
        f.load()
        self.assertEqual(f._stats().cargo.sum(), 0)
        self.assertEqual(f2._stats().cargo.sum(), 6)

    def test_load4(self):
        f = fleet.Fleet() + ship.Ship(cargo_max=10)
        f2 = fleet.Fleet() + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f2.ships[0].player = f.ships[0].player
        f.location = location.Location(reference=f2)
        f.order.load_ti = 1
        f.order.load_li = 0
        f.order.load_si = -1
        f.load()
        self.assertEqual(f._stats().cargo.sum(), 3)
        self.assertEqual(f2._stats().cargo.sum(), 3)

    def test_load5(self):
        f = fleet.Fleet() + ship.Ship(cargo_max=10)
        p = planet.Planet(on_surface=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        p.player = f.ships[0].player
        f.location = location.Location(reference=p)
        f.order.load_ti = 1
        f.order.load_li = 0
        f.order.load_si = -1
        f.load()
        self.assertEqual(f._stats().cargo.sum(), 3)
        self.assertEqual(p.on_surface.sum(), 3)





    def test_transfer1(self):
        pass #TODO



    def test_stargate_check1(self):
        pass #TODO method is also todo

    def test_fuel_calc1(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].engines = [engine.Engine(), engine.Engine()]
        with patch.object(engine.Engine, 'fuel_calc', return_value=200):
            self.assertEqual(f._fuel_calc(1, 2, 3), 400)

    def test_damage_check1(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].engines = [engine.Engine(), engine.Engine()]
        with patch.object(engine.Engine, 'tachometer', return_value=100):
            self.assertFalse(f._damage_check(1, 2))

    def test_damage_check2(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].engines = [engine.Engine(), engine.Engine()]
        with patch.object(engine.Engine, 'tachometer', return_value=101):
            self.assertTrue(f._damage_check(1, 2))

    def test_fuel_distribution1(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.ships[0].fuel_max = 100
        f.ships[1].fuel_max = 200
        stats = f._stats()
        stats.fuel = 151
        f._fuel_distribution()
        self.assertEqual(f.ships[0].fuel, 51)
        self.assertEqual(f.ships[1].fuel, 100)

    def test_fuel_distribution2(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.ships[0].fuel_max = 111
        f.ships[1].fuel_max = 200
        stats = f._stats()
        stats.fuel = 311
        f._fuel_distribution()
        self.assertEqual(f.ships[0].fuel, 111)
        self.assertEqual(f.ships[1].fuel, 200)

    def test_cargo_distribution1(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.ships[0].cargo_max = 200
        f.ships[1].cargo_max = 400
        stats = f._stats()
        stats.cargo = cargo.Cargo(titanium=151, silicon=151, lithium=149, people=149)
        f._cargo_distribution()
        self.assertEqual(f.ships[0].cargo, cargo.Cargo(titanium=51, silicon=50, lithium=50, people=49))
        self.assertEqual(f.ships[1].cargo, cargo.Cargo(titanium=100, silicon=101, lithium=99, people=100))

    def test_cargo_distribution2(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.ships[0].cargo_max = 100
        f.ships[1].cargo_max = 1000
        stats = f._stats()
        stats.cargo = cargo.Cargo(titanium=276, silicon=276, lithium=274, people=274)
        f._cargo_distribution()
        self.assertEqual(f.ships[0].cargo, cargo.Cargo(titanium=26, silicon=25, lithium=25, people=24))
        self.assertEqual(f.ships[1].cargo, cargo.Cargo(titanium=250, silicon=251, lithium=249, people=250))



'''
    def test_merge_1(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet(ships = [ship_1])
        fleet_two = fleet.Fleet(
            ships = [ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['merge'],
                recipiants = {'merge': fleet_one}
                )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.merge(p1)
        self.assertEqual(len(p1.fleets), 1)
        self.assertEqual(ship_2 in fleet_one.ships, True)

    def test_merge_2(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet(ships = [ship_1])
        fleet_two = fleet.Fleet(
            ships = [ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['merge'],
                recipiants = {'merge': fleet_one}
                )])
        p1 = player.Player(fleets = [fleet_one])
        p2 = player.Player(fleets = [fleet_two])
        fleet_two.merge(p2)
        self.assertEqual(len(p1.fleets), 1)
        self.assertEqual(ship_2 in fleet_two.ships, True)
        
    def test_split_1(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['split'],
                splits = [[ship_2]]
                )])
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.split(p1)
        self.assertEqual(ship_1 in fleet_one.ships, True)
        self.assertEqual(ship_2 in p1.fleets[1].ships, True)
        self.assertEqual(len(fleet_one.ships), 1)
    
    def test_split_2(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['split'],
                splits = [[ship_2, ship_1]]
                )])
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.split(p1)
        self.assertEqual(len(p1.fleets), 1)
        self.assertEqual(ship_1 in p1.fleets[0].ships, True)
        self.assertEqual(ship_2 in p1.fleets[0].ships, True)
        self.assertEqual(len(fleet_one.ships), 0)
        
    def test_split_3(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['split'],
                splits = [[ship_2], [ship_1]]
                )])
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.split(p1)
        self.assertEqual(ship_1 in p1.fleets[1].ships, True)
        self.assertEqual(ship_2 in p1.fleets[0].ships, True)
        self.assertEqual(len(fleet_one.ships), 0)
        
    def test_transfer(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        p2 = player.Player()
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['transfer'],
                recipiants = {'transfer':p2}
                )])
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.transfer(p1)
        self.assertEqual(fleet_one in p2.fleets, True)
    
    def test_hyper_denial(self):
        return # TODO
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['deploy_hyper_denial'],
                    )])
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.execute('deploy_hyper_denial', p1)
        self.assertEqual(True, False, "Not Testing")
    
    def test_move_1(self):
        ship_1 = ship.Ship(
            fuel = 0,
            fuel_max = 100,
            mass = 100,
            engines = [engine.Engine(kt_exponent = 1.5, speed_divisor = 10.0, speed_exponent = 5.0) for i in range(2)]
            )
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(speed = 5),
                waypoint.Waypoint(
                    location = location.Location(x = 1),
                    speed = 5
                    ),
                waypoint.Waypoint(
                    location = location.Location(x = 1),
                    speed = 5
                    )])
        p1 = player.Player(fleets = [fleet_one])
        for i in range(100):
            fleet_one.move(p1)
        self.assertEqual(fleet_one.location == location.Location(x = 1), True)
        self.assertEqual(len(fleet_one.waypoints), 3)
    
    def test_move_2(self):
        ship_1 = ship.Ship(
            fuel = 0,
            fuel_max = 100,
            mass = 10000,
            engines = [engine.Engine(kt_exponent = 1.5, speed_divisor = 10.0, speed_exponent = 5.0) for i in range(2)]
            )
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(speed = 5),
                waypoint.Waypoint(
                    location = location.Location(x = .0025),
                    speed = 5
                    ),
                waypoint.Waypoint(speed = 5)
                ])
        p1 = player.Player(fleets = [fleet_one])
        for i in range(1):
            fleet_one.move(p1)
        self.assertEqual(fleet_one.location == location.Location(x = .0025), True)
        self.assertEqual(len(fleet_one.waypoints), 3)
    
    def test_move_on(self):
        ship_1 = ship.Ship(
            fuel = 100,
            fuel_max = 100,
            mass = 100,
            engines = [engine.Engine(kt_exponent = 1.5, speed_divisor = 10.0, speed_exponent = 5.0) for i in range(2)]
            )
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(speed = 5),
                waypoint.Waypoint(speed = 5),
                waypoint.Waypoint(speed = 5, location = location.Location(x=1))
                ])
        p1 = player.Player(fleets = [fleet_one])
        for i in range(1):
            fleet_one.move(p1)
        self.assertEqual(fleet_one.location == location.Location(x = 25/100), True)
        self.assertEqual(len(fleet_one.waypoints), 2)
    
    def test_move_3(self):
        ship_3 = ship.Ship(
            fuel = 1000,
            fuel_max = 10000,
            mass = 100,)
        fleet_one = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(speed = 5),
                waypoint.Waypoint(
                    location = location.Location(x = 1, y = 1, z = 1),
                    speed = 2
                    )])
        p1 = player.Player(fleets = [fleet_one])
        for i in range(2):
            fleet_one.move(p1)
        self.assertEqual(fleet_one.location == location.Location(), True)
    
        fleet_one.location = location.Location()
        ship_1.location = location.Location()
        ship_2 = ship.Ship(
            fuel = 1000,
            fuel_max = 10000,
            mass = 100,
            engines = [engine.Engine(kt_exponent = 1.5, speed_divisor = 10.0, speed_exponent = 5.0) for i in range(2)]
            )
        fleet_one.add_ships([ship_2])
        fleet_one.waypoints[1] = waypoint.Waypoint(
            location = location.Location(x = 24/100, y = 7/100, z = 0),
            speed = 5
            )
        fleet_one.waypoints.append(waypoint.Waypoint(
            location = location.Location(x = 24/100, y = 14/100, z = 24),
            speed = 1
            ))
        for i in range(1):
            fleet_one.execute('move', p1)
        self.assertEqual(fleet_one.location == location.Location(x = 24/100, y = 7/100), True)
        fleet_one = fleet.Fleet(
            ships = [ship_2],
            waypoints = [
                waypoint.Waypoint(speed = 1),
                waypoint.Waypoint(
                    location = location.Location(x = 1, y = 1, z = 1),
                    speed = 10,
                    standoff = 'No Standoff'
                    ),
                waypoint.Waypoint(
                    location = location.Location(x = 2, y = 1, z = 1),
                    standoff = 'No Standoff',
                    speed = 1
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_one])
        '#''
        for i in range(9):
            fleet_one.move(p1)
        self.assertEqual(fleet_one.location.x, 1)
        self.assertEqual(fleet_one.location.y, 1)
        self.assertEqual(fleet_one.location.z, 1)
        
    def test_handle_cargo_10(self):
        fleet_1 = fleet.Fleet()
        unload_fuel = 100
        load_fuel_max = 100
        amount = fleet_1.handle_cargo(unload_fuel, 0, load_fuel_max, 'fuel', 30, cargo.Cargo(), 0, cargo.Cargo())
        self.assertEqual(amount, 30)
        
    def test_handle_cargo_11(self):
        fleet_1 = fleet.Fleet()
        unload_fuel = 7
        load_fuel_max = 100
        amount = fleet_1.handle_cargo(unload_fuel, 0, load_fuel_max, 'fuel', 30, cargo.Cargo(), 0, cargo.Cargo())
        self.assertEqual(amount, 7)
        
    def test_handle_cargo_12(self):
        fleet_1 = fleet.Fleet()
        unload_fuel = 100
        load_fuel_max = 20
        amount = fleet_1.handle_cargo(unload_fuel, 0, load_fuel_max, 'fuel', 30, cargo.Cargo(), 0, cargo.Cargo())
        self.assertEqual(amount, 20)
        
    def test_handle_cargo_20(self):
        fleet_1 = fleet.Fleet()
        load_cargo_max = 100
        unload_cargo = cargo.Cargo()
        for item in ['titanium', 'silicon', 'lithium', 'people']:
            unload_cargo[item] = 100
            amount = fleet_1.handle_cargo(0, 0, 0, item, 30, cargo.Cargo(), load_cargo_max, unload_cargo)
            self.assertEqual(amount, 30)
        
    def test_handle_cargo_21(self):
        fleet_1 = fleet.Fleet()
        load_cargo_max = 100
        unload_cargo = cargo.Cargo()
        for item in ['titanium', 'silicon', 'lithium', 'people']:
            unload_cargo[item] = 15
            amount = fleet_1.handle_cargo(0, 0, 0, item, 30, cargo.Cargo(), load_cargo_max, unload_cargo)
            self.assertEqual(amount, 15)
        
    def test_handle_cargo_22(self):
        fleet_1 = fleet.Fleet()
        load_cargo_max = 8
        unload_cargo = cargo.Cargo()
        for item in ['titanium', 'silicon', 'lithium', 'people']:
            unload_cargo[item] = 100
            amount = fleet_1.handle_cargo(0, 0, 0, item, 30, cargo.Cargo(), load_cargo_max, unload_cargo)
            self.assertEqual(amount, 8)
        
    def test_check_trade_10(self):
        p1 = player.Player()
        fleet_treaty = treaty.Treaty(
            relation = 'team',
            other_player = reference.Reference(p1),
            status = 'active',
            )
        ultimantico = planet.Planet(player = reference.Reference(p1))
        fleet_three = fleet.Fleet()
        p2 = player.Player(fleets = [fleet_three])
        p2.treaties.append(fleet_treaty)
        p1.treaties.append(fleet_treaty.for_other_player(p2))
        test = fleet_three.check_trade(ultimantico, p2)
        self.assertEqual(test, True)
    
    def test_check_trade_11(self):
        p1 = player.Player()
        fleet_treaty = treaty.Treaty(
            relation = 'neutral',
            other_player = reference.Reference(p1),
            status = 'active',
            )
        ultimantico = planet.Planet(player = reference.Reference(p1))
        fleet_three = fleet.Fleet()
        p2 = player.Player(fleets = [fleet_three])
        p2.treaties.append(fleet_treaty)
        p1.treaties.append(fleet_treaty.for_other_player(p2))
        test = fleet_three.check_trade(ultimantico, p2)
        self.assertEqual(test, True)
    
    def test_check_trade_20(self):
        p1 = player.Player()
        fleet_treaty = treaty.Treaty(
            relation = 'team',
            other_player = reference.Reference(p1),
            status = 'pending',
            )
        print(fleet_treaty.status)
        ultimantico = planet.Planet(player = reference.Reference(p1))
        fleet_three = fleet.Fleet()
        p2 = player.Player(fleets = [fleet_three])
        p2.treaties.append(fleet_treaty)
        p1.treaties.append(fleet_treaty.for_other_player(p2))
        test = fleet_three.check_trade(ultimantico, p2)
        self.assertEqual(test, True)
    
    def test_check_trade_21(self):
        p1 = player.Player()
        fleet_treaty = treaty.Treaty(
            relation = 'enemy',
            other_player = reference.Reference(p1),
            status = 'active',
            )
        ultimantico = planet.Planet(player = reference.Reference(p1))
        fleet_three = fleet.Fleet()
        p2 = player.Player(fleets = [fleet_three])
        p2.treaties.append(fleet_treaty)
        p1.treaties.append(fleet_treaty.for_other_player(p2))
        test = fleet_three.check_trade(ultimantico, p2)
        self.assertEqual(test, False)
    
    def test_check_trade_22(self):
        p1 = player.Player()
        ultimantico = planet.Planet(player = reference.Reference(p1))
        fleet_three = fleet.Fleet()
        p2 = player.Player(fleets = [fleet_three])
        test = fleet_three.check_trade(ultimantico, p2)
        self.assertEqual(test, True)
    
    def test_check_trade_30(self):
        ultimantico = ship.Ship()
        fleet_three = fleet.Fleet()
        p2 = player.Player(fleets = [fleet_three])
        test = fleet_three.check_trade(ultimantico, p2)
        self.assertEqual(test, False)
    
    def test_check_self_1(self):
        p1 = player.Player()
        ultimantico = planet.Planet(player = reference.Reference(p1))
        fleet_three = fleet.Fleet()
        p1.fleets = [fleet_three]
        test = fleet_three.check_self(ultimantico, p1)
        self.assertEqual(test, True)
    
    def test_check_self_2(self):
        ultimantico = planet.Planet()
        fleet_three = fleet.Fleet()
        p1 = player.Player(fleets = [fleet_three])
        test = fleet_three.check_self(ultimantico, p1)
        self.assertEqual(test, False)
    
    def test_check_self_3(self):
        fleet_one = fleet.Fleet()
        fleet_three = fleet.Fleet()
        p1 = player.Player(fleets = [fleet_three])
        test = fleet_three.check_self(fleet_one, p1)
        self.assertEqual(test, False)
    
    def test_check_self_4(self):
        fleet_one = fleet.Fleet()
        fleet_three = fleet.Fleet()
        p1 = player.Player(fleets = [fleet_one, fleet_three])
        test = fleet_three.check_self(fleet_one, p1)
        self.assertEqual(test, True)
    
    def test_buy_minerals(self):
        return #TODO
        p1 = player.Player(
            finance_minister_construction_percent = 0,
            finance_minister_mattrans_percent = 0,
            finance_minister_research_percent = 0,
            energy = 1000
            )
        fleet_treaty = treaty.Treaty(
            relation = 'team',
            other_player = reference.Reference(p1),
            status = 'active',
            buy_si = 3
            )
        p2 = player.Player(
            finance_minister_construction_percent = 0,
            finance_minister_mattrans_percent = 0,
            finance_minister_research_percent = 0,
            energy = 1000
            )
        p2.treaties.append(fleet_treaty)
        p1.treaties.append(fleet_treaty.for_other_player(p2))
        ultimantico = planet.Planet(
            player = reference.Reference(p1),
            space_stations = [
                fleet.Fleet(
                    ships = [
                        space_station.SpaceStation(is_trading_post = True)
                        ])
                ],
            on_surface = cargo.Cargo(silicon = 100, cargo_max = -1)
            )
        ship_1 = ship.Ship(cargo = cargo.Cargo(silicon = 100, cargo_max = 1000))
        fleet_three = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['buy'],
                    transfers = {'buy':[['silicon', 50]]},
                    recipiants = {'buy':ultimantico},
                    )])
        p2.fleets = [fleet_three]
        p1.allocate_budget()
        p2.allocate_budget()
        fleet_three.buy(p2)
        self.assertEqual(p1.energy, 1150)
        self.assertEqual(p2.energy, 850)
        self.assertEqual(ultimantico.on_surface.silicon, 50)
        self.assertEqual(ship_1.cargo.silicon, 150)
        
    def test_buy_fuel(self):
        return #TODO
        p1 = player.Player(
            finance_minister_construction_percent = 0,
            finance_minister_mattrans_percent = 0,
            finance_minister_research_percent = 0,
            energy = 1000
            )
        fleet_treaty = treaty.Treaty(
            relation = 'team',
            other_player = reference.Reference(p1),
            status = 'active',
            buy_fuel = 2
            )
        p2 = player.Player(
            finance_minister_construction_percent = 0,
            finance_minister_mattrans_percent = 0,
            finance_minister_research_percent = 0,
            energy = 1000
            )
        p2.treaties.append(fleet_treaty)
        p1.treaties.append(fleet_treaty.for_other_player(p2))
        ultimantico = planet.Planet(
            player = reference.Reference(p1),
            space_stations = [
                fleet.Fleet(
                    ships = [
                        space_station.SpaceStation(
                            fuel = 100000,
                            is_trading_post = True,
                            fuel_max = 500000
                            )])])
        ship_1 = ship.Ship(
            fuel = 10000,
            fuel_max = 30000
            )
        fleet_three = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['buy'],
                    transfers = {'buy':[['fuel', 50]]},
                    recipiants = {'buy':ultimantico},
                    )])
        p2.fleets = [fleet_three]
        p1.allocate_budget()
        p2.allocate_budget()
        fleet_three.buy(p2)
        self.assertEqual(p1.energy, 1100)
        self.assertEqual(p2.energy, 900)
        self.assertEqual(ultimantico.space_stations[0].fuel, 99950)
        self.assertEqual(ship_1.fuel, 10050)
        
    def test_sell_minerals(self):
        return #TODO
        p1 = player.Player(
            finance_minister_construction_percent = 0,
            finance_minister_mattrans_percent = 0,
            finance_minister_research_percent = 0,
            energy = 1000
            )
        fleet_treaty = treaty.Treaty(
            relation = 'team',
            other_player = reference.Reference(p1),
            status = 'active',
            sell_si = 7
            )
        p2 = player.Player(
            finance_minister_construction_percent = 0,
            finance_minister_mattrans_percent = 0,
            finance_minister_research_percent = 0,
            energy = 1000
            )
        p2.treaties.append(fleet_treaty)
        p1.treaties.append(fleet_treaty.for_other_player(p2))
        ultimantico = planet.Planet(
            player = reference.Reference(p1),
            space_stations = [
                fleet.Fleet(
                    ships = [
                        space_station.SpaceStation(is_trading_post = True)
                        ])
                ],
            on_surface = cargo.Cargo(
                silicon = 100,
                cargo_max = -1
                ))
        ship_1 = ship.Ship(cargo = cargo.Cargo(silicon=100, cargo_max=1000))
        fleet_three = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['sell'],
                    transfers = {'sell':[['silicon', 50]]},
                    recipiants = {'sell':ultimantico},
                    )])
        p2.fleets = [fleet_three]
        p1.allocate_budget()
        p2.allocate_budget()
        fleet_three.sell(p2)
        self.assertEqual(p1.energy, 650)
        self.assertEqual(p2.energy, 1350)
        self.assertEqual(ultimantico.on_surface.silicon, 150)
        self.assertEqual(ship_1.cargo.silicon, 50)
        
    def test_sell_fuel(self):
        return #TODO
        p1 = player.Player(
            finance_minister_construction_percent = 0,
            finance_minister_mattrans_percent = 0,
            finance_minister_research_percent = 0,
            energy = 1000
            )
        fleet_treaty = treaty.Treaty(
            relation = 'team',
            other_player = reference.Reference(p1),
            status = 'active',
            sell_fuel = 2
            )
        p2 = player.Player(
            finance_minister_construction_percent = 0,
            finance_minister_mattrans_percent = 0,
            finance_minister_research_percent = 0,
            energy = 1000
            )
        p2.treaties.append(fleet_treaty)
        p1.treaties.append(fleet_treaty.for_other_player(p2))
        ultimantico = planet.Planet(
            player = reference.Reference(p1),
            space_stations = [
                fleet.Fleet(
                    ships = [
                        space_station.SpaceStation(
                            fuel = 100000,
                            is_trading_post = True,
                            fuel_max = 500000
                            )])])
        ship_1 = ship.Ship(
            fuel = 10000,
            fuel_max = 30000
            )
        fleet_three = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['sell'],
                    transfers = {'sell':[['fuel', 50]]},
                    recipiants = {'sell':ultimantico},
                    )])
        p2.fleets = [fleet_three]
        p1.allocate_budget()
        p2.allocate_budget()
        fleet_three.sell(p2)
        self.assertEqual(p1.energy, 900)
        self.assertEqual(p2.energy, 1100)
        self.assertEqual(ultimantico.space_stations[0].fuel, 100050)
        self.assertEqual(ship_1.fuel, 9950)
        
    def test_unload_fleet_cargo(self):
        ship_1 = ship.Ship(
            cargo = cargo.Cargo(cargo_max = 200)
            )
        fleet_one = fleet.Fleet(ships = [ship_1])
        ship_2 = ship.Ship(
            cargo = cargo.Cargo(silicon = 100, cargo_max = 300)
            )
        fleet_two = fleet.Fleet(
            ships = [ship_2],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['unload'],
                    transfers = {'unload':[['silicon', 40]]},
                    recipiants = {'unload':fleet_one},
                    )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.unload(p1)
        self.assertEqual(ship_1.cargo.silicon, 40)
        self.assertEqual(ship_2.cargo.silicon, 60)
    
    def test_unload_fleet_fuel(self):
        ship_1 = ship.Ship(
            fuel_max = 200
            )
        fleet_one = fleet.Fleet(ships = [ship_1])
        ship_2 = ship.Ship(
            fuel = 100,
            fuel_max = 300
            )
        fleet_two = fleet.Fleet(
            ships = [ship_2],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['unload'],
                    transfers = {'unload':[['fuel', 40]]},
                    recipiants = {'unload':fleet_one},
                    )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.unload(p1)
        self.assertEqual(ship_1.fuel, 40)
        self.assertEqual(ship_2.fuel, 60)
    
    def test_load_fleet_cargo(self):
        ship_1 = ship.Ship(
            cargo = cargo.Cargo(silicon = 100, cargo_max = 200)
            )
        fleet_one = fleet.Fleet(ships = [ship_1])
        ship_2 = ship.Ship(
            cargo = cargo.Cargo(cargo_max = 300)
            )
        fleet_two = fleet.Fleet(
            ships = [ship_2],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['load'],
                    transfers = {'load':[['silicon', 60]]},
                    recipiants = {'load':fleet_one},
                    )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.load(p1)
        self.assertEqual(ship_1.cargo.silicon, 40)
        self.assertEqual(ship_2.cargo.silicon, 60)
    
    def test_load_fleet_fuel(self):
        ship_1 = ship.Ship(
            fuel = 100,
            fuel_max = 200
            )
        fleet_one = fleet.Fleet(ships = [ship_1])
        ship_2 = ship.Ship(
            fuel_max = 300
            )
        fleet_two = fleet.Fleet(
            ships = [ship_2],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['load'],
                    transfers = {'load':[['fuel', 60]]},
                    recipiants = {'load':fleet_one},
                    )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.load(p1)
        self.assertEqual(ship_1.fuel, 40)
        self.assertEqual(ship_2.fuel, 60)
    
    def test_unload_planet_cargo(self):
        ship_1 = ship.Ship(cargo = cargo.Cargo(people = 100, cargo_max = 200))
        p1 = player.Player()
        ultimantico = planet.Planet(on_surface = cargo.Cargo(people = 100, cargo_max = -1))
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['unload'],
                    transfers = {'unload': [['people', 40]]},
                    recipiants = {'unload': ultimantico},
                    )])
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.unload(p1)
        self.assertEqual(ship_1.cargo.people, 60)
        self.assertEqual(ultimantico.on_surface.people, 140)
    
    def test_unload_planet_fuel(self):
        return #TODO
        ship_1 = ship.Ship(
            fuel = 100,
            fuel_max = 200
            )
        p1 = player.Player()
        ultimantico = planet.Planet(
            space_stations = [
                fleet.Fleet(
                    ships = [
                        space_station.SpaceStation(
                            fuel_max = 1000,
                            fuel = 100
                            )])])
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['unload'],
                    transfers = {'unload': [['fuel', 40]]},
                    recipiants = {'unload': ultimantico}
                    )])
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.unload(p1)
        self.assertEqual(ship_1.fuel, 60)
        self.assertEqual(ultimantico.space_stations[0].fuel, 140)
    
    def test_load_planet_cargo(self):
        ship_1 = ship.Ship(cargo = cargo.Cargo(people = 100, cargo_max = 200))
        p1 = player.Player()
        ultimantico = planet.Planet(on_surface = cargo.Cargo(people = 100, cargo_max = -1))
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['load'],
                    transfers = {'load': [['people', 60]]},
                    recipiants = {'load': ultimantico},
                    )])
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.load(p1)
        self.assertEqual(ship_1.cargo.people, 160)
        self.assertEqual(ultimantico.on_surface.people, 40)
    
    def test_load_planet_fuel(self):
        return #TODO
        ship_1 = ship.Ship(
            fuel = 100,
            fuel_max = 200
            )
        p1 = player.Player()
        ultimantico = planet.Planet(
            space_stations = [
                fleet.Fleet(
                    ships = [
                        space_station.SpaceStation(
                            fuel_max = 1000,
                            fuel = 100
                    )])])
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['load'],
                    transfers = {'load': [['fuel', 60]]},
                    recipiants = {'load': ultimantico},
                    )])
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.load(p1)
        self.assertEqual(ship_1.fuel, 160)
        self.assertEqual(ultimantico.space_stations[0].fuel, 40)
    
    def test_self_repair(self):
        return # TODO
        ship_3 = ship.Ship(
            repair = 3,
            damage_armor = 7,
            armor = 10,
            )
        ship_4 = ship.Ship(
            repair = 3,
            damage_armor = 7,
            armor = 20,
            )
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['self_repair'],
                    )])
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('self_repair', p1)
    
    def test_repair(self):
        return # TODO
        ship_3 = ship.Ship(
            repair_bay = 3,
            damage_armor = 7,
            armor = 10,
            )
        ship_4 = ship.Ship(
            repair_bay = 3,
            damage_armor = 7,
            armor = 20,
            )
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['repair'],
                    )])
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('repair', p1)
    
    def test_orbital_mining_1(self):
        ultimantico = planet.Planet(
            remaining_minerals = minerals.Minerals(titanium = 40000),
            gravity = 50,
            on_surface = cargo.Cargo(people = 1)
            )
        ship_3 = ship.Ship(
            mining_rate = 1.6,
            percent_wasted = 1.4,
            )
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['orbital_mining'],
                    recipiants = {'orbital_mining': ultimantico}
                    )])
        p1 = player.Player(fleets = [fleet_two])
        ultimantico.colonize(p1)
        fleet_two.orbital_mining()
        self.assertEqual(ultimantico.on_surface.titanium, 0)
        self.assertEqual(ultimantico.remaining_minerals.titanium, 40000)
    
    def test_orbital_mining_2(self):
        ultimantico = planet.Planet(
            remaining_minerals = minerals.Minerals(titanium = 40000),
            gravity = 50
            )
        ship_3 = ship.Ship(
            mining_rate = 1.6,
            percent_wasted = 1.4,
            )
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['orbital_mining'],
                    recipiants = {'orbital_mining': ultimantico}
                    )])
        fleet_two.orbital_mining()
        self.assertEqual(ultimantico.on_surface.titanium, 16)
        self.assertEqual(ultimantico.remaining_minerals.titanium, 39977)
        
    def test_orbital_mining_3(self):
        ultimantico = ship.Ship()
        ship_3 = ship.Ship()
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['orbital_mining'],
                    recipiants = {'orbital_mining': ultimantico}
                    )])
        is_planet = fleet_two.orbital_mining()
        self.assertEqual(is_planet, False)
        
    def test_lay_mines(self):
        return # TODO
        p1 = player.Player(name = 'caltorez')
        system = star_system.StarSystem(
            mines = {p1.name: 0},
            planets = [
                planet.Planet(gravity = 70),
                planet.Planet(gravity = 50),
                planet.Planet(gravity = 30),
                planet.Planet(gravity = 50),
                planet.Planet(gravity = 50)
                ]
            )
        ship_3 = ship.Ship(mines_laid = 500000000000)
        ship_4 = ship.Ship(mines_laid = 500000000000)
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['lay_mines'],
                    recipiants = {'lay_mines': system},
                    location = location.Location()
                    )
                ]
            )
        p1.fleets = [fleet_two]
        fleet_two.execute('lay_mines', p1)
        self.assertEqual(system.mines[p1.name], 1000000000000)
        print('dencity', 1000000000000 / (100 ** 3))
        print('sweep', system.sweep_mines(120, 1, 0.3, 'caltorez'))
        print('hit', system.mines_hit(300, 100, 'caltorez'))
        system.mines_decay()
        self.assertEqual(system.mines['caltorez'], 985000000000)
        
    def test_bomb(self):
        return # activate when pulled Pam's fixes to bomb.py
        ultimantico = planet.Planet()
        ultimantico.on_surface.people = 200
        p1 = player.Player()
        ultimantico.colonize(p1)
        bombs = []
        for i in range(101):
            bombs.append(bomb.Bomb(percent_pop_kill = 0.2, shield_kill = 20, max_defense = 85))
        ship_3 = ship.Ship(bombs = bombs)
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['bomb'],
                    location = location.Location(),
                    recipiants = {'bomb': ultimantico})])
        p2 = player.Player(fleets = [fleet_two])
        p2.treaties.append(treaty.Treaty(relation = 'enemy', status = 'active', other_player = reference.Reference(p1)))
        fleet_two.execute('bomb', p2)
        self.assertLess(ultimantico.on_surface.people, 120, 'NOTE: this will somtimes fail as it is statistical in nature')
    
    def test_colonize_1(self):
        ultimantico = planet.Planet()
        ship_3 = ship.Ship(
            cargo = cargo.Cargo(people = 100, cargo_max = 200),
            colonizer = True
            )
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['colonize'],
                    recipiants = {'colonize': ultimantico},
                )])
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.colonize(p1)
        self.assertEqual(ultimantico.on_surface.people, 100)
        self.assertEqual(ship_3 in fleet_two.ships, False)
        
    def test_colonize_2(self):
        p2 = player.Player()
        ultimantico = planet.Planet(on_surface = cargo.Cargo(people = 1))
        ultimantico.colonize(p2)
        ship_3 = ship.Ship(
            cargo = cargo.Cargo(people = 100, cargo_max = 200),
            colonizer = True
            )
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['colonize'],
                    recipiants = {'colonize': ultimantico},
                )])
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.colonize(p1)
        self.assertEqual(ultimantico.on_surface.people, 1)
        self.assertEqual(ship_3 in fleet_two.ships, True)
        
    def test_colonize_3(self):
        return #TODO
        ultimantico = ship.Ship()
        fleet_two = fleet.Fleet(
            waypoints = [
                waypoint.Waypoint(
                    actions = ['colonize'],
                    recipiants = {'colonize': ultimantico},
                )])
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.colonize(p1)
        self.assertEqual(ultimantico.on_surface.people, 1)
        self.assertEqual(ship_3 in fleet_two.ships, True)
        
    def test_piracy(self):
        return # TODO
        ship_3 = ship.Ship(
            location = location.Location(),
            )
        ship_4 = ship.Ship(
            location = location.Location(),
            )
        game_engine.register(ship_3)
        game_engine.register(ship_4)
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['piracy'],
                    location = location.Location()
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('piracy', p1)
    
    def test_scrap(self):
        #return # TODO
        ultimantico = planet.Planet()
        ship_3 = ship.Ship(
            cost = cost.Cost(
                titanium = 10,
                lithium = 10,
                silicon = 10
                ),
            cargo = cargo.Cargo(people = 100)
            )
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['scrap'],
                    recipiants = {'scrap': ultimantico},
                    )])
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.scrap()
        self.assertEqual(ultimantico.on_surface.people, 100)
        self.assertEqual(ultimantico.on_surface.titanium, 9)
        self.assertEqual(ultimantico.on_surface.silicon, 9)
        self.assertEqual(ultimantico.on_surface.lithium, 9)
    
    def test_patrol(self):
        return # TODO
        ship_3 = ship.Ship()
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(actions = ['patrol'])
                ])
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.patrol(p1)
    
    def test_route(self):
        return # TODO
        ship_3 = ship.Ship()
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(actions = ['route'])
                ])
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.route(p1)
'''
