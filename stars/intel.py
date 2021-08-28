import copy
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'name': '',
    'date': '',
}


""" Historical field tracking """
TRACK_HISTORY = {
    'Ship': ['location_root'],
    'Asteroid': ['location_root'],
}

""" Accumulating within the date """
TRACK_ACCUMULATING = {
    'Planet': ['Finance Minister: Income', 
               'Finance Minister: Ship', 
               'Finance Minister: StarBase', 
               'Finance Minister: Facility', 
               'Finance Minister: baryogenesis', 
               'Finance Minister: MatTrans', 
               'Finance Minister: Research', 
               'Finance Minister: Other'],
    'Player': ['energy',
               'minerals',
               'tech_levels',
               'planets',
               'ships_unarmed',
               'ships_escort',
               'ships_of_the_wall',
               'facilities',
               'starbases',
               'score',
               'score_rank'],
}

""" Class for the players view of the galaxy """
class Intel(Defaults):
    """ Add a report with specal handling for location to lock to an x, y, z """
    def add_report(self, reference, date, report):
        # Special handling for locations to remove relative and reduce memory size
        if 'location' in report:
            report['location_root'] = report['location'].root_location.xyz
            report['system_key'] = '{:.20f},{:.20f},{:.20f}'.format(*(report['location'].xyz))
            report['location'] = report['location'].xyz
        self.date = date
        for key in report:
            # Capture historical when the date changes
            if key in TRACK_HISTORY.get(+reference, []):
                if hasattr(self, key):
                    last_date = list(self[key].keys())[-1]
                    if self[key][last_date] != report[key]:
                        self[key][date] = copy.copy(report[key])
                else:
                    self[key] = {}
                    self[key][date] = copy.copy(report[key])
            # Special handling for locations to remove relative and reduce memory size
            elif key in TRACK_ACCUMULATING.get(+reference, []):
                if not hasattr(self, key):
                    self[key] = {}
                self[key][date] = self[key].get(date, 0.0) + report[key]
            else:
                self[key] = copy.copy(report[key])

    """ Get a value """
    def get(self, key, default=None):
        value = getattr(self, key, default)
        if isinstance(value, dict):
            last_date = list(self[key].keys())[-1]
            return value[last_date]
        return value

    """ Assume historical or accumulating """
    def getall(self, key):
        return getattr(self, key, {})

Intel.set_defaults(Intel, __defaults)


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
