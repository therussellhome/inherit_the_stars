import copy
from .defaults import Defaults
from .location import Location


""" Default values (default, min, max)  """
__defaults = {
    'name': '',
    'date': '',
}


""" Class for the players view of the galaxy """
class Intel(Defaults):
    """ Add a report with specal handling for location to lock to an x, y, z """
    def add_report(self, **kwargs):
        for key in kwargs:
            # Special handling for locations to remove relative and reduce memory size
            if key == 'location':
                self[key] = kwargs[key].xyz
                self[location_root] = str(kwargs[key].root_location.xyz)
            else:
                self[key] = copy.copy(kwargs[key])


Intel.set_defaults(Intel, __defaults)


""" Default values (default, min, max)  """
__defaults_history = {
    'location_history': {},
    'location_root_history': {},
}


""" Add tracking of location history """
class IntelHistory(Intel):
    """ Extend locatin handling to include a history of when seen """
    def add_report(self, **kwargs):
        super().add_report(**kwargs)
        if 'location' in kwargs:
            self.location_history[self.date] = self.location
            self.location_root_history[self.date] = self.location_root


IntelHistory.set_defaults(IntelHistory, __defaults_history)


""" Propogate ship along current path using last 2 locations for speed and direction
** MOVE THIS TO ANOTHER CLASS
def propogate(self, future):
    if 'location' not in self.__dict__:
        return Location
    if len(self.location) == 1:
        return self.location[0].report
    curr = self.location[0].report
    prev = self.location[1].report
    time = self.location[0].date
    d_time = time - self.location[1].date
    dx = curr.x - prev.x
    dy = curr.y - prev.y
    dz = curr.z - prev.z
    x = curr.x + dx / d_time * (future - time)
    y = curr.y + dy / d_time * (future - time)
    z = curr.z + dz / d_time * (future - time)
    return Location(x=x, y=y, z=z)
"""
