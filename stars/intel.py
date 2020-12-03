import copy
from . import game_engine
from .location import Location

""" 
Class for the players view of the galaxy 
Reports are dictionaries stored in reverse order
The latest report is a merge of all reports
"""
class Intel(game_engine.BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'latest'):
            self.latest = {'date': 0.0}
            self.reports = []

    """ Always update the 'latest' intel, old reports are ignored """
    def add_report(self, **kwargs):
        report = {}
        for key in kwargs:
            if key == 'location':
                report[key] = Location(x=kwargs[key].x, y=kwargs[key].y, z=kwargs[key].z)
            else:
                report[key] = copy.copy(kwargs[key])
        if 'date' not in report:
            report['date'] = self.latest['date']
        # ignore old reports
        if report['date'] < self.latest['date']:
            return
        # already got a report this turn so update
        elif report['date'] == self.latest['date'] and len(self.reports) > 0:
            self.reports[0].update(report)
        else:
            self.reports.insert(0, report)
        self.latest.update(report)

    def get(self, attribute=None, date=None, default=None):
        report = self.latest
        if date:
            for report in self.reports:
                if report['date'] == date:
                     break
        if not attribute:
            return report
        if attribute not in report:
            return default
        return report[attribute]

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
