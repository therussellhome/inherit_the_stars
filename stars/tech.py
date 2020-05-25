from .buildable import Buildable
from .tech_level import TechLevel


""" Default values (default, min, max)  """
__defaults = {
    'level': [TechLevel()],
    'race_requirements': ['']
}


""" Represent 'minerals' """
class Tech(Buildable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Tech.set_defaults(Tech, __defaults)
