import sys
from .reference import Reference


""" Location binning """
__RANGE_BIN_SIZE = 50
# First level of bins is the player
# Second level is a tuple of (x_bin, y_bin, z_bin)
__bins = {}


""" Clear the bins prior to updating them """
def reset(players):
    global __bins
    __bins = {}
    for p in players:
        __bins[Reference(p)] = {}


""" Update a location """
def add(obj, location, apparent_mass, ke, has_cloak=False, in_system=False):
    global __bins, __RANGE_BIN_SIZE
    b = (int(location.x / __RANGE_BIN_SIZE), int(location.y / __RANGE_BIN_SIZE), int(location.z / __RANGE_BIN_SIZE))
    o = {'obj':obj, 'location':location, 'apparent_mass':apparent_mass, 'ke':ke, 'has_cloak':has_cloak, 'in_system':in_system, 'bin':b}
    for p in __bins:
        if b not in __bins[p]:
            __bins[p][b] = []
        __bins[p][b].append(o)


""" ONLY FOR TESTING """
def _bin_testing():
    global __bins
    return __bins


""" Basic bin list """
def _bin_scan(p_ref, location, rng):
    global __bins, __RANGE_BIN_SIZE
    objs = []
    for x in range(int((location.x - rng) / __RANGE_BIN_SIZE), int((location.x + rng) / __RANGE_BIN_SIZE) + 1):
        for y in range(int((location.y - rng) / __RANGE_BIN_SIZE), int((location.y + rng) / __RANGE_BIN_SIZE) + 1):
            for z in range(int((location.z - rng) / __RANGE_BIN_SIZE), int((location.z + rng) / __RANGE_BIN_SIZE) + 1):
                objs.extend(__bins[p_ref].get((x, y, z), []))
    return objs


""" Found in bin """
def _bin_found(p_ref, o):
    global __bins, __RANGE_BIN_SIZE
    __bins[Reference(p_ref)][o['bin']].remove(o)


""" Search the bins and return the ships seen """
def anticloak(player, location, rng):
    p_ref = Reference(player)
    for o in _bin_scan(p_ref, location, rng):
        if o['has_cloak'] and location - o['location'] < rng:
            _bin_found(p_ref, o)
            player.add_intel(o['obj'], **(o['obj'].scan_report(scan_type='anticloak')))


""" Search the bins and return the ships seen """
def penetrating(player, location, rng):
    p_ref = Reference(player)
    for o in _bin_scan(p_ref, location, rng):
        if o['apparent_mass'] > 0 and location - o['location'] < rng:
            _bin_found(p_ref, o)
            player.add_intel(o['obj'], **(o['obj'].scan_report()))


""" Search the bins and return the ships seen """
def normal(player, location, rng):
    p_ref = Reference(player)
    for o in _bin_scan(p_ref, location, rng):
        distance = location - o['location']
        if not o['in_system'] and o['apparent_mass'] > 0 and distance < rng and o['ke'] > ((-500000 * rng) / (distance - rng) - 500000):
            _bin_found(p_ref, o)
            player.add_intel(o['obj'], **(o['obj'].scan_report()))

""" Search the bins and return the ships seen """
def hyperdenial(player, location, rng):
    p_ref = Reference(player)
    for o in _bin_scan(p_ref, location, rng):
        if o['ke'] > 0 and location - o['location'] < rng:
            _bin_found(p_ref, o)
            player.add_intel(o['obj'], **(o['obj'].scan_report(scan_type='hyperdenial')))
