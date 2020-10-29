import math

""" 
Tm * constant = ly
ly / constant = Tm
"""
TERAMETER_2_LIGHTYEAR = 0.000105702977392

""" Distance between points """
def distance(x1, y1, z1, x2, y2, z2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5

""" Add volumes """
def volume_add(r1, r2):
    if r1 == 0:
        return r2
    if r2 == 0:
        return r1
    v1 = 4.0 / 3.0 * math.pi * (r1 ** 3.0)
    v2 = 4.0 / 3.0 * math.pi * (r2 ** 3.0)
    v = v1 + v2
    r = ((3.0 * v) / (4.0 * math.pi)) ** (1.0/3.0)
    return round(r, 2)
