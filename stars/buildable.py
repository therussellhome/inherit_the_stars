import sys
from .defaults import Defaults
from .cost import Cost

""" Default values (default, min, max)  """
__defaults = {
    'name': [''],
    'description': [''],
    'cost': [Cost()],
    'cost_complete': [Cost()],
    'is_end_item': [False]
}

""" Represent 'cost' """
class Buildable(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Register the class with the game engine
Buildable.set_defaults(Buildable, __defaults)
