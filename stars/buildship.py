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
        n = self.calc_next()
        if n == 'refit':
            return self.calc_refit_cost()
        if not self.started:
            self.start()
            return n.cost
        self.ship.add_coponent(n)
        self.cost -= n.cost
        if self.cost.is_zero():
            self.ship.in_queue = False
            return self.cost
        return self.calc_next().cost
    
    """ calculates the cost of a refit """
    def calc_refit_cost(self):
        return #TODO curent_mini_level - new_mini_level per coponent in poduction capacity and ten times that in energy
    
    """ calculates the next item to work on """
    def calc_next(self):
        n = None
        for tech in self.ship_design.components:
            if tech not in self.ship.components:
                n = tech
                break
            elif self.ship_design.components[tech] - self.ship.components[tech] > 0:
                n = tech
                break
        if n:
            for item in self.ship.player.tech:
                if item.name == n:
                    return item
        return 'refit'
    
    """ starts an upgrade (maybe a build too) """
    def start(self):
        self.ship.in_queue = True
        self.started = True
        for tech in self.ship.components:
            if tech in self.ship_design.components:
                extra = self.ship.components[tech] - self.ship_design.components[tech]
                if extra > 0:
                    #TODO scrap 'em
            else:
                #TODO scrap 'em
    
    """ Mark the item as completed """
    def finish_a(self):
        self.planet[self.hab + '_terraform'] += 1
    

BuildShip.set_defaults(BuildShip, __defaults)
