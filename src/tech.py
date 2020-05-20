from .cost import Cost
from .defaults import Defaults
from .tech_level import TechLevel


""" Default values (default, min, max)  """
__defaults = {
    'cost': [Cost()],
    'level': [TechLevel()],
    'race_requirements': ['']
}


""" Represent 'minerals' """
class Tech(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Tech.set_defaults(Tech, __defaults)
