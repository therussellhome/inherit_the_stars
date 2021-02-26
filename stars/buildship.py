from .build_queue import BuildQueue
from .ship_design import ShipDesign
from ..reference import Reference

""" Default values (default, min, max)  """
__defaults = {
    'ship_design': ShipDesign(), # what is being built
    'ship': Reference('ship')
    'started': False
}


""" Temporary class to indicate ship in process """
class BuildShip(BuildQueue):
    def __init__(self, **kwargs, player):
        super().__init__(**kwargs)
        self.cost = self.ship_design.cost
        self.origonal_cost = self.cost
        if 'ship' not in kwargs:
            ship = Ship(location=Location(reference = self.planet), player=Reference(player), in_queue=True)
            self.ship = Reference(ship)
            player.add_fleet(location=Location(reference = self.planet), ships=[ship])
    
    """ outputs thet next cost and marks the previous componet as done """
    def finish(self):
        if not self.started:
            self.start()
            return self.calc_next().cost
        self.ship.add_coponent(self.calc_next())
        self.cost -= self.calc_next().cost
        if self.cost.is_zero():
            self.ship.in_queue = False
            return self.cost
        return self.calc_next().cost
    
    """ calulates the next item to work on """
    
    
    """ starts an upgrade (maybe a build too) """
    
    
    """ Mark the item as completed """
    def finish_a(self):
        self.planet[self.hab + '_terraform'] += 1
    

BuildShip.set_defaults(BuildShip, __defaults)
