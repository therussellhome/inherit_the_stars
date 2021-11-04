from .build_queue import BuildQueue
from .cost import Cost
from .location import Location
from .minerals import Minerals
from .reference import Reference
from .ship import Ship
from .ship_design import ShipDesign
from .tech_level import TechLevel

""" Default values (default, min, max)  """
__defaults = {
    'buships': Reference('BuShips'), # reference to the BuShips item
    'ship': Reference('Ship'), # ship being built / upgraded
    'in_progress': Cost(), # remaining cost on the in-progress component
    'level': TechLevel(), # upgrade/build level of the ship
    'to_build': [], # components to build
    'to_scrap': [], # components to scrap
    'overhaul': Cost(), # cost for doing an upgrade
    'scrap_mineals': Minerals(), # minerals recooped as part of upgrade
}


""" Temporary class to indicate ship in process """
class BuildShip(BuildQueue):
    """ Initialize the cost """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_cost()

    """ Check if the component is done or the entire ship is done """
    def build(self, spend=Cost()):
        # Make sure we have the latest cost
        self.update_cost()
        # Select the first/next component to work on
        self._next_component()
        # Spend
        super().build(spend)
        self.in_progress -= spend
        # Recover any scrap
        if len(self.to_scrap) > 0:
            for tech in self.to_scrap:
                self.ship.remove_component(tech)
            self.planet.on_surface += self.scrap_minerals
            super().build(self.scrap_minerals * -1)
            self.to_scrap = []
            self.scrap_minerals = Minerals()
        # Completed the overhaul / component
        if self.in_progress.is_zero():
            if not self.overhaul.is_zero():
                # Recover all the minerals for the overhaul
                overhaul_minerals = Minerals(self.overhaul)
                self.planet.on_surface += overhaul_minerals
                super().build(overhaul_minerals * -1)
                self.overhaul = Cost()
            elif len(self.to_build) > 0: # add component
                if not self.ship:
                    self.ship = Reference(Ship(location=Location(reference=self.planet), race=Reference(self.planet.player.race)))
                    for f in self.planet.player.fleets:
                        if self.buships in f.under_construction:
                            self.planet.player.add_ships(self.ship, f)
                            f - self
                            break
                    else:
                        self.planet.player.add_ships(self.ship)
                self.ship.add_component(self.to_build.pop(0), False)
            self.ship.update(self.level)
            self._next_component()
        return self.in_progress

    """ Next component """
    def _next_component(self):
        if self.in_progress.is_zero():
            if self.ship:
                self.ship.under_construction = True
            if not self.overhaul.is_zero():
                self.in_progress = self.overhaul
            elif len(self.to_build) > 0:
                self.in_progress = self.to_build[0].build_cost(self.level)
            elif self.ship: # no more components so no longer under construction
                self.ship.under_construction = False

    """ Update the cost if contruction has not started """
    def update_cost(self):
        if self.spent.is_zero():
            self.level = self.planet.player.tech_level
            # make sure the design is updated
            self.buships.ship_design.update()
            # all components in the design (will be reduced for existing below)
            self.to_build = []
            for (tech, cnt) in self.buships.ship_design.components.items():
                for i in range(cnt):
                    # make sure the hull is built first
                    if tech.is_hull():
                        self.to_build.insert(0, tech)
                    else:
                        self.to_build.append(tech)
            # find extra components to scrap and overhaul costs
            self.overhaul = Cost()
            self.to_scrap = []
            self.scrap_minerals = Minerals()
            if self.ship:
                if not self.buships.overhaul:
                    self.level = self.ship.level
                for (tech, cnt) in self.ship.components.items():
                    for i in range(cnt):
                        if tech in self.to_build:
                            if self.buships.overhaul:
                                self.overhaul += tech.overhaul_cost(self.ship.level, self.level, self.planet.player.race)
                            self.to_build.remove(tech)
                        else:
                            self.scrap_minerals += tech.scrap_value(self.planet.player.race, self.ship.level)
                            self.to_scrap.append(tech)
            # Add up costs
            self.cost = Cost()
            for tech in self.to_build:
                self.cost += tech.build_cost(self.level)
            self.cost = self.cost - self.scrap_minerals + self.overhaul - Minerals(self.overhaul)


BuildShip.set_defaults(BuildShip, __defaults)
