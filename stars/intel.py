import copy
from . import game_engine
from .location import Location

""" Class for an individual report """
class IntelReport(game_engine.BaseClass):
    def __init__(self, *args, **kwargs):
        if 'date' in kwargs:
            self.date = kwargs['date']
        else:
            self.date = game_engine.get('Game/')[0].date
        if 'report' in kwargs:
            self.report = kwargs['report']
        else:
            self.report = args[0]

""" 
Class for the players view of the galaxy 
Reports are stored with the newest report at the front of the list
Reports are tuples of (date, information)
"""
class Intel(game_engine.BaseClass):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    """ Newest reports are always at the front of the list """
    def addReport(self, **kwargs):
        now = game_engine.get('Game/')[0].date
        for name in kwargs:
            reports = getattr(self, name, [])
            if len(reports) > 0:
                if reports[0].date != now:
                    reports.insert(0, IntelReport(copy.copy(kwargs[name])))
            else:
                reports.append( (now, copy.copy(kwargs[name])) )
            setattr(self, name, reports)
        self.last_report = now

    """ Propogate ship along current path using last 2 locations for speed and direction """
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
        
