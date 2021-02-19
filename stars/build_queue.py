from .cost import Cost
from .defaults import Defaults
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'cost': Cost(), # cost remaining
    'planet': Reference('Planet'),
    'baryogenesis': False,
}


""" Base class for the build queue """
class BuildQueue(Defaults):
    """ Child classes should override this to set the cost """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Child classes need to override this """
    def finish(self):
        pass


BuildQueue.set_defaults(BuildQueue, __defaults)
