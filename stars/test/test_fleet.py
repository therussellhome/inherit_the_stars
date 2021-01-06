import unittest
from .. import *

class FleetCase(unittest.TestCase):
    def test_distribute_cargo(self):
        ship_1 = ship.Ship(cargo = cargo.Cargo(cargo_max = 200))
        ship_2 = ship.Ship(cargo = cargo.Cargo(cargo_max = 200))
        ship_3 = ship.Ship(cargo = cargo.Cargo(cargo_max = 200))
        fleet_1 = fleet.Fleet(ships = [ship_1, ship_2, ship_3])
        fleet_1.distribute_cargo(cargo.Cargo(titanium = 1), 'titanium', 600)
        self.assertEqual(ship_1.cargo.titanium, 1)
        fleet_1.distribute_cargo(cargo.Cargo(people = 13), 'people', 600)
        self.assertEqual(ship_2.cargo.people, 5)
        self.assertEqual(ship_3.cargo.people, 4)
    
    def test_distribute_fuel(self):
        ship_1 = ship.Ship(fuel_max = 200)
        ship_2 = ship.Ship(fuel_max = 200)
        fleet_1 = fleet.Fleet(ships = [ship_1, ship_2])
        fleet_1.distribute_fuel(1, 400)
        self.assertEqual(ship_1.fuel, 1)
        fleet_1.distribute_fuel(2, 400)
        self.assertEqual(ship_2.fuel, 1)
    
    def test_addships_1(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet()
        fleet_one.add_ships([ship_1, ship_2])
        self.assertEqual(fleet_one.ships[0], ship_1)
        self.assertEqual(fleet_one.ships[1], ship_2)
    
    def test_addships_2(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet()
        fleet_one.add_ships([ship_2])
        fleet_one.add_ships([ship_2])
        self.assertEqual(fleet_one.ships[0], ship_2)
        self.assertEqual(len(fleet_one.ships), 1)
    
    def test_addships_3(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet()
        fleet_one.add_ships([ship_1])
        fleet_one.add_ships([ship_2])
        self.assertEqual(fleet_one.ships[0], ship_1)
        self.assertEqual(fleet_one.ships[1], ship_2)
    
    def test_merge(self):
        return # TODO
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
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
        return # TODO
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
        fleet_one.waypoints = [
            waypoint.Waypoint(
                actions = ['split'],
                splits = [[ship_1]],
                location = location.Location()
                )
            ]
        fleet_one.execute('split', p1)
        self.assertEqual(ship_1 in p1.fleets[1].ships, True)
        self.assertEqual(ship_2 in p1.fleets[0].ships, True)
        
        
    def test_transfer(self):
        return # TODO
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
        return # TODO
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
    
    def test_move(self):
        return # TODO
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
                    ),
                ],
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
                    ),
                ],
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
        #'''
        ship_3 = ship.Ship(
            fuel = 1000,
            fuel_max = 10000,
            location = location.Location(),
            mass = 100,
            engines = [
                ],
            )
        fleet_one = fleet.Fleet(
            ships = [ship_3],
            waypoints = [
                waypoint.Waypoint(
                    location = location.Location(),
                    standoff = 'No Standoff',
                    speed = 5,
                    ),
                waypoint.Waypoint(
                    location = location.Location(x = 1, y = 1, z = 1),
                    speed = 2,
                    standoff = 'No Standoff',
                    ),
                ],
            )
        p1 = player.Player(fleets = [fleet_one])
        for i in range(1):
            fleet_one.execute('move', p1)
        self.assertEqual(fleet_one.location.x, 0)
        self.assertEqual(fleet_one.location.y, 0)
        self.assertEqual(fleet_one.location.z, 0)
        #'''
        fleet_one.location = location.Location()
        ship_1.location = location.Location()
        fleet_one.add_ships([ship_2])
        fleet_one.waypoints[1] = waypoint.Waypoint(
            location = location.Location(x = 24/100, y = 7/100, z = 0),
            speed = 5,
            standoff = 'No Standoff'
            )
        fleet_one.waypoints.append(waypoint.Waypoint(
            location = location.Location(x = 48/100, y = 14/100, z = 0),
            standoff = 'No Standoff',
            speed = 1
            ))
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
        """
        for i in range(9):
            fleet_one.move(p1)
        self.assertEqual(fleet_one.location.x, 1)
        self.assertEqual(fleet_one.location.y, 1)
        self.assertEqual(fleet_one.location.z, 1)
        #"""
        
    def test_buy_minerals(self):
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
            space_station = defaults.Defaults(
                fuel = 100000,
                is_trading_post = True,
                fuel_max = 500000
                ),
            on_surface = cargo.Cargo(
                silicon = 100,
                cargo_max = -1
                ))
        ship_1 = ship.Ship(cargo = cargo.Cargo(silicon = 100, cargo_max = 1000))
        fleet_three = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['buy'],
                    transfers = {'buy':[['silicon', 50]]},
                    recipiants = {'buy':ultimantico},
                    location = location.LocationReference(ultimantico)
                    )])
        p2.fleets = [fleet_three]
        p1.allocate_budget()
        p2.allocate_budget()
        fleet_three.buy(fleet_three.waypoints[0].recipiants['buy'], p2)
        self.assertEqual(p1.energy, 1150)
        self.assertEqual(p2.energy, 850)
        self.assertEqual(ultimantico.on_surface.silicon, 50)
        self.assertEqual(ship_1.cargo.silicon, 150)
    
    def test_buy_fuel(self):
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
            space_station = defaults.Defaults(
                fuel = 100000,
                is_trading_post = True,
                fuel_max = 500000
                ))
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
                    location = location.LocationReference(ultimantico)
                    )])
        p2.fleets = [fleet_three]
        p1.allocate_budget()
        p2.allocate_budget()
        fleet_three.buy(fleet_three.waypoints[0].recipiants['buy'], p2)
        self.assertEqual(p1.energy, 1100)
        self.assertEqual(p2.energy, 900)
        self.assertEqual(ultimantico.space_station.fuel, 99950)
        self.assertEqual(ship_1.fuel, 10050)
        
    def test_sell_minerals(self):
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
            space_station = defaults.Defaults(
                fuel = 100000,
                is_trading_post = True,
                fuel_max = 500000
                ),
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
                    location = location.LocationReference(ultimantico)
                    )])
        p2.fleets = [fleet_three]
        p1.allocate_budget()
        p2.allocate_budget()
        fleet_three.sell(fleet_three.waypoints[0].recipiants['sell'], p2)
        self.assertEqual(p1.energy, 650)
        self.assertEqual(p2.energy, 1350)
        self.assertEqual(ultimantico.on_surface.silicon, 150)
        self.assertEqual(ship_1.cargo.silicon, 50)
        
    def test_sell_fuel(self):
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
            space_station = defaults.Defaults(
                fuel = 100000,
                is_trading_post = True,
                fuel_max = 500000
                ))
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
                    location = location.LocationReference(ultimantico)
                    )])
        p2.fleets = [fleet_three]
        p1.allocate_budget()
        p2.allocate_budget()
        fleet_three.sell(fleet_three.waypoints[0].recipiants['sell'], p2)
        self.assertEqual(p1.energy, 900)
        self.assertEqual(p2.energy, 1100)
        self.assertEqual(ultimantico.space_station.fuel, 100050)
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
                    location = location.LocationReference(fleet_one)
                    )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.unload(fleet_two.waypoints[0].recipiants['unload'], p1)
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
                    location = location.LocationReference(fleet_one)
                    )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.unload(fleet_two.waypoints[0].recipiants['unload'], p1)
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
                    location = location.LocationReference(fleet_one)
                    )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.load(fleet_two.waypoints[0].recipiants['load'], p1)
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
                    location = location.LocationReference(fleet_one)
                    )])
        p1 = player.Player(fleets = [fleet_one, fleet_two])
        fleet_two.load(fleet_two.waypoints[0].recipiants['load'], p1)
        self.assertEqual(ship_1.fuel, 40)
        self.assertEqual(ship_2.fuel, 60)
    
    def test_unload_planet_cargo(self):
        ship_1 = ship.Ship(cargo = cargo.Cargo(people = 100, cargo_max = 200))
        p1 = player.Player()
        ultimantico = planet.Planet(
            space_station = defaults.Defaults(
                fuel_max = 1000,
                fuel = 100
                ),
            on_surface = cargo.Cargo(people = 100, cargo_max = -1)
            )
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['unload'],
                    transfers = {'unload': [['people', 40]]},
                    recipiants = {'unload': ultimantico},
                    location = location.LocationReference(ultimantico)
                    )])
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.unload(fleet_one.waypoints[0].recipiants['unload'], p1)
        self.assertEqual(ship_1.cargo.people, 60)
        self.assertEqual(ultimantico.on_surface.people, 140)
    
    def test_unload_planet_fuel(self):
        ship_1 = ship.Ship(
            fuel = 100,
            fuel_max = 200
            )
        p1 = player.Player()
        ultimantico = planet.Planet(
            space_station = defaults.Defaults(
                fuel_max = 1000,
                fuel = 100
                ))
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['unload'],
                    transfers = {'unload': [['fuel', 40]]},
                    recipiants = {'unload': ultimantico},
                    location = location.LocationReference(ultimantico)
                    )])
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.unload(fleet_one.waypoints[0].recipiants['unload'], p1)
        self.assertEqual(ship_1.fuel, 60)
        self.assertEqual(ultimantico.space_station.fuel, 140)
    
    def test_load_planet_cargo(self):
        ship_1 = ship.Ship(cargo = cargo.Cargo(people = 100, cargo_max = 200))
        p1 = player.Player()
        ultimantico = planet.Planet(
            space_station = defaults.Defaults(
                fuel_max = 1000,
                fuel = 100
                ),
                on_surface = cargo.Cargo(people = 100, cargo_max = -1)
                )
        fleet_one = fleet.Fleet(
            location = location.LocationReference(ultimantico),
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['load'],
                    transfers = {'load': [['people', 60]]},
                    recipiants = {'load': ultimantico},
                    location = location.LocationReference(ultimantico)
                    )])
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.load(fleet_one.waypoints[0].recipiants['load'], p1)
        self.assertEqual(ship_1.cargo.people, 160)
        self.assertEqual(ultimantico.on_surface.people, 40)
    
    def test_load_planet_fuel(self):
        ship_1 = ship.Ship(
            fuel = 100,
            fuel_max = 200
            )
        p1 = player.Player()
        ultimantico = planet.Planet(
            space_station = defaults.Defaults(
                fuel_max = 1000,
                fuel = 100
                ))
        fleet_one = fleet.Fleet(
            ships = [ship_1],
            waypoints = [
                waypoint.Waypoint(
                    actions = ['load'],
                    transfers = {'load': [['fuel', 60]]},
                    recipiants = {'load': ultimantico},
                    location = location.LocationReference(ultimantico)
                    )])
        p1.fleets = [fleet_one]
        ultimantico.player = reference.Reference(p1)
        fleet_one.load(fleet_one.waypoints[0].recipiants['load'], p1)
        self.assertEqual(ship_1.fuel, 160)
        self.assertEqual(ultimantico.space_station.fuel, 40)
    
    def test_self_repair(self):
        return # TODO
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
        return # TODO
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
        return # TODO
        ultimantico = planet.Planet(
            location = location.Location(),
            remaining_minerals = minerals.Minerals(
                titanium = 40000,
                silicon = 40000,
                lithium = 40000,
                ),
            gravity = 50,
            on_surface = cargo.Cargo(
                people = 1,
                ),
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
        ultimantico.on_surface.people = 0
        fleet_two.execute('orbital_mining', p1)
        self.assertEqual(ultimantico.on_surface.titanium, 16)
        self.assertEqual(ultimantico.remaining_minerals.titanium, 39977)
        
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
    
    def test_colonize(self):
        return # TODO
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
        return # TODO
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
                    actions = ['route'],
                    location = location.Location()
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_two])
        fleet_two.execute('route', p1)
    """

