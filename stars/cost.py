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
        c = Cost(super().__add__(other))
        c.energy = self.energy + getattr(other, 'energy', 0)
        return c

    """ Subtracton operator """
    def __sub__(self, other):
        c = Cost(super().__sub__(other))
        c.energy = self.energy - getattr(other, 'energy', 0)
        return c

    """ Mutiply operator """
    def __mul__(self, other):
        m = super().__mul__(other)
        c = Cost(**m.__dict__)
        c.energy = self.energy * other
        return c
    
    """ Divide operator """
    def __truediv__(self, other):
        m = super().__truediv__(other)
        c = Cost(**m.__dict__)
        c.energy = self.energy / other
        return c
    
    """ percent done of other """
    def percent(self, other): #where self is remaining cost and other is original cost
        if other.is_zero(): 
            return 100
        denom = other.energy / 100 + other.titanium + other.lithium + other.silicon
        p = self.energy / 100 + self.titanium + self.lithium + self.silicon
        return int(100 * (1 - (p / denom)))
    
    """ Format the tech level for HTML """
    def to_html(self):
        html = ''
        if self.energy > 0:
            html += '<i class="fa-bolt" title="Energy">' + str(self.energy) + '</i>'
        if self.titanium > 0:
            html += '<i class="ti" title="Titanium">' + str(round(self.titanium)) + '</i>'
        if self.lithium > 0:
            html += '<i class="li" title="Lithium">' + str(round(self.lithium)) + '</i>'
        if self.silicon > 0:
            html += '<i class="si" title="Silicon">' + str(round(self.silicon)) + '</i>'
        return html


Cost.set_defaults(Cost, __defaults)
