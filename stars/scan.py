import copy
import sys
from . import binning
from .reference import Reference


# Unscanned ships
# First level of bins is the player
# Second level is the bin number
__anticloak = {}
__penetrating = {}
__normal = {}
# Post scan bins
__scanned = {}


""" Clear the bins prior to updating them """
def reset(players, fleets, planets, asteroids, wormholes, nebulae, mystery_traders):
    global __anticloak, __penetrating, __normal, __scanned
    if len(players) == 0:
        __anticloak = {}
        __penetrating = {}
        __normal = {}
        __scanned = {}
        return
    p0 = Reference(players[0])
    __anticloak = {p0: {} }
    __penetrating = {p0: {} }
    __normal = {p0: {} }
    __scanned = {p0: {} }
    # Ships can be cloaked so they are visible in anticloak, penetrating, and normal
    for f in fleets:
        for s in f.ships:
            reference = Reference(s)
            bin_num = binning.num(s.location)
            if s['total_mass'] != s['apparent_mass']:
                if bin_num not in __anticloak[p0]:
                    __anticloak[p0][bin_num] = []
                __anticloak[p0][bin_num].append(reference)
            if s['apparent_mass'] > 0.0:
                if bin_num not in __penetrating[p0]:
                    __penetrating[p0][bin_num] = []
                __penetrating[p0][bin_num].append(reference)
            if s['apparent_ke'] > 0.0 and not s.location.in_system:
                if bin_num not in __normal[p0]:
                    __normal[p0][bin_num] = []
                __normal[p0][bin_num].append(reference)
    # Planets are only visible in penetrating
    for p in planets:
        reference = Reference(p)
        bin_num = binning.num(p.location)
        if bin_num not in __penetrating[p0]:
            __penetrating[p0][bin_num] = []
        __penetrating[p0][bin_num].append(reference)
    # Asteroids can be cloaked so they are visible in anticloak, penetrating, and normal
    for a in asteroids:
        reference = Reference(a)
        bin_num = binning.num(a.location)
        if a['total_mass'] != a['apparent_mass']:
            if bin_num not in __anticloak[p0]:
                __anticloak[p0][bin_num] = []
            __anticloak[p0][bin_num].append(reference)
        if a['apparent_mass'] > 0.0:
            if bin_num not in __penetrating[p0]:
                __penetrating[p0][bin_num] = []
            __penetrating[p0][bin_num].append(reference)
        if a['apparent_ke'] > 0.0 and not a.location.in_system:
            if bin_num not in __normal[p0]:
                __normal[p0][bin_num] = []
            __normal[p0][bin_num].append(reference)
    # Wormholes are only visible in penetrating
    for w in wormholes:
        reference = Reference(w)
        bin_num = binning.num(w.location)
        if bin_num not in __penetrating[p0]:
            __penetrating[p0][bin_num] = []
        __penetrating[p0][bin_num].append(reference)
    # TODO nebulae
    # Mystery traders are visible in penetrating and normal
    for m in mystery_traders:
        reference = Reference(m)
        bin_num = binning.num(m.location)
        if bin_num not in __penetrating[p0]:
            __penetrating[p0][bin_num] = []
        __penetrating[p0][bin_num].append(reference)
        if bin_num not in __normal[p0]:
            __normal[p0][bin_num] = []
        __normal[p0][bin_num].append(reference)
    # Copy to every other player
    for p in players[1:]:
        p = Reference(p)
        __anticloak[p] = copy.copy(__anticloak[p0])
        __penetrating[p] = copy.copy(__penetrating[p0])
        __normal[p] = copy.copy(__normal[p0])
        __scanned[p] = {}


""" ONLY FOR TESTING """
def _bin_testing(scanned=False):
    global __normal, __scanned
    if scanned:
        return __scanned
    return __normal


""" Found in bin """
def _bin_found(bins, p_ref, reference, bin_num):
    global __scanned
    bins[p_ref][bin_num].remove(reference)
    if bin_num not in __scanned[p_ref]:
        __scanned[p_ref][bin_num] = []
    if reference not in __scanned[p_ref][bin_num]:
        __scanned[p_ref][bin_num].append(reference)


""" Search the bins and return the ships seen """
def anticloak(player, location, rng):
    global __anticloak
    p_ref = Reference(player)
    for (reference, bin_num) in binning.search(__anticloak[p_ref], location, rng):
        if location - reference.location < rng:
            _bin_found(__anticloak, p_ref, reference, bin_num)
            player.add_intel(reference, reference.scan_report(scan_type='anticloak'))


""" Search the bins and return the ships seen """
def penetrating(player, location, rng):
    global __penetrating
    p_ref = Reference(player)
    for (reference, bin_num) in binning.search(__penetrating[p_ref], location, rng):
        if location - reference.location < rng:
            _bin_found(__penetrating, p_ref, reference, bin_num)
            player.add_intel(reference, reference.scan_report(scan_type='penetrating'))


""" Search the bins and return the ships seen """
def normal(player, location, rng):
    global __normal
    p_ref = Reference(player)
    for (reference, bin_num) in binning.search(__normal[p_ref], location, rng):
        distance = location - reference.location
        if distance < rng and reference['apparent_ke'] > ((-500000 * rng) / (distance - rng) - 500000):
            _bin_found(__normal, p_ref, reference, bin_num)
            player.add_intel(reference, reference.scan_report(scan_type='normal'))


""" Report on ships seen moving in hyperdenial fields, hyperdenial does its own binning """
def hyperdenial(fleet, players):
    for player in players:
        for ship in fleet.ships:
            player.add_intel(ship, ship.scan_report(scan_type='hyperdenial'))


""" Search for closest enemy """
def patrol(player, location, rng):
    global __scanned
    p_ref = Reference(player)
    closest_distance = sys.maxsize
    closest_object = None
    for (reference, bin_num) in binning.search(__scanned[p_ref], location, rng):
        if reference ^ 'Ship' and player.get_relation(reference.player) == 'enemy':
            distance = location - reference.location
            if distance < closest_distance:
                closest_distance = distance
                closest_object = reference
    if closest_object:
        return Location(reference=closest_object)
    return location
