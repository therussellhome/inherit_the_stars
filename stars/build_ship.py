from .build_queue import BuildQueue
from .cost import Cost
from .ship_design import ShipDesign
from .reference import Reference
from .tech_level import TechLevel
from .ship import Ship
from .location import Location

""" Default values (default, min, max)  """
__defaults = {
    'ship_design': ShipDesign(), # what is being built
    'ship': Reference('Ship'),
    'in_progress': Cost(),
    'component': Reference('Tech'),
    'level': TechLevel(),
}


""" Temporary class to indicate ship in process """
class BuildShip(BuildQueue):
    """ Initialize the cost """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'ship' not in kwargs:
            ship = Ship(location=Location(reference = self.planet), race=Reference(self.planet.player.race), in_queue=True)
            self.ship = Reference(ship)
            self.planet.player.create_fleet(location=Location(reference = self.planet), ships=[ship])
            self.ship_design.update(self.planet.player.tech_level)
            self.cost = self.ship_design.cost
            self.component = self.ship_design.hull
            self.in_progress = self.component.cost * self.component.miniaturization(self.planet.player.tech_level)
        elif 'cost' not in kwargs:
            self.cost = self.ship.hull.reminiaturize(self.ship.level, self.player.planet.tech_level)
            for (tech, cnt) in self.ship.components.items():
                self.cost = tech.reminiaturize(self.ship.level, self.player.planet.tech_level) * cnt
            for (tech, cnt) in self.ship_design.components.items():
                if tech in self.ship.components:
                    cnt = max(0, cnt - self.ship.components[tech])
                self.cost = tech.miniaturize(self.player.planet.tech_level, 'cost') * cnt

    """ Check if the component is done or the entire ship is done """
    def build(self, spend=Cost()):
        # Ensure ship still exists
        if not self.ship:
            return Cost()
        # Trying to build beyond your tech level - cancel build
        if not self.ship_design.hull.is_available(self.planet.player.tech_level, self.planet.player.race):
            self.ship.player.add_message(sender=Reference('Minister/Admiralty'), message='invalid_shipdesign', parameters=[self.ship_design.ID])
            self.ship.find_fleet().remove_ship(ship)
            return Cost()
        # Scrap extra parts, upgrade the rest
        if not self.component:
            for (tech, cnt) in self.ship.components.items():
                if tech not in self.ship_design.components:
                    self.remove_component(tech, cnt)
                elif self.ship_design.components[tech] > cnt:
                    self.remove_component(tech, cnt - self.ship_design.components[tech])
            self.in_progress = self.ship.hull.reminiturize(self.ship.level, self.player.planet.tech_level)
            for (tech, cnt) in self.ship.components.items():
                self.in_progress += tech.reminiturize(self.ship.level, self.player.planet.tech_level) * cnt
            self.level = self.player.planet.tech_level
        super().build(spend)
        self.in_progress -= spend
        if self.in_progress.is_zero():
            # If not doing initial miniaturize, add hull/component
            if self.component:
                if self.component == self.ship_design.hull:
                    ship.hull = self.component
                    ship.commissioning = float(self.planet.player.date) - self.race.start_date
                    self.level = self.player.planet.tech_level
                else:
                    self.ship.add_component(self.component)
            # miniaturize returns the minerals
            else:
                self.planet.on_surface += self.spent
            # Next component
            self.component = Reference('Tech')
            for (tech, cnt) in self.ship_design.components.items():
                if not tech.is_available(self.planet.player.tech_level, self.planet.player.race):
                    # Skip unbuildable components
                    pass
                elif tech not in self.ship.components:
                    self.component = tech
                    break
                elif self.ship.components[tech] < cnt:
                    self.component = tech
                    break
            if self.component:
                self.in_progress = self.component.miniaturize(self.level, 'cost')
            # Recompute stats and apply any miniaturize
            self.ship.update(self.ship.level)
        return self.in_progress

    """ Called when being removed from the build queue """
    def cancel(self):
        if not ship.hull:
            self.ship.find_fleet().remove_ship(ship)

    """ Remove component """
    def remove_component(self, tech, cnt):
        self.planet.on_surface += tech.scrap_value(self.planet.player.race, self.ship.level) * cnt
        self.ship.remove_component(tech, cnt)

    """ Build queue display """
    def to_html(self):
        return self.ship_design.ID + ' - ' + self.ship.ID #TODO
    

BuildShip.set_defaults(BuildShip, __defaults)
