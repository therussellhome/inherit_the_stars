import sys
from .minerals import Minerals


""" Default values (default, min, max)  """
__defaults = {
    'energy': (0, 0, sys.maxsize),
}


""" Represent 'cost' """
class Cost(Minerals):
    """ Test if the cost is zero """
    def is_zero(self):
        return (self.energy == 0 and super().is_zero())

    """ Addition operator """
    def __add__(self, other):
        m = super().__add__(other)
        c = Cost(**m.__dict__)
        c.energy = self.energy + other.energy
        return c

    """ Subtracton operator """
    def __sub__(self, other):
        m = super().__sub__(other)
        c = Cost(**m.__dict__)
        c.energy = self.energy - other.energy
        return c

    """ Mutiply operator """
    def __mul__(self, other):
        m = super().__mul__(other)
        c = Cost(**m.__dict__)
        c.energy = self.energy * other
        return c
    
    """ percent of other """
    def percent(self, other): #where self is remaining cost and other is original cost
        den = other.energy / 100 + other.titanium + other.lithium + other.silicon
        p = self.energy / 100 + self.titanium + self.lithium + self.silicon
        return round((p * 100) / den) # TODO Pam please code and add tests
    
    """ Format the tech level for HTML """
    def to_html(self):
        html = ''
        if self.energy > 0:
            html += '<i class="fa-bolt" title="Energy">' + str(self.energy) + '</i>'
        if self.titanium > 0:
            html += '<i class="ti" title="Titanium">' + str(self.titanium) + '</i>'
        if self.lithium > 0:
            html += '<i class="li" title="Lithium">' + str(self.lithium) + '</i>'
        if self.silicon > 0:
            html += '<i class="si" title="Silicon">' + str(self.silicon) + '</i>'
        return html


Cost.set_defaults(Cost, __defaults)
