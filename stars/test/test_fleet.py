import unittest
from .. import *
class FleetCase(unittest.TestCase):
    def test_addships_compile_returnn(self):
        ship_1 = ship.Ship(
            location=location.Location(),
            cargo=cargo.Cargo(titanium=100, cargo_max=200)
            )
        ship_2 = ship.Ship(
            location=location.Location(),
            cargo=cargo.Cargo(people=100, cargo_max=200)
            )
        game_engine.register(ship_1)
        game_engine.register(ship_2)
        fleet_one = fleet.Fleet()
        fleet_one.add_ships([ship_1, ship_2])
        fleet_one.compile()
        fleet_one.returnn()
        self.assertEqual(ship_1.cargo.titanium, 50)
        self.assertEqual(ship_1.cargo.people, 50)
        self.assertEqual(ship_2.cargo.titanium, 50)
        self.assertEqual(ship_2.cargo.people, 50)
    
    def test_merge(self):
        ship_1 = ship.Ship(location = location.Location())
        ship_2 = ship.Ship(location = location.Location())
        game_engine.register(ship_1)
        game_engine.register(ship_2)
        fleet_one = fleet.Fleet(ships = [ship_1])
        fleet_two = fleet.Fleet(
            ships = [ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['merge'],
                recipiants = {'merge': fleet_one},
                location = location.LocationReference(fleet_one)
                )]
            )
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.execute('merge', p1)
        self.assertEqual(len(p1.fleets), 1)
        self.assertEqual(ship_2 in fleet_one.ships, True)
        ship_3 = ship.Ship(location = location.Location())
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [waypoint.Waypoint(
                actions = ['merge'],
                recipiants = {'merge': fleet_one},
                location = location.LocationReference(fleet_one)
                )]
            )
        p2 = player.Player(fleets = [fleet_two])
        fleet_two.execute('bomb', p2)
        fleet_two.execute('merge', p2)
        self.assertEqual(len(p1.fleets), 1)
        self.assertEqual(ship_3 in fleet_two.ships, True)
        
    def test_split(self):
        ship_1 = ship.Ship(location = location.Location())
        ship_2 = ship.Ship(location = location.Location())
        game_engine.register(ship_1)
        game_engine.register(ship_2)
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['split'],
                splits = [[ship_2]],
                location = location.Location()
                )]
            )
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.execute('split', p1)
        self.assertEqual(ship_1 in fleet_one.ships, True)
        self.assertEqual(ship_2 in p1.fleets[1].ships, True)
        
    def test_transfer(self):
        ship_1 = ship.Ship(location = location.Location())
        ship_2 = ship.Ship(location = location.Location())
        game_engine.register(ship_1)
        game_engine.register(ship_2)
        p2 = player.Player()
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [waypoint.Waypoint(
                actions = ['transfer'],
                recipiants = {'transfer':p2},
                location = location.Location()
                )]
            )
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.execute('transfer', p1)
        self.assertEqual(fleet_one in p2.fleets, True)
    
    def test_hyper_denial(self):
        ship_1 = ship.Ship(location = location.Location())
        ship_2 = ship.Ship(location = location.Location())
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['deploy_hyper_denial'],
                    location = location.Location(),
                    ),
                ]
            )
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.execute('deploy_hyper_denial', p1)
        self.assertEqual(True, False, "Not Testing")
    
    def test_scan(self):
        ship_1 = ship.Ship(
            location = location.Location(),
            scanner = scanner.Scanner(
                anti_cloak = 75,
                penetrating = 250,
                normal = 400,
                )
            )
        ship_2 = ship.Ship(
            location = location.Location(),
            scanner = scanner.Scanner(
                anti_cloak = 125,
                penetrating = 50,
                normal = 600,
                )
            )
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['scan'],
                    location = location.Location(),
                    ),
                ]
            )
        p1 = player.Player(fleets = [fleet_one])
        fleet_one.execute('scan', p1)
        self.assertEqual(True, False, "Not Testing")
    
    def test_move(self):
        ship_1 = ship.Ship(
            fuel = 0,
            fuel_max = 100,
            location = location.Location(),
            mass = 100,
            engines = [
                engine.Engine(
                    kt_exponent = 1.5,
                    speed_divisor = 10.0,
                    speed_exponent = 5.0,
                    antimatter_siphon = 0.0
                    ),
                engine.Engine(
                    kt_exponent = 1.5,
                    speed_divisor = 10.0,
                    speed_exponent = 5.0,
                    antimatter_siphon = 0.0
                    )
                ]
            )
        ship_2 = ship.Ship(
            fuel = 1000,
            fuel_max = 10000,
            location = location.Location(),
            mass = 100,
            engines = [
                engine.Engine(
                    kt_exponent = 1.5,
                    speed_divisor = 10.0,
                    speed_exponent = 5.0,
                    antimatter_siphon = 0.0
                    ),
                engine.Engine(
                    kt_exponent = 1.5,
                    speed_divisor = 10.0,
                    speed_exponent = 5.0,
                    antimatter_siphon = 0.0
                    )
                ]
            )
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    location = location.Location(),
                    standoff = 'No Standoff',
                    speed = 5,
                    ),
                waypoint.Waypoint(
                    location = location.Location(x = 1, y = 1, z = 1),
                    speed = 5,
                    standoff = 'No Standoff',
                    ),
                waypoint.Waypoint(
                    location = location.Location(x = 1, y = 1, z = 1),
                    standoff = 'No Standoff',
                    speed = 5,
                    ),
                ],
            )
        p1 = player.Player(fleets = [fleet_one])
        for i in range(175):
            fleet_one.execute('move', p1)
        self.assertEqual(fleet_one.location.x, 1)
        self.assertEqual(fleet_one.location.y, 1)
        self.assertEqual(fleet_one.location.z, 1)
        fleet_one.location = location.Location()
        ship_1.location = location.Location()
        fleet_one.add_ships([ship_2])
        fleet_one.waypoints[1] = waypoint.Waypoint(
            location = location.Location(x = 24/100, y = 7/100, z = 0),
            speed = 5,
            standoff = 'No Standoff'
            )
        fleet_one.waypoints[2] = waypoint.Waypoint(
            location = location.Location(x = 24/100, y = 7/100, z = 0),
            standoff = 'No Standoff',
            speed = 1
            )
        for i in range(1):
            fleet_one.execute('move', p1)
        self.assertEqual(fleet_one.location.x, 24/100)
        self.assertEqual(fleet_one.location.y, 7/100)
        self.assertEqual(fleet_one.location.z, 0)
        fleet_one = fleet.Fleet(
            ships = [ship_2],
            waypoints = [
                waypoint.Waypoint(
                    location = location.Location(),
                    standoff = 'No Standoff',
                    speed = 1
                    ),
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
        """for i in range(9):
            fleet_one.move(p1)
        self.assertEqual(fleet_one.location.x, 1)
        self.assertEqual(fleet_one.location.y, 1)
        self.assertEqual(fleet_one.location.z, 1)"""
        
    def test_trade(self):
        buy = defaults.Defaults(
            cost_titanium = 6,
            cost_lithium = 4,
            cost_silicon = 3,
            cost_fuel = 2
            )
        sell = defaults.Defaults(
            cost_titanium = 9,
            cost_lithium = 7,
            cost_silicon = 7,
            cost_fuel = 2
            )
        treaty1 = defaults.Defaults(
            sell = sell,
            buy = buy,
            relation = 'team'
            )
        treaty2 = defaults.Defaults(
            sell = buy,
            buy = sell,
            relation = 'team'
            )
        p1 = player.Player(
            energy_minister = energy_minister.EnergyMinister(
                energy_minister_construction_percent = 0,
                energy_minister_mattrans_percent = 0,
                energy_minister_research_percent = 0,
                ),
            energy = 90000,
            name = 'Alpha',
            )
        p2 = player.Player(
            energy_minister = energy_minister.EnergyMinister(
                energy_minister_construction_percent = 0,
                energy_minister_mattrans_percent = 0,
                energy_minister_research_percent = 0,
                ),
            name = 'Beta',
            energy = 90000,
            )
        p2.treaties[p1.name] = treaty1
        p1.treaties[p2.name] = treaty2
        game_engine.register(p1)
        game_engine.register(p2)
        space_station = defaults.Defaults(
            fuel = 100000,
            trade = True,
            fuel_max = 500000
            )
        ultimantico = planet.Planet(
            name = 'ultimantico',
            player = reference.Reference(p1),
            space_station = space_station,
            on_surface = cargo.Cargo(
                titanium = 1000,
                lithium = 1000,
                silicon = 1000,
                people = 1000,
                cargo_max = 10000000000000000000000000000000
                ),
            location=location.Location(),
            )
        ship_7 = ship.Ship(
            name = 'ship_1',
            location = location.Location(),
            cargo = cargo.Cargo(silicon=100, cargo_max=100),
            fuel = 10000,
            fuel_max = 10000
            )
        ship_8 = ship.Ship(
            name = 'ship_3',
            location = location.Location(),
            cargo = cargo.Cargo(lithium=100, cargo_max=300),
            fuel = 10000,
            fuel_max = 30000
            )
        ship_6 = ship.Ship(
            name = 'ship_2',
            location = location.Location(),
            cargo = cargo.Cargo(titanium=100, cargo_max=200),
            fuel = 10000,
            fuel_max = 20000
            )
        fleet_three = fleet.Fleet(
            ships = [ship_6, ship_7, ship_8],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['buy', 'sell'],
                    transfers = {'buy':[['lithium', 50], ['silicon', 50], ['fuel', 30000]], 'sell':[['titanium', 40], ['fuel', 30000]]},
                    recipiants = {'buy':ultimantico, 'sell':ultimantico},
                    location = location.LocationReference(ultimantico)
                    )
                ]
            )
        p2.fleets = [fleet_three]
        p1.get_budget()
        p2.get_budget()
        fleet_three.compile()
        fleet_three.returnn()
        """print()
        print(ultimantico.name, ": {'fuel':", ultimantico.space_station.fuel, end='')
        for key in ultimantico.on_surface.__dict__:
            print(", '", key, "': ", getattr(ultimantico.on_surface, key), sep='', end='')
        print("}")
        for p in game_engine.get('Player'):
            print(p.name, " : {'energy': ", p.energy, "}", sep='')
            for f in p.fleets:
                for s in f.ships:
                    print(s.name, ": {'fuel':", s.fuel, end='')
                    for key in s.cargo.__dict__:
                        if key != 'cargo_max':
                            print(", '", key, "': ", getattr(s.cargo, key), sep='', end='')
                    print("}")"""
        fleet_three.execute('sell', p2)
        self.assertEqual(p1.energy, 29640)
        self.assertEqual(p2.energy, 150360)
        self.assertEqual(ultimantico.on_surface.titanium, 1040)
        self.assertEqual(ultimantico.space_station.fuel, 130000)
        self.assertEqual(ship_6.cargo.titanium, 20)
        self.assertEqual(ship_6.fuel, 0)
        self.assertEqual(ship_7.cargo.titanium, 10)
        self.assertEqual(ship_7.fuel, 0)
        self.assertEqual(ship_8.cargo.titanium, 30)
        self.assertEqual(ship_8.fuel, 0)
        fleet_three.execute('buy', p2)
        self.assertEqual(p1.energy, 90340)
        self.assertEqual(p2.energy, 89660)
        self.assertEqual(ultimantico.on_surface.lithium, 950)
        self.assertEqual(ultimantico.on_surface.silicon, 950)
        self.assertEqual(ultimantico.space_station.fuel, 100000)
        self.assertEqual(ship_6.cargo.lithium, 50)
        self.assertEqual(ship_6.cargo.silicon, 50)
        self.assertEqual(ship_6.fuel, 10000)
        self.assertEqual(ship_7.cargo.lithium, 25)
        self.assertEqual(ship_7.cargo.silicon, 25)
        self.assertEqual(ship_7.fuel, 5000)
        self.assertEqual(ship_8.cargo.lithium, 75)
        self.assertEqual(ship_8.cargo.silicon, 75)
        self.assertEqual(ship_8.fuel, 15000)
        
        
    def test_load_unload_fleet(self):
        ship_1 = ship.Ship(
            name = 'ship_1',
            location = location.Location(),
            cargo = cargo.Cargo(titanium = 100, cargo_max = 200),
            fuel_max = 200
            )
        ship_2 = ship.Ship(
            name = 'ship_2',
            location = location.Location(),
            cargo = cargo.Cargo(people = 100, cargo_max = 200),
            fuel_max = 200
            )
        game_engine.register(ship_1)
        game_engine.register(ship_2)
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2]
            )
        ship_3 = ship.Ship(
            name = 'ship_3',
            location = location.Location(),
            cargo = cargo.Cargo(lithium = 100, cargo_max = 100),
            fuel_max = 100
            )
        ship_4 = ship.Ship(
            name = 'ship_4',
            location = location.Location(),
            cargo = cargo.Cargo(silicon = 100, cargo_max = 300),
            fuel = 100,
            fuel_max = 300
            )
        game_engine.register(ship_3)
        game_engine.register(ship_4)
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['load', 'unload'],
                    transfers = {'unload':[['lithium', 40], ['silicon', 60], ['fuel', 40]], 'load':[['titanium', 60], ['people', 40]]},
                    recipiants = {'load':fleet_one, 'unload':fleet_one},
                    location = location.LocationReference(fleet_one)
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.execute('load', p1)
        """print()
        for fleett in p1.fleets:
            for shipp in fleett.ships:
                print(shipp.name, ": {'fuel':", shipp.fuel, end='')
                for key in shipp.cargo.__dict__:
                    if key != 'cargo_max':
                        print(", '", key, "': ", getattr(shipp.cargo, key), sep='', end='')
                print("}")"""
        self.assertEqual(ship_1.cargo.titanium, 20)
        self.assertEqual(ship_1.cargo.people, 30)
        self.assertEqual(ship_2.cargo.titanium, 20)
        self.assertEqual(ship_2.cargo.people, 30)
        self.assertEqual(ship_3.cargo.titanium, 15)
        self.assertEqual(ship_3.cargo.people, 10)
        self.assertEqual(ship_4.cargo.titanium, 45)
        self.assertEqual(ship_4.cargo.people, 30)
        fleet_two.execute('unload', p1)
        self.assertEqual(ship_1.cargo.lithium, 20)
        self.assertEqual(ship_1.cargo.silicon, 30)
        self.assertEqual(ship_1.fuel, 20)
        self.assertEqual(ship_2.cargo.lithium, 20)
        self.assertEqual(ship_2.cargo.silicon, 30)
        self.assertEqual(ship_2.fuel, 20)
        self.assertEqual(ship_3.cargo.lithium, 15)
        self.assertEqual(ship_3.cargo.silicon, 10)
        self.assertEqual(ship_3.fuel, 15)
        self.assertEqual(ship_4.cargo.lithium, 45)
        self.assertEqual(ship_4.cargo.silicon, 30)
        self.assertEqual(ship_4.fuel, 45)
    
    def test_load_unload_planet(self):
        ship_1 = ship.Ship(
            name = 'ship_1',
            location = location.Location(),
            cargo = cargo.Cargo(lithium = 100, cargo_max = 200),
            fuel = 100,
            fuel_max = 100
            )
        ship_2 = ship.Ship(
            name = 'ship_2',
            location = location.Location(),
            cargo = cargo.Cargo(silicon = 100, cargo_max = 200),
            fuel_max = 100
            )
        game_engine.register(ship_1)
        game_engine.register(ship_2)
        p1 = player.Player()
        ultimantico = planet.Planet(
            player = reference.Reference(p1),
            name = 'ultimantico',
            space_station = defaults.Defaults(
                fuel_max = 1000000,
                fuel = 100000
                ),
            on_surface = cargo.Cargo(
                titanium = 100,
                people = 100,
                cargo_max = 1000000000000
                ),
            location=location.Location()
            )
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['load', 'unload'],
                    transfers = {'unload':[['lithium', 40], ['silicon', 60]], 'load':[['titanium', 40], ['people', 60], ['fuel', 40]]},
                    recipiants = {'load':ultimantico, 'unload':ultimantico},
                    location = location.LocationReference(ultimantico)
                    )
                ]
            )
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.execute('load', p1)
        """print()
        for shipp in fleet_one.ships:
            print(shipp.name, ": {'fuel':", shipp.fuel, end='')
            for key in shipp.cargo.__dict__:
                if key != 'cargo_max':
                    print(", '", key, "': ", getattr(shipp.cargo, key), sep='', end='')
            print("}")
        print(ultimantico.name, ": {'fuel':", ultimantico.space_station.fuel, end='')
        for key in ultimantico.on_surface.__dict__:
            print(", '", key, "': ", getattr(ultimantico.on_surface, key), sep='', end='')
        print("}")"""
        self.assertEqual(ship_1.cargo.titanium, 20)
        self.assertEqual(ship_1.cargo.people, 30)
        self.assertEqual(ship_1.fuel, 70)
        self.assertEqual(ship_2.cargo.titanium, 20)
        self.assertEqual(ship_2.cargo.people, 30)
        self.assertEqual(ship_2.fuel, 70)
        self.assertEqual(ultimantico.on_surface.titanium, 60)
        self.assertEqual(ultimantico.on_surface.people, 40)
        self.assertEqual(ultimantico.space_station.fuel, 99960)
        fleet_one.execute('unload', p1)
        self.assertEqual(ship_1.cargo.lithium, 30)
        self.assertEqual(ship_1.cargo.silicon, 20)
        self.assertEqual(ship_2.cargo.lithium, 30)
        self.assertEqual(ship_2.cargo.silicon, 20)
        self.assertEqual(ultimantico.on_surface.lithium, 40)
        self.assertEqual(ultimantico.on_surface.silicon, 60)
    
    
    def test_self_repair(self):
        ship_3 = ship.Ship(
            location = location.Location(),
            repair = 3,
            damage_armor = 7,
            armor = 10,
            )
        ship_4 = ship.Ship(
            location = location.Location(),
            repair = 3,
            damage_armor = 7,
            armor = 20,
            )
        game_engine.register(ship_3)
        game_engine.register(ship_4)
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['self_repair'],
                    location = location.Location()
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('self_repair', p1)
    
    def test_repair(self):
        ship_3 = ship.Ship(
            location = location.Location(),
            repair_bay = 3,
            damage_armor = 7,
            armor = 10,
            )
        ship_4 = ship.Ship(
            location = location.Location(),
            repair_bay = 3,
            damage_armor = 7,
            armor = 20,
            )
        game_engine.register(ship_3)
        game_engine.register(ship_4)
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['repair'],
                    location = location.Location()
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('repair', p1)
    
    def test_orbital_mining(self):
        ultimantico = planet.Planet(
            location = location.Location(),
            remaining_minerals = minerals.Minerals(
                titanium = 40000,
                silicon = 40000,
                lithium = 40000,
                ),
            gravity = 50,
            )
        ship_3 = ship.Ship(
            location = location.Location(),
            mining_rate = 1.6,
            percent_wasted = 1.4,
            )
        game_engine.register(ship_3)
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['orbital_mining'],
                    recipiants = {'orbital_mining': ultimantico},
                    location = location.Location()
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('orbital_mining', p1)
        self.assertEqual(ultimantico.on_surface.titanium, 16)
        self.assertEqual(ultimantico.on_surface.lithium, 16)
        self.assertEqual(ultimantico.on_surface.silicon, 16)
        self.assertEqual(ultimantico.remaining_minerals.titanium, 39977)
        self.assertEqual(ultimantico.remaining_minerals.lithium, 39977)
        self.assertEqual(ultimantico.remaining_minerals.silicon, 39977)
    
    def test_lay_mines(self):
        p1 = player.Player(name = 'caltorez')
        system = star_system.StarSystem(
            mines = {p1.name: 0},
            location = location.Location(),
            planets = [
                planet.Planet(
                    gravity = 70,
                    ),
                planet.Planet(
                    gravity = 50,
                    ),
                planet.Planet(
                    gravity = 30,
                    ),
                planet.Planet(
                    gravity = 50,
                    ),
                planet.Planet(
                    gravity = 50,
                    ),
                ],
            )
        ship_3 = ship.Ship(
            location = location.Location(),
            mines_laid = 500000000000,
            )
        ship_4 = ship.Ship(
            location = location.Location(),
            mines_laid = 500000000000,
            )
        game_engine.register(ship_3)
        game_engine.register(ship_4)
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
        p1 = player.Player(
            race = race.Race(
                colonists_to_operate_defense = 1,
                ),
            name = 'p1',
            planetary_ministers = [
                planetary_minister.PlanetaryMinister(
                    name = 'New Colony Minister',
                    new_colony_minister = True,
                    ),
                planetary_minister.PlanetaryMinister(
                    name = 'target',
                    defenses = 97,
                    power_plants = 1,
                    factories = 1,
                    mines = 1,
                    ),
                ],
            )
        game_engine.register(p1)
        ultimantico = planet.Planet(
            player = reference.Reference(p1),
            on_surface = cargo.Cargo(
                people = 200
                ),
            location = location.Location(),
            facilities = {
                'Defense': facility.Facility(
                    quantity = 20,
                    tech = tech.Tech(shields = 600)
                    ),
                },
            )
        game_engine.register(ultimantico)
        p1.planetary_ministers[1].planets.append(ultimantico.name)
        ship_3 = ship.Ship(
            location = location.Location(),
            bombs = [
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                bomb.Bomb(
                    percent_pop_kill = 0.2,
                    minimum_pop_kill = 0,
                    shield_kill = 20,
                    max_defense = 85,
                    ),
                ],
            )
        game_engine.register(ship_3)
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['bomb'],
                    recipiants = {'bomb': ultimantico},
                    location = location.Location()
                    )
                ]
            )
        p2 = player.Player(fleets = [fleet_two], name = 'p2')
        game_engine.register(p2)
        p2.treaties[p1.name] = defaults.Defaults(relation = 'enemy')
        fleet_two.execute('bomb', p2)
        self.assertLess(ultimantico.on_surface.people, 192, 'NOTE: this will somtimes fail as it is statistical in nature')
        self.assertLess(ultimantico.facilities['Defense'].quantity, 17, 'NOTE: this will somtimes fail as it is statistical in nature')
    
    def test_colonize(self):
        ultimantico = planet.Planet(
            name = 'ultimantico',
            location = location.Location()
            )
        ship_3 = ship.Ship(
            location = location.Location(),
            cargo = cargo.Cargo(people = 100, cargo_max = 200),
            colonizer = True,
            )
        ship_4 = ship.Ship(
            location = location.Location(),
            cargo = cargo.Cargo(people = 200, cargo_max = 200),
            colonizer = True,
            )
        game_engine.register(ship_3)
        game_engine.register(ship_4)
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['colonize'],
                    recipiants = {'colonize': ultimantico},
                    location = location.Location()
                    )
                ]
            )
        p1 = player.Player(
            name = 'p1',
            fleets = [fleet_two],
            )
        game_engine.register(p1)
        game_engine.register(ultimantico)
        fleet_two.execute('colonize', p1)
        self.assertEqual(ultimantico.on_surface.people, 200)
        self.assertEqual(ship_3 in fleet_two.ships, False)
        
    """
    def test_piracy(self):
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
    """
    def test_scrap(self):
        ultimantico = planet.Planet(
            location=location.Location()
            )
        ship_3 = ship.Ship(
            location = location.Location(),
            cost = cost.Cost(
                titanium = 10,
                lithium = 10,
                silicon = 10
                ),
            cargo = cargo.Cargo(
                people = 100
                )
            )
        ship_4 = ship.Ship(
            location = location.Location(),
            cargo = cargo.Cargo(
                titanium = 10,
                lithium = 10,
                silicon = 10
                ),
            )
        game_engine.register(ship_3)
        game_engine.register(ship_4)
        game_engine.register(ultimantico)
        fleet_two = fleet.Fleet(
            ships = [ship_3, ship_4],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['scrap'],
                    recipiants = {'scrap': ultimantico},
                    location = location.Location(),
                    )
                ],
            location = location.LocationReference(ultimantico)
            )
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('scrap', p1)
        self.assertEqual(ultimantico.on_surface.people, 100)
        self.assertEqual(ultimantico.on_surface.titanium, 19)
        self.assertEqual(ultimantico.on_surface.silicon, 19)
        self.assertEqual(ultimantico.on_surface.lithium, 19)
    """
    def test_patrol(self):
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
                    actions = ['patrol'],
                    location = location.Location()
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('patrol', p1)
    "'""
    def test_route(self):
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
                    actions = ['route'],
                    location = location.Location()
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('route', p1)
    """

