from .cost import Cost
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'under_construction': [True],
}


""" Buildable base class for use in the build queue """
class Buildable(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Return the cost to build - must be overridden by child class """
    def add_to_build_queue(self, race=None, upgrade_to=None):
        self.under_construction = True
        return Cost()

    """ Mark the item as completed """
    def build_complete(self, race=None, upgrade_to=None):
        self.under_construction = False

Buildable.set_defaults(Buildable, __defaults)
