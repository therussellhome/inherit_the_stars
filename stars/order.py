import sys
import copy
from . import stars_math
from . import game_engine
from .defaults import Defaults
from .location import Location
from .reference import Reference
cargo_options = ['_ti', '_li', '_si', '_people']
depart_options = [
    'immediately',
    'after x years',
    'repair to x',
    'remain indef',
]

standoff_options = [
    'No Standoff',
    'Avoid Detection',
    'Penetrating Minimum',
    'Anti-Cloak Minimum',
    'Hyper-Denial Minimum',
]

seperate_display = [
    'speed',
    'load_si',
    'load_ti',
    'load_li',
    'load_people',
    'unload_si',
    'unload_ti',
    'unload_li',
    'unload_people',
    'buy_si',
    'buy_ti',
    'buy_li',
    'buy_fuel',
    'colonize_min_hab',
    'colonize_min_ti',
    'colonize_min_li',
    'colonize_min_si',
]

veriable_maxes = [
    'load_si',
    'load_ti',
    'load_li',
    'load_people',
    'unload_si',
    'unload_ti',
    'unload_li',
    'unload_people',
    'buy_si',
    'buy_ti',
    'buy_li',
    'buy_fuel',
]

""" Default values (default, min, max)  """
__defaults = {
    'location': Location(),
    'speed': (-2, -2, 10), # -2=manual stargate, -1=auto, 0-10=manual
    'description': '',
    'standoff': standoff_options[0],
    'upgrade_if_commanded': False,#???
    'depart': depart_options[0],
    'depart_after_x': (0.01, 0.0, sys.maxsize),
    'repair_to_x': (0, 0, sys.maxsize),
    'load_si': (0, -1, sys.maxsize), # -1=load all available, 0-max=load exactly kt
    'load_ti': (0, -1, sys.maxsize), # -1=load all available, 0-max=load exactly kt
    'load_li': (0, -1, sys.maxsize), # -1=load all available, 0-max=load exactly kt
    'load_people': (0, -1, sys.maxsize), # -1=load all available, 0-max=load exactly kt
    'load_all available': False,
    'unload_si': (0, -1, sys.maxsize), # -1=unload all, 0-max=load exactly kt
    'unload_ti': (0, -1, sys.maxsize), # -1=unload all, 0-max=load exactly kt
    'unload_li': (0, -1, sys.maxsize), # -1=unload all, 0-max=load exactly kt
    'unload_people': (0, -1, sys.maxsize), # -1=unload all, 0-max=load exactly kt
    'buy_si': (0, -1, sys.maxsize), # -1=buy all available, 0-max=buy exactly kt
    'buy_ti': (0, -1, sys.maxsize), # -1=buy all available, 0-max=buy exactly kt
    'buy_li': (0, -1, sys.maxsize), # -1=buy all available, 0-max=buy exactly kt
    'buy_fuel': (0, -1, sys.maxsize), # -1=buy all available, 0-max=buy exactly kt
    'sell_si': False,
    'sell_ti': False,
    'sell_li': False,
    'sell_fuel': False,
    'patrol': False,
    'transfer_to': Reference('Player'),
    'merge': False,
    'hyperdenial': False,
    'lay_mines': False,
    'colonize_manual': False, # 
    'colonize_min_hab': (70, 0, 101), # 101=do not auto colonize
    'colonize_min_ti': (0, 0, 10),
    'colonize_min_li': (0, 0, 10),
    'colonize_min_si': (0, 0, 10),
    'scrap': False,
}

""" Class defining waypoints - edited by the player through fleet """
class Order(Defaults):
    def move_calc(self, fleet_location):
        """ 
        # Intentionally stopped
        if self.order.speed == 0:
            return
        # Calculate destination (patrol, standoff, etc)
        move = self.order.calc_fly_to(self.location)
        # Already there
        if self.location == move:
            return
        self.__cache__['move_in_system'] = move
        # Move is in system only
        if self.location.root_location == move.root_location:
            return
        # Move is to an in_system point, go to outer system first
        if move.in_system:
            self.__cache__['move'] = self.location.move(move, sys.maxsize, standoff=stars_math.TERAMETER_2_LIGHTYEAR)
        else:
            self.__cache__['move'] = move
        """
        return (self.location, self.location) #TODO

    """ calculates the standoff distance for the fleet """
    def move_to(self, fleet):
        self.fly_to = copy.copy(self.location)
        if self.standoff == 'No Standoff':
            if hasattr(self.location, 'reference') and self.location.reference.__class__.__name__ == "Planet":
                self.fly_to = planet.system.get_outer_system(fleet.location)
            if hasattr(self.location, 'reference') and self.location.reference.__class__.__name__ == "Ship":
                self.calc_intercept(fleet, self.location.reference)            
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
                self.calc_standoff(fleet, distance + 1)
            elif standoff == 'Penetrating Minimum':
                if fleet.pennetrating_scanner >= 1:
                    self.calc_standoff(fleet, fleet.pennetrating_scanner-1)
                else:
                    self.standoff = 'No Standoff'
                    self.move_to(fleet)
            elif standoff == 'Anti-Cloak Minimum':
                if fleet.anti_cloak_scanner >= 1:
                    self.fly_to.move(fleet.location, fleet.anti_cloak_scanner-1)
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

Order.set_defaults(Order, __defaults)
