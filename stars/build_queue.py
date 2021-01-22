from .cost import Cost
from .defaults import Defaults
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'cost': Cost(), # cost remaining
    'planet': Reference('Planet'),
    'baryogenesis': False,
    'origonal_cost': Cost(), #origonal cost
}


""" Base class for the build queue """
class BuildQueue(Defaults):
    """ Child classes should override this to set the cost """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    """ Child classes need to override this """
    def finish(self):
        pass
    
    """ for child classes to use for their name in the production queue """
    def calc_type(self):
        print(type(self))
        tipe = str(type(self))
        if type(self) == "<class 'stars.facility.Facility'>":
            return self.facility_type
        if type(self) == "<class 'stars.ship_design.ShipDesign'>":
            return self.name
        if type(self) == "<class 'stars.ship.Ship'>":
            return self.ship_design.name
        if type(self) == "<class 'stars.terraform.Terraform'>":
            return self.name
        return 'unknown'
#        if type(self) == 'fleet'?


BuildQueue.set_defaults(BuildQueue, __defaults)
