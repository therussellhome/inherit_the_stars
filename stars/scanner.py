import sys
from . import stars_math
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'anti_cloak': [0.0, 0.0, sys.maxsize],
    'penetrating': [0.0, 0.0, sys.maxsize],
    'normal': [0.0, 0.0, sys.maxsize]
}


""" Represent 'scanner' """
class Scanner(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Calculate the range an apparent mass is visible at """
    def range_visible(self, apparent_mass):
        visible_at = self.anti_cloak
        if apparent_mass > 0:
            visible_at = min(visible_at, self.penetrating)
            ly_per_kt = self.normal / 100.0
            visible_at = min(visible_at, apparent_mass * ly_per_kt)
        return visible_at

    """ Stack another scanner with this one """
    def stack(self, scanner):
        s = Scanner()
        s.anti_cloak = stars_math.volume_add(self.anti_cloak, scanner.anti_cloak)
        s.penetrating = stars_math.volume_add(self.penetrating, scanner.penetrating)
        s.normal = stars_math.volume_add(self.normal, scanner.normal)
        return s

Scanner.set_defaults(Scanner, __defaults)
