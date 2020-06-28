import sys
import math
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

    def add(self, scanner):
        s = Scanner()
        s.anti_cloak = volume_add(self.anti_cloak, scanner.anti_cloak)
        s.penetrating = volume_add(self.penetrating, scanner.penetrating)
        s.normal = volume_add(self.normal, scanner.normal)
        return s

Scanner.set_defaults(Scanner, __defaults)

def volume_add(r1, r2):
    if r1 == 0:
        return r2
    if r2 == 0:
        return r1
    v1 = 4.0 / 3.0 * math.pi * (r1 ** 3.0)
    v2 = 4.0 / 3.0 * math.pi * (r2 ** 3.0)
    v = v1 + v2
    r = ((3.0 * v) / (4.0 * math.pi)) ** (1.0/3.0)
    return math.round(r * 100) / 100
