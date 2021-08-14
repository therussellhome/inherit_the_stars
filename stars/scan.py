import sys
from . import binning
from .reference import Reference


# Unscanned ships
# First level of bins is the player
# Second level is the bin number
__unscanned = {}
# Post scan bins
__scanned = {}


""" Clear the bins prior to updating them """
def reset(players):
    global __unscanned
    __unscanned = {}
    __scanned = {}
    for p in players:
        __unscanned[Reference(p)] = {}
        __scanned[Reference(p)] = {}


""" Update a location """
def add(obj, location, apparent_mass, ke, is_ship=False, has_cloak=False, in_system=False):
    global __unscanned
    b = binning.num(location)
    o = {'obj':obj, 'location':location, 'apparent_mass':apparent_mass, 'ke':ke, 'is_ship':is_ship, 'has_cloak':has_cloak, 'in_system':in_system, 'bin':b}
    for p in __unscanned:
        if b not in __unscanned[p]:
            __unscanned[p][b] = []
        __unscanned[p][b].append(o)


""" ONLY FOR TESTING """
def _bin_testing(scanned=False):
    global __unscanned, __scanned
    if scanned:
        return __scanned
    return __unscanned


""" Found in bin """
def _bin_found(p_ref, o):
    global __unscanned, __RANGE_BIN_SIZE
    __unscanned[p_ref][o['bin']].remove(o)
    __scanned[p_ref][o['bin']].append(o)


""" Search the bins and return the ships seen """
def anticloak(player, location, rng):
    global __unscanned
    p_ref = Reference(player)
    for o in binning.search(__unscanned[p_ref], location, rng):
        if o['has_cloak'] and location - o['location'] < rng:
            _bin_found(p_ref, o)
            player.add_intel(o['obj'], **(o['obj'].scan_report(scan_type='anticloak')))


""" Search the bins and return the ships seen """
def penetrating(player, location, rng):
    global __unscanned
    p_ref = Reference(player)
    for o in binning.search(__unscanned[p_ref], location, rng):
        if o['apparent_mass'] > 0 and location - o['location'] < rng:
            _bin_found(p_ref, o)
            player.add_intel(o['obj'], **(o['obj'].scan_report(scan_type='penetrating')))


""" Search the bins and return the ships seen """
def normal(player, location, rng):
    global __unscanned
    p_ref = Reference(player)
    for o in binning.search(__unscanned[p_ref], location, rng):
        distance = location - o['location']
        if not o['in_system'] and o['apparent_mass'] > 0 and distance < rng and o['ke'] > ((-500000 * rng) / (distance - rng) - 500000):
            _bin_found(p_ref, o)
            player.add_intel(o['obj'], **(o['obj'].scan_report(scan_type='normal')))


""" Report on ships seen moving in hyperdenial fields, hyperdenial does its own binning """
def hyperdenial(fleet, players):
    for player in players:
        for ship in fleet.ships:
            player.add_intel(ship, **(ship.scan_report(scan_type='hyperdenial')))


""" Search for closest enemy """
def patrol(player, location, rng):
    global __scanned
    p_ref = Reference(player)
    closest_distance = sys.maxsize
    closest_object = None
    for o in binning.search(__scanned[p_ref], location, rng):
        if o['is_ship'] and player.get_relation(o['obj'].player) == 'enemy':
            distance = location - o['location']
            if distance < closest_distance:
                closest_distance = distance
                closest_object = o['obj']
    if closest_object:
        return Location(reference=closest_object)
    return location
