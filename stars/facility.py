from .build_queue import BuildQueue
from .cost import Cost


""" Default values (default, min, max)  """
__defaults = {
    'facility_type': 'power_plants',
}


""" Facility types """
FACILITY_TYPES = ['power_plants', 'factories', 'mines', 'defenses']


""" Facility costs """
_facility_costs = {
    'power_plants': Cost(titanium=1, lithium=1, silicon=2, energy=250),
    'factories': Cost(titanium=1, lithium=0, silicon=1, energy=250),
    'mines': Cost(titanium=0, lithium=1, silicon=0, energy=500),
    'defenses': Cost(titanium=3, lithium=0, silicon=3, energy=400), 
}

""" Facility names """
_facility_names = {
    'power_plants': 'Power Plant',
    'factories': 'Factory',
    'mines': 'Mineral Extractor',
    'defenses': 'Planetary Shield',
}

""" Temporary class to indicate facility in process """
class Facility(BuildQueue):
    """ Store the cost to build the facility """
    def __init__(self, **kwargs):
        global _facility_costs
        super().__init__(**kwargs)
        self.cost = _facility_costs[self.facility_type]

    """ Check if we are completed """
    def build(self, spend=Cost()):
        super().build(spend)
        if self.cost.is_zero():
            self.planet[self.facility_type] += 1
        return self.cost

    """ Build queue display """
    def to_html(self):
        global _facility_names
        return _facility_names[self.facility_type]


Facility.set_defaults(Facility, __defaults)
