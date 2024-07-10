from .build_queue import BuildQueue
from .cost import Cost
from .location import Location
from .minerals import Minerals
from .reference import Reference
from .asteroid import Asteroid

""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'bupackets': Reference('BuPackets'), # reference to the BuShips item
    'asteroid': Reference('Asteroid'), # ship being built / upgraded
    'in_progress': Cost(), # remaining cost on the in-progress component
}


""" Temporary class to indicate Packet in process """
class BuildPacket(BuildQueue):
    """ Check if the component is done or the entire ship is done """
    def build(self, spend=Cost()):
        # Make sure we have the latest cost
        self._update_cost()
        # Spend
        super().build(spend)
        self.in_progress -= spend
        # Recover any scrap
        if len(self.to_scrap) > 0:
            for tech in self.to_scrap:
                self.ship.remove_component(tech) #how are minerals loaded into self.scrap_minerals?
            self.planet.on_surface += self.scrap_minerals
            super().build(self.scrap_minerals * -1)
            self.to_scrap = []
            self.scrap_minerals = Minerals()
        # Completed the overhaul / component
        if self.in_progress.is_zero():
        return self.in_progress

        """ Provide calculated values """
    def __getattribute__(self, name):
        self_dict = object.__getattribute__(self, '__dict__')
        # Safety check if inital defaults have not been applied or if has value
        if '__init_complete__' not in self_dict or name not in self_dict:
            return super().__getattribute__(name)
        if name == 'cost' and self_dict['spent'].is_zero():
            self_dict['cost'] = self._update_cost()
        return super().__getattribute__(name)

    """ Update the cost """
    def _update_cost(self):
        if not self.spent.is_zero():
            return super().__getattribute__('cost')
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
                self.level = self.ship.level #
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
        cost = Cost()
        for tech in self.to_build:
            cost += tech.build_cost(self.level)
        cost = cost - self.scrap_minerals + self.overhaul - Minerals(self.overhaul)
        return cost


BuildShip.set_defaults(BuildShip, __defaults)
