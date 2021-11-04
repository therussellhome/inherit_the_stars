from .build_ship import BuildShip
from .cost import Cost
from .defaults import Defaults
from .ship_design import ShipDesign
from .reference import Reference

""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'ship_design': ShipDesign(), # design of what to build
    'ship': Reference('Ship'), # ship being built/upgraded
    'planet': Reference('Planet'), # where to build/upgrade the ship
    'overhaul': True, # upgrade entire ship
    'on_hold': False, # pause building the ship but don't loose progress #TODO this is not implemented
    'cost': Cost(), # remaining cost for display
    'percent': (0, 0, 100), # percent complete
    'baryogenesis': False,
}

""" Ship building queue """
class BuShips(Defaults):
    """ Initialize the cost """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'ship' not in kwargs and self.planet and self.planet.player: 
            # Force the creation of a fleet for the player to interact with
            self.planet.player.add_ships(self)
        self.__cache__['queue'] = None

    """ Cache the associated queue item """
    def queue(self, queue=None):
        if queue:
            self.__cache__['queue'] = queue
        if not self.__cache__['queue']:
            self.__cache__['queue'] = BuildShip(planet=self.planet, baryogenesis=self.baryogenesis, buships=Reference(self), ship=self.ship)
        return self.__cache__['queue']

BuShips.set_defaults(BuShips, __defaults)
