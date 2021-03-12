import unittest
from .. import *

class FleetCase(unittest.TestCase):
    """ Test distribute_cargo()"""
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
    
    """ Test distribute_fuel()"""
    def test_distribute_fuel(self):
        ship_1 = ship.Ship(fuel_max = 200)
        ship_2 = ship.Ship(fuel_max = 200)
        fleet_1 = fleet.Fleet(ships = [ship_1, ship_2])
        fleet_1.distribute_fuel(1, 400)
        self.assertEqual(ship_1.fuel, 1)
        fleet_1.distribute_fuel(2, 400)
        self.assertEqual(ship_2.fuel, 1)
    
    """ Test adding ships as one list """
    def test_addships_1(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet()
        fleet_one.add_ships([ship_1, ship_2])
        self.assertEqual(fleet_one.ships[0], ship_1)
        self.assertEqual(fleet_one.ships[1], ship_2)
    
    """ Test adding same ship twice """
    def test_addships_2(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet()
        fleet_one.add_ships([ship_2])
        fleet_one.add_ships([ship_2])
        self.assertEqual(fleet_one.ships[0], ship_2)
        self.assertEqual(len(fleet_one.ships), 1)
    
    """ Test adding ships to an established fleet """
    def test_addships_3(self):
        ship_1 = ship.Ship()
        ship_2 = ship.Ship()
        fleet_one = fleet.Fleet()
        fleet_one.add_ships([ship_1])
        fleet_one.add_ships([ship_2])
        self.assertEqual(fleet_one.ships[0], ship_1)
        self.assertEqual(fleet_one.ships[1], ship_2)
    
    """ Test normal merge """
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

    """ Test that merge does execute when it would transfer player ownership of the ships in the merging fleet """
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
        
    """ Test normal split """
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
    
    """ Test putting all ships into one other fleet and removeing emptey fleets """
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
        
    """ Test putting all ships into other fleets and removeing emptey fleets """
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
        
    """ Test normal transfer """
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
    
    """ Test normal deployment of hyper denial """
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
    
    """ Test normal movement """
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
    
    """ Test movement with massive ship and low distance """
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
    
        '''
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
        #'''
        
    """ Fuel, perfect situation """
    def test_handle_cargo_10(self):
        fleet_1 = fleet.Fleet()
        unload_fuel = 100
        load_fuel_max = 100
        amount = fleet_1.handle_cargo(unload_fuel, 0, load_fuel_max, 'fuel', 30, cargo.Cargo(), 0, cargo.Cargo())
        self.assertEqual(amount, 30)
        
    """ Fuel, less fuel than requested """
    def test_handle_cargo_11(self):
        fleet_1 = fleet.Fleet()
        unload_fuel = 7
        load_fuel_max = 100
        amount = fleet_1.handle_cargo(unload_fuel, 0, load_fuel_max, 'fuel', 30, cargo.Cargo(), 0, cargo.Cargo())
        self.assertEqual(amount, 7)
        
    """ Fuel, cannot hold requested fuel """
    def test_handle_cargo_12(self):
        fleet_1 = fleet.Fleet()
        unload_fuel = 100
        load_fuel_max = 20
        amount = fleet_1.handle_cargo(unload_fuel, 0, load_fuel_max, 'fuel', 30, cargo.Cargo(), 0, cargo.Cargo())
        self.assertEqual(amount, 20)
        
    """ Cargo, perfect situation """
    def test_handle_cargo_20(self):
        fleet_1 = fleet.Fleet()
        load_cargo_max = 100
        unload_cargo = cargo.Cargo()
        for item in ['titanium', 'silicon', 'lithium', 'people']:
            unload_cargo[item] = 100
            amount = fleet_1.handle_cargo(0, 0, 0, item, 30, cargo.Cargo(), load_cargo_max, unload_cargo)
            self.assertEqual(amount, 30)
        
    """ Cargo, less cargo than requested """
    def test_handle_cargo_21(self):
        fleet_1 = fleet.Fleet()
        load_cargo_max = 100
        unload_cargo = cargo.Cargo()
        for item in ['titanium', 'silicon', 'lithium', 'people']:
            unload_cargo[item] = 15
            amount = fleet_1.handle_cargo(0, 0, 0, item, 30, cargo.Cargo(), load_cargo_max, unload_cargo)
            self.assertEqual(amount, 15)
        
    """ Cargo, cannot hold requested cargo """
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
    
    """ does not mine when planet is inhabited """
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
    
    """ normal test """
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
        
    """ #NotAPlanet test """
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
