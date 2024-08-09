import sys
import copy
from . import stars_math
from . import game_engine
from .defaults import Defaults
from .location import Location
from .reference import Reference

standoff_options = [
    'No Standoff',
    'Avoid Detection',
    'Penetrating Minimum',
    'Anti-Cloak Minimum',
    'Hyper-Denial Minimum',
]

""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'location': Location(),
    'speed': (-1, -2, 10), # -2=auto stargate, -1=auto, 0-10=manual
    'description': '',
    'standoff': standoff_options[0],
    'depart': (0.0, 0.0, 10.0), # depart after x years, 10.0=never
    'repair_to': (0, 0, sys.maxsize), # TODO Do we even want this option?
    'ti': (0, 0, 100), # unload / load %
    'ti_dunnage': False, # load dunnage
    'ti_trade': False, # buy / sell
    'li': (0, 0, 100), # unload / load %
    'li_dunnage': False, # load dunnage
    'li_trade': False, # buy / sell
    'si': (0, 0, 100), # unload / load %
    'si_dunnage': False, # load dunnage
    'si_trade': False, # buy / sell
    'pop': (0, 0, 100), # unload / load %
    'pop_dunnage': False, # load dunnage
    'fuel': (0, 0, 100), # buy / sell %
    'fuel_trade': False, # buy / sell
    'transfer_to': Reference('Player'),
    'hyperdenial': True,
    'lay_mines': True,
    'auto_colonize': True, 
    'merge': False,
    'scrap': False,
    'patrol': False,
}

""" Class defining waypoints - edited by the player through fleet """
class Order(Defaults):
    """ Initialize and register """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        game_engine.register(self)
        print('order.__init__', kwargs)

    def __getattribute__(self, name, check=False):
        if name == 'location' and (check == None or check == True):
            loc = super().__getattribute__(name)
            if check == None:
                print('get Order location:', end=' ')
            loc.get_display('pos,ref')
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'location':
            print('old Order location:', end=' ')
            loc = self.__getattribute__(name, True)
            print('set Order location:', end=' ')
            value.get_display('pos,ref')
            print('Change in Terrameters:', (loc - value) / stars_math.TERAMETER_2_LIGHTYEAR)
        return super().__setattr__(name, value)

    """ Calculate where to move to """
    def move_calc(self, fleet_location, in_system_only=False):
        print('Order.move_calc[ fleet_location ]:', end=' ')
        fleet_location.get_display('pos,ref')
        # In-system moves allowed
        if fleet_location.root_location == self.location.root_location:
            print('in-system move:', end=' ')
            self.location.get_display('pos,ref')
            return self.location
        # Intentionally stopped or not allowed to move outside of system
        if self.speed == 0 or in_system_only:
            print('No move')
            return fleet_location
        if self.patrol:
            pass # TODO select nearest enemy to pursue and change the location
        if self.standoff == 'No Standoff':
            print('no-standoff move:', end=' ')
            self.location.get_display('pos,ref')
            return self.location
        location = fleet_location.move(self.location, standoff=self._standoff(fleet_location))
        print('standard move:', end=' ')
        location.get_display('pos,ref')
        return location

    """ Calculates the standoff distance for the fleet """
    def _standoff(self, fleet_location):
        standoff = 0.0
        if self.standoff == 'Avoid Detection':
            pass # TODO calculate the standoff distance
        elif self.standoff == 'Penetrating Minimum':
            pass # TODO calculate the standoff distance
        elif self.standoff == 'Anti-Cloak Minimum':
            pass # TODO calculate the standoff distance
        elif self.standoff == 'Hyper-Denial Minimum':
            pass # TODO calculate the standoff distance
        return standoff


    """ calculates the standoff distance for the fleet 
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
    """
    
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
