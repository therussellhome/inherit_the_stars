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
    
    def start2(self):
        self.p1 = player.Player(energy=90000)
        buy = defaults.Defaults(cost_titanium=6, cost_lithium=4, cost_silicon=3, cost_fuel=2)
        sell = defaults.Defaults(cost_titanium=9, cost_lithium=7, cost_silicon=7, cost_fuel=2)
        treaty = defaults.Defaults(sell=sell, buy=buy)
        space_station = defaults.Defaults(fuel=100000, trade=True, fuel_max=500000)
        self.p2 = player.Player(treaties={self.p1.name: treaty}, energy=90000)
        self.ultimantico = planet.Planet(player=reference.Reference(self.p1), space_station=space_station, on_surface=cargo.Cargo(titanium=1000, lithium=1000, silicon=1000, people=1000, cargo_max=1000000000000), location=location.Location())
        self.ship_7 = ship.Ship(location=location.Location(), cargo=cargo.Cargo(silicon=100, cargo_max=100), fuel=10000, fuel_max=10000)
        self.ship_8 = ship.Ship(location=location.Location(), cargo=cargo.Cargo(lithium=100, cargo_max=300), fuel=10000, fuel_max=30000)
        self.ship_5 = ship.Ship(location=location.Location(), cargo=cargo.Cargo(titanium=100, cargo_max=200), fuel=10000, fuel_max=20000)
        self.ship_6 = ship.Ship(location=location.Location(), cargo=cargo.Cargo(cargo_max=200), fuel=10000, fuel_max=20000)
        self.fleet_three = fleet.Fleet(player=reference.Reference(self.p2), ships=[reference.Reference(self.ship_5), reference.Reference(self.ship_6), reference.Reference(self.ship_7), reference.Reference(self.ship_8)], waypoints=[waypoint.Waypoint(actions=['buy', 'sell'], transfers={'buy':[['lithium', 60], ['silicon', 60]], 'sell':[['titanium', 20], ['fuel', 40000]]}, recipiants={'buy':self.ultimantico, 'sell':self.ultimantico}, location=location.Location(x=self.ultimantico.location.x, y=self.ultimantico.location.y, z=self.ultimantico.location.z))], cargo=cargo.Cargo(), fuel=0, fuel_max=0)
        self.assertEqual(self.p2.energy, 90000)
        self.assertEqual(self.ultimantico.on_surface.titanium, 1000)
        self.assertEqual(self.ultimantico.space_station.fuel, 100000)
        self.assertEqual(self.ultimantico.on_surface.lithium, 1000)
        self.assertEqual(self.ultimantico.on_surface.silicon, 1000)
        self.assertEqual(self.ship_5.cargo.titanium, 25)
        self.assertEqual(self.ship_5.cargo.lithium, 25)
        self.assertEqual(self.ship_5.cargo.silicon, 25)
        self.assertEqual(self.ship_6.cargo.titanium, 25)
        self.assertEqual(self.ship_6.cargo.lithium, 25)
        self.assertEqual(self.ship_6.cargo.silicon, 25)
        self.assertEqual(self.ship_7.cargo.titanium, 13)
        self.assertEqual(self.ship_7.fuel, 5000)
        self.assertEqual(self.ship_7.cargo.lithium, 12)
        self.assertEqual(self.ship_7.cargo.silicon, 13)
        self.assertEqual(self.ship_8.cargo.titanium, 37)
        self.assertEqual(self.ship_8.fuel, 15000)
        self.assertEqual(self.ship_8.cargo.lithium, 38)
        self.assertEqual(self.ship_8.cargo.silicon, 37)
    
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
        game_engine.register(ship_1)
        game_engine.register(ship_2)
        fleet_one = fleet.Fleet(ships = [ship_1])
        fleet_two = fleet.Fleet(
            ships = [ship_3],
            waypoints = [waypoint.Waypoint(
                actions = ['merge'],
                recipiants = {'merge': fleet_one},
                location = location.LocationReference(fleet_one)
                )]
            )
        p2 = player.Player(fleets = [fleet_two])
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
        
    def t_transfer(self):
        self.fleet_one.execute('transfer')
        self.assertEqual(self.p1.fleets[0], self.fleet_two)
        self.assertEqual(self.p2.fleets[0], self.fleet_one)
        
    def test_move(self):
        ship_1 = ship.Ship(
            fuel = 0,
            fuel_max = 100,
            location=location.Location(),
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
            location=location.Location(),
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
                    location = location.Location()
                    ),
                waypoint.Waypoint(
                    location = location.Location(x = 1, y = 1, z = 1),
                    speed = 1,
                    standoff = 'No Standoff'
                    )
                ]
            )
        p1 = player.Player(fleets = [fleet_one])
        for i in range(175):
            fleet_one.execute('move', p1)
        self.assertEqual(fleet_one.location.x, 1)
        self.assertEqual(fleet_one.location.y, 1)
        self.assertEqual(fleet_one.location.z, 1)
        """
        fleet_one = fleet.Fleet(
            ships = [ship_1, ship_2],
            waypoints = [
                waypoint.Waypoint(
                    location = location.Location(x = 24/100, y = 7/100, z = 0),
                    speed = 5,
                    standoff = 'No Standoff'
                    )
                ]
            )
        for i in range(6):
            self.fleet_one.move()
        self.assertEqual(self.fleet_one.location.x, 24/100)
        self.assertEqual(self.fleet_one.location.y, 7/100)
        self.assertEqual(self.fleet_one.location.z, 0)
        """
        
    def t_sell(self):
        self.fleet_three.execute('sell')
        self.assertEqual(self.p1.energy, 9820)
        self.assertEqual(self.p2.energy, 170180)
        self.assertEqual(self.ultimantico.on_surface.titanium, 1020)
        self.assertEqual(self.ultimantico.space_station.fuel, 140000)
        self.assertEqual(self.ship_5.cargo.titanium, 20)
        self.assertEqual(self.ship_5.fuel, 0)
        self.assertEqual(self.ship_6.cargo.titanium, 20)
        self.assertEqual(self.ship_6.fuel, 0)
        self.assertEqual(self.ship_7.cargo.titanium, 10)
        self.assertEqual(self.ship_7.fuel, 0)
        self.assertEqual(self.ship_8.cargo.titanium, 30)
        self.assertEqual(self.ship_8.fuel, 0)
        
    def t_buy(self):
        self.fleet_three.execute('buy')
        self.assertEqual(self.p1.energy, 10240)
        self.assertEqual(self.p2.energy, 169760)
        self.assertEqual(self.ultimantico.on_surface.lithium, 940)
        self.assertEqual(self.ultimantico.on_surface.silicon, 940)
        self.assertEqual(self.ship_5.cargo.lithium, 40)
        self.assertEqual(self.ship_5.cargo.silicon, 40)
        self.assertEqual(self.ship_6.cargo.lithium, 40)
        self.assertEqual(self.ship_6.cargo.silicon, 40)
        self.assertEqual(self.ship_7.cargo.lithium, 20)
        self.assertEqual(self.ship_7.cargo.silicon, 20)
        self.assertEqual(self.ship_8.cargo.lithium, 60)
        self.assertEqual(self.ship_8.cargo.silicon, 60)
        
        
    def t_load(self):
        self.fleet_two.execute('load')
        self.assertEqual(self.ship_1.cargo.titanium, 20)
        self.assertEqual(self.ship_1.cargo.people, 30)
        self.assertEqual(self.ship_2.cargo.titanium, 20)
        self.assertEqual(self.ship_2.cargo.people, 30)
        self.assertEqual(self.ship_3.cargo.titanium, 15)
        self.assertEqual(self.ship_3.cargo.people, 10)
        self.assertEqual(self.ship_4.cargo.titanium, 45)
        self.assertEqual(self.ship_4.cargo.people, 30)
        
    def t_unload(self):
        self.fleet_two.execute('unload')
        self.assertEqual(ship_1.cargo.lithium, 30)
        self.assertEqual(ship_1.cargo.silicon, 20)
        self.assertEqual(ship_2.cargo.lithium, 30)
        self.assertEqual(ship_2.cargo.silicon, 20)
        self.assertEqual(ship_3.cargo.lithium, 10)
        self.assertEqual(ship_3.cargo.silicon, 15)
        self.assertEqual(ship_4.cargo.lithium, 30)
        self.assertEqual(ship_4.cargo.silicon, 45)
