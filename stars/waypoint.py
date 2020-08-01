import sys
import copy
from . import game_engine
from .race import Race
from .ship import Ship
#from .fleet import Fleet
from .planet import Planet
from .defaults import Defaults
from .location import Location
#from .location import locationReference
from .reference import Reference
#from .star_system import Star_System


""" Default values (default, min, max)  """
__defaults = {
    'actions': [[]],
    # 'pre_load', 'unload', 'sell', 'buy', 'piracy', ...'load',
    'location': [],
    'fly_to': [Location()],
    'speed': [1, 0, 10],
    'description': [''],
    'standoff': ['No Standoff'],
    # 'Avoid Detection', 'Penetrating Minimum', 'Anti-Cloak Minimum', 'Hyper-Denial Minimum', 'No Standoff'(intercept if target is a ship)
    'move_on': [False],
    'upgrade_if_commanded': [False],
    'recipiants': [{}],
    # 'load':"your; Planet(), Fleet() or empty_space, salvage",
    # 'unload':"your; Planet(), Fleet() or salvege",
    # 'sell':"other; Planet()",
    # 'buy':"other; Planet()",
    # 'merge':Reference(Fleet())
    # 'transfer':Reference(Fleet().player)
    #?'piracy':"other; Fleet()"?
    'transfers': [{}],
    # 'load':[[item, amount][item, amount][item, amount][item, amount][fuel, amount]],
    # 'unload':[[item, amount][item, amount][item, amount][item, amount][fuel, amount]],
    # 'sell':[[item, amount][item, amount][item, amount][fuel, amount]],
    # 'buy':[[item, amount][item, amount][item, amount][fuel, amount]],
    #?'piracy':[[item, amount][item, amount][item, amount][fuel, amount]]?
    
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
        self.fly_to.x += mod*mod_x*(x/dis)*a
        self.fly_to.y += mod*mod_y*(y/dis)*a
        self.fly_to.z += mod*mod_z*(z/dis)*a
    
    """ checks the distance between the fleet an the fly_to point """
    def calc_distance(self, location):
        dis_x = ((self.fly_to.x-location.x)**2)**(1/2)
        dis_y = ((self.fly_to.y-location.y)**2)**(1/2)
        dis_z = ((self.fly_to.z-location.z)**2)**(1/2)
        distance = ((dis_x)**2 + (dis_y)**2 + (dis_z)**2)**(1/2)
        return distance, dis_x, dis_y, dis_z
    
    """ calculates the standoff distance for the fleet """
    def move_to(self, fleet):
        self.fly_to = Location(x=copy.copy(self.location.x), y=copy.copy(self.location.y), z=copy.copy(self.location.z))
        if self.standoff == 'No Standoff':
            for planet in game_engine.get('Planet/'):
                if self.location is planet.location:
                    self.fly_to = planet.system.get_outer_system(fleet.location)
            for ship in game_engine.get('Ship/'):
                if self.location is ship.location:
                    self.calc_intercept(fleet, ship)            
        else:
            fleet.compile_scanning()
            if self.standoff == 'Avoid Detection':
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
                if fleet.pennetrating_scanner >= 1:
                    self.calc_standoff(fleet, fleet.pennetrating_scanner-1)
                else:
                    self.standoff = 'No Standoff'
                    self.move_to(fleet)
            elif standoff == 'Anti-Cloak Minimum':
                if fleet.anti_cloak_scanner >= 1:
                    self.calc_standoff(fleet, fleet.anti_cloak_scanner-1)
                else:
                    self.standoff = 'No Standoff'
                    self.move_to(fleet)
            elif standoff == 'Hyper-Denial Minimum':
                fleet.compile_hyper_denial()
                if fleet.hyper_denial:
                    self.calc_standoff(fleet, fleet.hyper_denial_range-1)
                else:
                    self.standoff = 'No Standoff'
                    self.move_to(fleet)
            else:
                self.standoff = 'No Standoff'
                self.move_to(fleet)
    
    """ gets places a ship will be """
    def get_cord(self, location, pre_location, speed, time):
        cord = Location(location.x, location.y, location.z)
        dis = (speed**2)*(time+time_in)
        dis_self = (self.speed**2)*time/100
        check_dis =  dis - dis_self
        x = (pre_location.x-location.x)
        y = (pre_location.y-location.y)
        z = (pre_location.z-location.z)
        cord.x -= x/dis
        cord.y -= y/dis
        cord.z -= z/dis
        return cord, check_dis
        
    """ Predicts the movements of a ship """
    def predict_movment(self, speed, location, pre_location):
        intercepts = [pre_location, location]
        for time in range(2000):
            location, check_dis = get_cord(intercepts[-1][0], intercepts[-2][0], speed, time)
            intercepts.append([location, check_dis])
            if time == 1 or time == 2:
                intercepts.pop(0)
        return intercepts
    
    """ Predicts the movements of a pursuing fleet and choses the cord to go to """
    def chose_intercept(self, cords):
        min_distance = sys.maxsize
        for i in range(len(cords)):
            if cords[i][1] < min_distance:
                chose = i
                min_distance = cords[i][1]
                cord = cords[chose][0]
            if min_disnance <= 0:
                cord = cords[chose][0]
                break
        return cord
    
    """ calcuates the intercept point """
    def calc_intercept(self, fleet, ship):
        top_speed, pre_location, ship = fleet.player.find_intel(str(ship.name))
        cords = self.predict_movment(top_speed, ship.location, pre_location)
        self.fly_to = self.chose_intercept(cords)
    
