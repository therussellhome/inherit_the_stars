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
        s.planets[1].temperature = (f.player.race.hab_temperature_stop + f.player.race.hab_temperature) / 2
        s.planets[1].gravity = (f.player.race.hab_gravity_stop + f.player.race.hab_gravity) / 2
        s.planets[1].radiation = (f.player.race.hab_radiation_stop + f.player.race.hab_radiation) / 2
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
        s.planets[1].temperature = (f.player.race.hab_temperature_stop + f.player.race.hab_temperature) / 2 - 1
        s.planets[1].gravity = (f.player.race.hab_gravity_stop + f.player.race.hab_gravity) / 2 - 1
        s.planets[1].radiation = (f.player.race.hab_radiation_stop + f.player.race.hab_radiation) / 2 - 1
        s.planets[2].temperature = (f.player.race.hab_temperature_stop + f.player.race.hab_temperature) / 2
        s.planets[2].gravity = (f.player.race.hab_gravity_stop + f.player.race.hab_gravity) / 2
        s.planets[2].radiation = (f.player.race.hab_radiation_stop + f.player.race.hab_radiation) / 2
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
        s.planets[1].temperature = (f.player.race.hab_temperature_stop + f.player.race.hab_temperature) / 2
        s.planets[1].gravity = (f.player.race.hab_gravity_stop + f.player.race.hab_gravity) / 2
        s.planets[1].radiation = (f.player.race.hab_radiation_stop + f.player.race.hab_radiation) / 2
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
        f2.player = reference.Reference(player.Player())
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
        f2.player = f.player
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
        f2.player = f.player
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
        p.player = f.player
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
        f2.player = reference.Reference(player.Player())
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
        f2.player = f.player
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
        f2.player = f.player
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
        p.player = f.player
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

