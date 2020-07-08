import sys
from . import game_engine
from .defaults import Defaults
from .location import Location
from .location import locationReference
from .reference import Reference
from .star_system import Star_System
from .fleet import Fleet
from .ship import Ship


""" Default values (default, min, max)  """
__defaults = {
    'actions': [[]],
    # 'pre_load', 'unload', 'sell', 'buy', 'piracy', ...'load',
    'location': [],
    'fly_to': [Location()],
    'speed': [1, 1, 10],
    'description': [''],
    'standoff': [''],
    'recipiants': [{}],
    # 'load':"your; Planet(), Fleet() or empty_space, salvage",
    # 'unload':"your; Planet(), Fleet() or salvege",
    # 'sell':"other; Planet()",
    # 'buy':"other; Planet()",
    #?'piracy':"other; Fleet()"?
    #?'pre_piracy':"other; Fleet()"?
    'transfers': [{}],
    # 'load':[[item, amount][item, amount][item, amount][item, amount][fuel, amount]],
    # 'unload':[[item, amount][item, amount][item, amount][item, amount][fuel, amount]],
    # 'sell':[[item, amount][item, amount][item, amount][fuel, amount]],
    # 'buy':[[item, amount][item, amount][item, amount][fuel, amount]],
    #?'piracy':[[item, amount][item, amount][item, amount][fuel, amount]]?
    #?'pre_piracy':[[item, amount][item, amount][item, amount][fuel, amount]]?
    
}


""" Class defining waypoints - edited by the player through fleet """
class Waypoint(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    """ takes the standoff distance and changes the fly_to point accordingly """
    def calc_standoff(self, location, amount):
        dis, x, y, z = self.calc_distance(location)
        a = ((amount)**2)**(1/2)
        mod = -amount/a
        mod_x = (self.location.x-location.x)/x
        mod_y = (self.location.y-location.y)/y
        mod_z = (self.location.z-location.z)/z
        for i in range(int(a)):
            dis, x, y, z = self.calc_distance(location)
            self.fly_to.x += mod*mod_x*(x/dis)
            self.fly_to.y += mod*mod_y*(y/dis)
            self.fly_to.z += mod*mod_z*(z/dis)
    
    """ checks the distance between the fleet an the fly_to point """
    def calc_distance(self, location):
	self.dis_x = ((self.fly_to.x-location.x)**2)**(1/2)
	self.dis_y = ((self.fly_to.y-location.y)**2)**(1/2)
	self.dis_z = ((self.fly_to.z-location.z)**2)**(1/2)
	distance = ((self.dis_x)**2 + (self.dis_y)**2 + (self.dis_z)**2)**(1/2)
	return distance, self.dis_x, self.dis_y, self.dis_z
    
    """ calculates the standoff distance for the fleet """
    def move_to(self, fleet):
        if self.stantoff == 'No Standoff':
            for planet in game_engine.get('Planet/'):
                if self.location is planet.location:
                    self.fly_to = planet.system.get_outer_system(fleet.location)
            for ship in game_engine.get('Ship/'):
                if self.location is ship.location:
                    self.calc_intercept(fleet, ship)            
        fleet.compile_scanning()
        self.fly_to.x = self.location.x
        self.fly_to.y = self.location.y
        self.fly_to.z = self.location.z
        elif self.standoff == 'Avoid Detection':
            distance = fleet.anti_cloak_scanner
            for ship in fleet.ships:
                ship.mass = ship.hull_masss + (ship.cargo.titanium + ship.cargo.lithium + ship.cargo.silicon + ship.cargo.people)
                ship.aparant_mass = (ship.mass * ship.cloak)
                if ship.player.race.primary_race_trait == "SS":
                    ship.aparant_mass -= ship.kt_modifier
                normal_scanner = (fleet.pennetrating_scanner + ((fleet.normal_scanner - fleet.pennetrating_scanner) * (ship.aparant_mass / 100)))
                if distance < normal_scanner and ship.aparant_mass > 0:
                    distance = normal_scanner
            if distance < fleet.pennetrating_scanner:
                distance = fleet.pennetrating_scanner
            self.calc_standoff(fleet, distance+1)
        elif standoff == 'Penetrating Minimum':
            self.calc_standoff(fleet, fleet.pennetrating_scanner-1)
        elif standoff == 'Anti-Cloak Minimum':
            self.calc_standoff(fleet, fleet.anti_cloak_scanner-1)
        elif standoff == 'Hyper-Denial Minimum':
            fleet.compile_hyper_denial()
            if fleet.hyper_denial:
                self.calc_standoff(fleet, fleet.hyper_denial_range-1)
            else:
                self.standoff = 'No Standoff'
                self.move_to(fleet)
    
    """ gets places a ship will be """
    def get_cord(self, location, pre_location, speed):
        cord = Location(location.x, location.y, location.z)
        dis = (speed**2)/100
        x = (pre_location.x-location.x)
        y = (pre_location.y-location.y)
        z = (pre_location.z-location.z)
        mod_x = (x)/((x)**2)**(1/2)
        mod_y = (y)/((y)**2)**(1/2)
        mod_z = (z)/((z)**2)**(1/2)
        cord.x -= mod_x*(x/dis)
        cord.y -= mod_y*(y/dis)
        cord.z -= mod_z*(z/dis)
        return cord
        
    """ Predicts the movements of a ship """
    def predict_movment(self, speed, location, pre_location, time_distance):
        intercepts = [pre_location, location]
        for i in range(100*time_distance):
            location = get_cord(intercepts[-1], intercepts[-2], speed)
            intercepts.append(location)
            if i == 1:
                intercepts.pop(0)
        return intercepts
    
    """ Predicts the movements of a pursuing fleet and choses the cord to go to """
    def chose_intercept(self, fleet, ship, ship_speed, cords):
        times = []
        for cord in cords:
            distance_fleet = ((fleet.location.x-cord.x)**2 + (fleet.location.y-cord.y)**2 + (fleet.location.z-cord.z)**2)**(1/2)
            distance_ship = ((ship.location.x-cord.x)**2 + (ship.location.y-cord.y)**2 + (ship.location.z-cord.z)**2)**(1/2)
            times.append([distance_fleet/(self.speed**2), distance_ship/(ship_speed**2), cord])
        time = sys.maxsize
        for i in range(len(times)):
            if times[i][0] <= times[i][0] and times[i][0] < time:
                time = times[i][0]
                cord = times[i][2]
        return cord
    
    """ calcuates the intercept point """
    def calc_intercept(self, fleet, ship):
        top_speed, pre_location = fleet.player.find_intel(str(ship.name))
        distance = ((fleet.location.x-ship.location.x)**2 + (fleet.location.y-ship.location.y)**2 + (fleet.location.z-ship.location.z)**2)**(1/2)
        time_distance = distance/(top_speed**2)
        cords = self.predict_movment(top_speed, ship.location, pre_location, time_distance+50)
        self.fly_to = self.chose_intercept(fleet, ship, top_speed, cords)
    
