from .cost import Cost
from .defaults import Defaults
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'cost': Cost(), # cost remaining
    'spent': Cost(), # cost applied so far
    'planet': Reference('Planet'), # where the thing is being built
    'baryogenesis': False,
}


""" Base class for the build queue """
class BuildQueue(Defaults):
    """ Apply effort, child classes should override to determine when finished """
    def build(self, spend=Cost()):
        self.spent += spend
        self.cost -= spend
        return self.cost

    """ Called when being removed from the build queue """
    def cancel(self):
        pass

    """ Build for display, child classes should override """
    def to_html(self):
        return '??? mystery item ???'


BuildQueue.set_defaults(BuildQueue, __defaults)
