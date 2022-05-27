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
    
    def test_sub_1(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
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

    def test_sub_4(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
        fleet_two = fleet.Fleet() + [ship_1, ship_2]
        fleet_one.player.fleets.append(fleet_one)
        fleet_one.player.fleets.append(fleet_two)
        fleet_one -= fleet_two
        self.assertEqual(len(fleet_one.ships), 0)

    def test_sub_5(self):
        ship_1 = ship.Ship()
        ship_2 = build_ship.BuildShip()
        fleet_one = fleet.Fleet() + [ship_1, ship_2]
        fleet_one -= ship_2
        self.assertTrue(ship_1 in fleet_one.ships)
        self.assertFalse(ship_2 in fleet_one.ships)
        self.assertEqual(len(fleet_one.ships), 1)

    def test_attribute1(self):
        f = fleet.Fleet() + ship.Ship(initiative=2) + ship.Ship(initiative=10)
        self.assertEqual(f.initiative, 10)

    def test_duplicate1(self):
        f0 = fleet.Fleet() + ship.Ship()
        f0.orders.append(order.Order())
        f1 = f0.duplicate()
        self.assertEqual(len(f0.ships), 1)
        self.assertEqual(len(f1.ships), 0)

    def test_next_hundreth(self):
        f = fleet.Fleet()
        f.is_stationary = False
        f.next_hundreth()
        self.assertTrue(f.is_stationary)

    def test_location1(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.update_location(location.Location(5, 5, 5))
        self.assertEqual(f.location.xyz, (5, 5, 5))
        self.assertEqual(f.ships[0].location.xyz, (5, 5, 5))

    def test_location2(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        p = planet.Planet(location=location.Location(5, 5, 5))
        f.update_location(location.Location(reference=p))
        self.assertAlmostEqual(f.location.xyz[0], 5)
        self.assertAlmostEqual(f.location.xyz[1], 5)
        self.assertAlmostEqual(f.location.xyz[2], 5)

    def test_read_orders1(self):
        f = fleet.Fleet() + build_ship.BuildShip()
        f.read_orders()
        self.assertEqual(f.move_to, f.location)

    def test_read_orders2(self):
        f = fleet.Fleet() + ship.Ship()
        f.read_orders()
        self.assertEqual(f.move_to, None)

    def test_read_orders3(self):
        f = fleet.Fleet() + ship.Ship(engines=[engine.Engine()])
        with patch.object(ship.Ship, 'is_space_station', return_value=True) as mock:
            f.read_orders()
        self.assertEqual(f.move_to, None)

    def test_read_orders4(self):
        f = fleet.Fleet() + ship.Ship(engines=[engine.Engine()])
        f.location = location.Location(1, 0, 0)
        with patch.object(order.Order, 'move_calc', return_value=location.Location()):
            f.read_orders()
        self.assertEqual(f.move_to, location.Location())

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

    def test_inhyperdenial1(self):
        f = fleet.Fleet()
        f.in_hyperdenial(10, None, True)
        f.in_hyperdenial(1, player.Player(), False)
        self.assertEqual(f.hyperdenial_effect, [1.0, 10.0])
        self.assertEqual(len(f.hyperdenial_players), 1)

    def test_hyperdenial1(self):
        f = fleet.Fleet() + ship.Ship()
        with patch.object(hyperdenial.HyperDenial, 'activate') as mock:
            f.activate_hyperdenial()
            self.assertEqual(mock.call_count, 1)

    def test_hyperdenial2(self):
        f = fleet.Fleet() + ship.Ship()
        f.stats.hyperdenial.radius = 1
        with patch.object(hyperdenial.HyperDenial, 'activate') as mock:
            f.activate_hyperdenial()
            self.assertEqual(mock.call_count, 1)

    def test_hyperdenial3(self):
        f = fleet.Fleet() + ship.Ship()
        f.stats.hyperdenial.range = 1
        f.is_stationary = False
        with patch.object(hyperdenial.HyperDenial, 'activate') as mock:
            f.activate_hyperdenial()
            self.assertEqual(mock.call_count, 0)

    def test_move1(self):
        f = fleet.Fleet()
        f.location = location.Location(1, 2, 3)
        f.move_to = None
        f.move()
        self.assertEqual(f.location.xyz, (1, 2, 3))

    def test_move2(self):
        f = fleet.Fleet() + ship.Ship()
        f.location = location.Location(1, 2, 3)
        f.move_to = location.Location(1.5, 2 , 3)
        f.is_stationary = False
        f.fuel = 100
        f.stats.fuel_max = 100
        f.order.speed = -1
        with patch.object(fleet.Fleet, '_fuel_calc', return_value=42):
            f.move()
        self.assertEqual(f.location.xyz, (1.5, 2, 3))
        self.assertEqual(f.fuel, 58)

    def test_move3(self):
        f = fleet.Fleet() + ship.Ship()
        f.ships[0].engines.append(engine.Engine())
        f.location = location.Location(1, 2, 3)
        f.move_to = location.Location(3, 2 , 3)
        f.is_stationary = False
        f.fuel = 100
        f.stats.fuel_max = 100
        f.order.speed = -1
        with patch.object(fleet.Fleet, '_fuel_calc', side_effect=[120, 42, 42]):
            f.move()
        self.assertEqual(f.location.xyz, (1.81, 2, 3))
        self.assertEqual(f.fuel, 58)

    def test_move4(self):
        f = fleet.Fleet() + ship.Ship()
        f.location = location.Location(1, 2, 3)
        f.move_to = location.Location(3, 2 , 3)
        f.is_stationary = False
        f.fuel = 100
        f.stats.fuel_max = 100
        f.order.speed = 1
        f.hyperdenial_effect = [0.1, 0.2]
        with patch.object(fleet.Fleet, '_fuel_calc', return_value=42):
            f.move()
        self.assertEqual(f.location.xyz, (1.01, 2, 3))
        self.assertEqual(f.fuel, 58)

    def test_move5(self):
        f = fleet.Fleet() + ship.Ship()
        f.location = location.Location(1, 2, 3)
        f.move_to = location.Location(3, 2 , 3)
        f.is_stationary = False
        f.fuel = 100
        f.stats.fuel_max = 100
        f.order.speed = 10
        with patch.object(fleet.Fleet, '_fuel_calc', side_effect=[120, 42, 42]):
            f.move()
        self.assertEqual(f.location.xyz, (1.01, 2, 3))
        self.assertEqual(f.fuel, 58)
    
    def test_move6(self):
        f = fleet.Fleet() + ship.Ship()
        f.location = location.Location(1, 2, 3)
        f.move_to = location.Location(2, 3, 4)
        f.is_stationary = False
        f.order.speed = -2
        f.move()
        self.assertEqual(f.location.xyz, (1, 2, 3))

    def test_move7(self):
        f = fleet.Fleet() + ship.Ship()
        f.location = location.Location(5, 5, 5)
        f.order.speed = -2
        f.move_to = location.Location(55, 55, 5)
        f.is_stationary = False
        with patch.object(fleet.Fleet, '_stargate_find', return_value=(None, None)):
            f.move()
        self.assertEqual(f.location.xyz, (5, 5, 5))
    
    def test_move8(self):
        start = fleet.Fleet() + ship.Ship()
        start.ships[0].stargate.strength = 500
        end = fleet.Fleet() + ship.Ship()
        end.location = location.Location(55, 55, 5)
        f = fleet.Fleet() + ship.Ship()
        f.order.speed = -1
        f.move_to = location.Location(55, 55, 5)
        f.is_stationary = False
        with patch.object(fleet.Fleet, '_stargate_find', return_value=(start, end)):
            f.move()
        self.assertEqual(f.location.xyz, (55, 55, 5))

    def test_move_in_system1(self):
        f = fleet.Fleet()
        f.move_in_system()
        self.assertEqual(f.location.xyz, (0, 0, 0))

    def test_move_in_system2(self):
        f = fleet.Fleet()
        f.move_to = location.Location(1, 0, 0)
        f.move_in_system()
        self.assertEqual(f.location.xyz, (0, 0, 0))

    def test_move_in_system1(self):
        # Use multiple fleets to "simulate" system location hierarchy
        system = fleet.Fleet()
        f = fleet.Fleet()
        f.location = location.Location(1, 0, 0, reference=system)
        f.move_to = location.Location(-1, 0, 0, reference=system)
        f.move_in_system()
        self.assertEqual(f.location.xyz, (-1, 0, 0))

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
            self.assertEqual(f.cargo.sum(), 30)

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
        f.is_stationary = False
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
        multi_fleet.reset()
        f1 = fleet.Fleet() + ship.Ship(fuel_max=100)
        f2 = fleet.Fleet() + ship.Ship(fuel=200)
        multi_fleet.add(f1)
        multi_fleet.add(f2)
        f1.piracy()
        self.assertEqual(f1.fuel, 0)
        self.assertEqual(f2.fuel, 200)

    def test_piracy2(self):
        multi_fleet.reset()
        f1 = fleet.Fleet() + ship.Ship(is_piracy_fuel=True, fuel_max=100)
        f2 = fleet.Fleet() + ship.Ship(fuel=200)
        multi_fleet.add(f1)
        multi_fleet.add(f2)
        f1.piracy()
        self.assertEqual(f1.fuel, 100)
        self.assertEqual(f2.fuel, 100)

    def test_piracy3(self):
        multi_fleet.reset()
        f1 = fleet.Fleet() + ship.Ship(is_piracy_fuel=True, fuel_max=100)
        f2 = fleet.Fleet() + ship.Ship(fuel=50)
        multi_fleet.add(f1)
        multi_fleet.add(f2)
        f1.piracy()
        self.assertEqual(f1.fuel, 50)
        self.assertEqual(f2.fuel, 0)

    def test_piracy4(self):
        multi_fleet.reset()
        f1 = fleet.Fleet() + ship.Ship(is_piracy_fuel=True, fuel_max=100)
        f2 = fleet.Fleet() + ship.Ship(fuel=0)
        multi_fleet.add(f1)
        multi_fleet.add(f2)
        f1.piracy()
        self.assertEqual(f1.fuel, 0)
        self.assertEqual(f2.fuel, 0)

    def test_piracy5(self):
        multi_fleet.reset()
        f1 = fleet.Fleet() + ship.Ship(is_piracy_fuel=True, fuel_max=100)
        f2 = fleet.Fleet() + ship.Ship(fuel=75)
        f3 = fleet.Fleet() + ship.Ship(fuel=75)
        multi_fleet.add(f1)
        multi_fleet.add(f2)
        multi_fleet.add(f3)
        f1.piracy()
        self.assertEqual(f1.fuel, 100)
        self.assertEqual(f2.fuel + f3.fuel, 50)

    def test_piracy6(self):
        multi_fleet.reset()
        f1 = fleet.Fleet() + ship.Ship(is_piracy_cargo=True, cargo_max=100)
        f2 = fleet.Fleet() + ship.Ship()
        f2.ships[0].cargo.titanium = 200
        multi_fleet.add(f1)
        multi_fleet.add(f2)
        with patch.object(player.Player, 'get_treaty', return_value=treaty.Treaty(relation='enemy')):
            f1.piracy()
        self.assertEqual(f1.cargo.titanium, 100)
        self.assertEqual(f2.cargo.titanium, 100)

    def test_unload1(self):
        f = fleet.Fleet() + ship.Ship()
        f.is_stationary = False
        with patch.object(fleet.Fleet, '_other_cargo', return_value=(None,0)) as mock:
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
        self.assertEqual(f.cargo.sum(), 6)
        self.assertEqual(f2.cargo.sum(), 0)

    def test_unload3(self):
        f = fleet.Fleet() + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f2 = fleet.Fleet() + ship.Ship(cargo_max=0)
        f2.player = f.player
        f.location = location.Location(reference=f2)
        f.order.unload_ti = 1
        f.order.unload_li = 0
        f.order.unload_si = -1
        f.unload()
        self.assertEqual(f.cargo.sum(), 6)
        self.assertEqual(f2.cargo.sum(), 0)

    def test_unload4(self):
        p_ref = reference.Reference(player.Player())
        f = fleet.Fleet(player=p_ref) + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f2 = fleet.Fleet(player=p_ref) + ship.Ship(cargo_max=10)
        f.location = location.Location(reference=f2)
        f.order.unload_ti = 1
        f.order.unload_li = 0
        f.order.unload_si = -1
        f.unload()
        self.assertEqual(f.cargo.sum(), 3)
        self.assertEqual(f2.cargo.sum(), 3)

    def test_unload5(self):
        p_ref = reference.Reference(player.Player())
        f = fleet.Fleet(player=p_ref) + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        p = planet.Planet(player=p_ref)
        f.location = location.Location(reference=p)
        f.order.unload_ti = 1
        f.order.unload_li = 0
        f.order.unload_si = -1
        f.unload()
        self.assertEqual(f.cargo.sum(), 3)
        self.assertEqual(p.on_surface.sum(), 3)

    def test_buy1(self):
        pass #TODO

    def test_scrap1(self):
        f = fleet.Fleet() + ship.Ship()
        f.is_stationary = False
        with patch.object(ship.Ship, 'scrap') as mock:
            f.scrap()
            self.assertEqual(mock.call_count, 0)

    def test_scrap2(self):
        f = fleet.Fleet() + ship.Ship()
        f.order.scrap = True
        with patch.object(ship.Ship, 'scrap') as mock:
            f.scrap()
            self.assertEqual(mock.call_count, 1)

    def test_scrap3(self):
        f = fleet.Fleet() + ship.Ship()
        p = planet.Planet()
        f.location = location.Location(reference=p)
        f.ships[0].cargo.people = 1
        f.order.scrap = True
        with patch.object(ship.Ship, 'scrap') as mock:
            f.scrap()
            self.assertEqual(mock.call_count, 0)

    def test_scrap4(self):
        p_ref = reference.Reference(player.Player())
        f = fleet.Fleet() + ship.Ship()
        p = planet.Planet()
        p.player = p_ref
        f.player = p_ref
        f.location = location.Location(reference=p)
        f.ships[0].cargo.people = 1
        f.order.scrap = True
        with patch.object(ship.Ship, 'scrap') as mock:
            f.scrap()
            self.assertEqual(mock.call_count, 1)

    def test_load1(self):
        f = fleet.Fleet() + ship.Ship()
        f.is_stationary = False
        with patch.object(fleet.Fleet, '_other_cargo', return_value=(None,0)) as mock:
            f.load()
            self.assertEqual(mock.call_count, 0)

    def test_load2(self):
        p1 = reference.Reference(player.Player())
        p2 = reference.Reference(player.Player())
        f = fleet.Fleet(player=p1) + ship.Ship(cargo_max=10)
        f2 = fleet.Fleet(player=p2) + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f.location = location.Location(reference=f2)
        f.order.load_ti = 1
        f.order.load_li = 0
        f.order.load_si = -1
        f.load()
        self.assertEqual(f.cargo.sum(), 0)
        self.assertEqual(f2.cargo.sum(), 6)

    def test_load3(self):
        p1 = reference.Reference(player.Player())
        f = fleet.Fleet(player=p1) + ship.Ship(cargo_max=0)
        f2 = fleet.Fleet(player=p1) + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f.location = location.Location(reference=f2)
        f.order.load_ti = 1
        f.order.load_li = 0
        f.order.load_si = -1
        f.load()
        self.assertEqual(f.cargo.sum(), 0)
        self.assertEqual(f2.cargo.sum(), 6)

    def test_load4(self):
        p1 = reference.Reference(player.Player())
        f = fleet.Fleet(player=p1) + ship.Ship(cargo_max=10)
        f2 = fleet.Fleet(player=p1) + ship.Ship(cargo=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f.location = location.Location(reference=f2)
        f.order.load_ti = 1
        f.order.load_li = 0
        f.order.load_si = -1
        f.load()
        self.assertEqual(f.cargo.sum(), 3)
        self.assertEqual(f2.cargo.sum(), 3)

    def test_load5(self):
        p1 = reference.Reference(player.Player())
        f = fleet.Fleet(player=p1) + ship.Ship(cargo_max=10)
        p = planet.Planet(player=p1, on_surface=cargo.Cargo(titanium=2, lithium=2, silicon=2))
        f.location = location.Location(reference=p)
        f.order.load_ti = 1
        f.order.load_li = 0
        f.order.load_si = -1
        f.load()
        self.assertEqual(f.cargo.sum(), 3)
        self.assertEqual(p.on_surface.sum(), 3)

    def test_buy1(self):
        f = fleet.Fleet() + ship.Ship(cargo_max=10)
        f.is_stationary = False
        f.buy()
        self.assertEqual(f.cargo.sum(), 0)

    def test_transfer1(self):
        p1 = reference.Reference(player.Player())
        f = fleet.Fleet(player=p1) + ship.Ship()
        f.transfer()
        self.assertEqual(f.player, p1)

    def test_transfer2(self):
        p1 = reference.Reference(player.Player())
        p2 = reference.Reference(player.Player())
        s = ship.Ship()
        f = p1.add_ships(s)
        f.order.transfer_to = p2
        f.transfer()
        self.assertFalse(s in p1.ships)
        self.assertTrue(s in p2.ships)

    def test_transfer3(self):
        f = fleet.Fleet() + ship.Ship()
        p = reference.Reference(player.Player())
        f.order.transfer_to = p
        f.ships[0].cargo.people = 100
        f.transfer()
        self.assertNotEqual(f.player, p)

    def test_transfer4(self):
        p1 = reference.Reference(player.Player())
        p2 = reference.Reference(player.Player())
        f = fleet.Fleet(player=p1) + build_ship.BuildShip()
        f.order.transfer_to = p2
        f.transfer()
        self.assertEqual(f.player, p1)

    def test_merge1(self):
        f1 = fleet.Fleet() + ship.Ship()
        f2 = fleet.Fleet() + ship.Ship()
        f1.merge()
        self.assertEqual(len(f2.ships), 1)

    def test_merge2(self):
        f1 = fleet.Fleet() + ship.Ship()
        f2 = fleet.Fleet() + ship.Ship()
        f1.order.merge = True
        f1.merge()
        self.assertEqual(len(f2.ships), 1)

    def test_merge3(self):
        f1 = fleet.Fleet() + ship.Ship()
        f2 = fleet.Fleet() + ship.Ship()
        f1.location = location.Location(reference=f2)
        f1.order.merge = True
        f1.merge()
        self.assertEqual(len(f2.ships), 1)

    def test_merge4(self):
        f1 = fleet.Fleet() + ship.Ship()
        f2 = fleet.Fleet() + ship.Ship()
        f1.order.location = location.Location(reference=f2)
        f1.location = f1.order.location
        f1.order.merge = True
        f1.merge()
        self.assertEqual(len(f2.ships), 1)

    def test_merge5(self):
        p1 = reference.Reference(player.Player())
        f1 = fleet.Fleet(player=p1) + ship.Ship()
        f2 = fleet.Fleet(player=p1) + ship.Ship()
        f1.order.location = location.Location(reference=f2)
        f1.location = f1.order.location
        f1.order.merge = True
        f1.merge()
        self.assertEqual(len(f2.ships), 2)

    def test_stargate_find1(self):
        multi_fleet.reset()
        f = fleet.Fleet() + ship.Ship()
        multi_fleet.add(f)
        f.move_to = f.location
        self.assertEqual(f._stargate_find(False)[0], None)
        self.assertEqual(f._stargate_find(False)[1], None)
    
    def test_stargate_find2(self):
        multi_fleet.reset()
        start = fleet.Fleet() + ship.Ship()
        start.ships[0].stargate.strength = 210
        end = fleet.Fleet() + ship.Ship()
        end.ships[0].stargate.strength = 150
        end.location = location.Location(5, 5, 5)
        f = fleet.Fleet() + ship.Ship(armor=1) + ship.Ship(armor=1, mass = 155)
        multi_fleet.add(start)
        multi_fleet.add(end)
        f.move_to = end.location
        with patch.object(player.Player, 'get_treaty', return_value=treaty.Treaty(buy_gate = 1)):
            self.assertEqual(f._stargate_find(False)[0].ID, start.ID)
            self.assertEqual(f._stargate_find(False)[1].ID, end.ID)
    
    def test_stargate_find3(self):
        multi_fleet.reset()
        start1 = fleet.Fleet() + ship.Ship()
        start1.ships[0].stargate.strength = 20
        start2 = fleet.Fleet() + ship.Ship()
        start2.ships[0].stargate.strength = 210
        end = fleet.Fleet() + ship.Ship()
        end.ships[0].stargate.strength = 150
        end.location = location.Location(5, 5, 5)
        f = fleet.Fleet() + ship.Ship(armor=1) + ship.Ship(armor=1, mass = 155)
        multi_fleet.add(start1)
        multi_fleet.add(start2)
        multi_fleet.add(end)
        f.move_to = end.location
        with patch.object(player.Player, 'get_treaty', return_value=treaty.Treaty(buy_gate = 1)):
            self.assertEqual(f._stargate_find(False)[0].ID, start2.ID)
            self.assertEqual(f._stargate_find(False)[1].ID, end.ID)
    
    def test_stargate_find4(self):
        multi_fleet.reset()
        start = fleet.Fleet() + ship.Ship()
        start.ships[0].stargate.strength = 20
        end = fleet.Fleet() + ship.Ship()
        end.ships[0].stargate.strength = 150
        end.location = location.Location(5, 5, 5)
        f = fleet.Fleet() + ship.Ship(armor=1) + ship.Ship(armor=1, mass = 155)
        multi_fleet.add(start)
        multi_fleet.add(end)
        f.move_to = end.location
        with patch.object(player.Player, 'get_treaty', return_value=treaty.Treaty(buy_gate = 1)):
            self.assertEqual(f._stargate_find(False)[0], None)
            self.assertEqual(f._stargate_find(False)[1], None)
    
    def test_stargate_find5(self):
        multi_fleet.reset()
        start = fleet.Fleet() + ship.Ship()
        start.ships[0].stargate.strength = 20
        end = fleet.Fleet() + ship.Ship()
        end.ships[0].stargate.strength = 150
        end.location = location.Location(5, 5, 5)
        f = fleet.Fleet() + ship.Ship(armor=1) + ship.Ship(armor=1, mass = 155)
        multi_fleet.add(start)
        multi_fleet.add(end)
        f.move_to = end.location
        with patch.object(player.Player, 'get_treaty', return_value=treaty.Treaty(buy_gate = 1)):
            self.assertEqual(f._stargate_find(True)[0], None)
            self.assertEqual(f._stargate_find(True)[1], None)
    
    def test_stargate_find6(self):
        multi_fleet.reset()
        start = fleet.Fleet() + ship.Ship()
        start.ships[0].stargate.strength = 160
        end = fleet.Fleet() + ship.Ship()
        end.ships[0].stargate.strength = 150
        end.location = location.Location(5, 5, 5)
        f = fleet.Fleet() + ship.Ship(armor=100) + ship.Ship(armor=100, mass = 155)
        multi_fleet.add(start)
        multi_fleet.add(end)
        f.move_to = end.location
        with patch.object(player.Player, 'get_treaty', return_value=treaty.Treaty(buy_gate = 1)):
            self.assertEqual(f._stargate_find(True)[0].ID, start.ID)
            self.assertEqual(f._stargate_find(True)[1].ID, end.ID)
    
    def test_scan_anticloak1(self):
        f = fleet.Fleet() + ship.Ship()
        with patch.object(scan, 'anticloak') as mock:
            f.scan_anticloak()
            self.assertEqual(mock.call_count, 0)

    def test_scan_anticloak2(self):
        f = fleet.Fleet() + ship.Ship(scanner=scanner.Scanner(anti_cloak=1))
        with patch.object(scan, 'anticloak') as mock:
            f.scan_anticloak()
            self.assertEqual(mock.call_count, 1)

    def test_scan_hyperdenial1(self):
        f = fleet.Fleet() + ship.Ship()
        with patch.object(scan, 'hyperdenial') as mock:
            f.scan_hyperdenial()
            self.assertEqual(mock.call_count, 0)

    def test_scan_hyperdenial2(self):
        f = fleet.Fleet() + ship.Ship(hyperdenial=hyperdenial.HyperDenial(radius=1))
        with patch.object(scan, 'hyperdenial') as mock:
            f.scan_hyperdenial()
            self.assertEqual(mock.call_count, 1)

    def test_scan_penetrating1(self):
        f = fleet.Fleet() + ship.Ship()
        with patch.object(scan, 'penetrating') as mock:
            f.scan_penetrating()
            self.assertEqual(mock.call_count, 0)

    def test_scan_penetrating2(self):
        f = fleet.Fleet() + ship.Ship(scanner=scanner.Scanner(penetrating=1))
        with patch.object(scan, 'penetrating') as mock:
            f.scan_penetrating()
            self.assertEqual(mock.call_count, 1)

    def test_scan_normal1(self):
        f = fleet.Fleet() + ship.Ship()
        with patch.object(scan, 'normal') as mock:
            f.scan_normal()
            self.assertEqual(mock.call_count, 0)

    def test_scan_normal2(self):
        f = fleet.Fleet() + ship.Ship(scanner=scanner.Scanner(normal=1))
        with patch.object(scan, 'normal') as mock:
            f.scan_normal()
            self.assertEqual(mock.call_count, 1)

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
        f.fuel = 151
        f.fuel_distribution()
        self.assertEqual(f.ships[0].fuel, 51)
        self.assertEqual(f.ships[1].fuel, 100)

    def test_fuel_distribution2(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.ships[0].fuel_max = 111
        f.ships[1].fuel_max = 200
        f.fuel = 311
        f.fuel_distribution()
        self.assertEqual(f.ships[0].fuel, 111)
        self.assertEqual(f.ships[1].fuel, 200)

    def test_fuel_distribution3(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.fuel_distribution()
        self.assertEqual(f.ships[0].fuel, 0)
        self.assertEqual(f.ships[1].fuel, 0)

    def test_cargo_distribution1(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.ships[0].cargo_max = 200
        f.ships[1].cargo_max = 400
        f.cargo = cargo.Cargo(titanium=151, silicon=151, lithium=149, people=149)
        f.cargo_distribution()
        self.assertEqual(f.ships[0].cargo, cargo.Cargo(titanium=51, silicon=50, lithium=50, people=49))
        self.assertEqual(f.ships[1].cargo, cargo.Cargo(titanium=100, silicon=101, lithium=99, people=100))

    def test_cargo_distribution2(self):
        f = fleet.Fleet() + ship.Ship() + ship.Ship()
        f.ships[0].cargo_max = 100
        f.ships[1].cargo_max = 1000
        f.cargo = cargo.Cargo(titanium=276, silicon=276, lithium=274, people=274)
        f.cargo_distribution()
        self.assertEqual(f.ships[0].cargo, cargo.Cargo(titanium=26, silicon=25, lithium=25, people=24))
        self.assertEqual(f.ships[1].cargo, cargo.Cargo(titanium=250, silicon=251, lithium=249, people=250))

