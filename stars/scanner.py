import sys
from . import game_engine
from . import stars_math
from .defaults import Defaults
from .reference import Reference


""" Location binning """
__RANGE_BIN_SIZE = 50
# First level of bins is the player
# Second level is a tuple of (x_bin, y_bin, z_bin)
__bins = {}


""" Clear the bins prior to updating them """
def reset_scan_bins(players):
    global __bins
    __bins = {}
    for p in players:
        __bins[Reference(p)] = {}


""" Update a location """
def bin_for_scanning(obj, location, ke, apparent_mass, has_cloak=False):
    global __bins, __RANGE_BIN_SIZE
    b = (int(location.x / __RANGE_BIN_SIZE), int(location.y / __RANGE_BIN_SIZE), int(location.z / __RANGE_BIN_SIZE))
    o = {'obj':obj, 'location':location, 'ke':ke, 'apparent_mass':apparent_mass, 'has_cloak':has_cloak, 'bin':b}
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
    __bins[Reference(p_ref)][o.bin].remove(o)


""" Search the bins and return the ships seen """
def _bin_scan_hyperdenial(p_ref, location, hyperdenial):
    objs = []
    for o in _bin_scan(p_ref, location, hyperdenial):
        if o.ke > 0 and location - o.location < hyperdenial:
            _bin_found(p_ref, o)
            objs.append(o)
    return objs


""" Search the bins and return the ships seen """
def _bin_scan_anticloak(p_ref, location, anti_cloak):
    objs = []
    for o in _bin_scan(p_ref, location, anti_cloak):
        if o.has_cloak and location - o.location < anti_cloak:
            _bin_found(p_ref, o)
            objs.append(o)
    return objs


""" Search the bins and return the ships seen """
def _bin_scan_penetrating(p_ref, location, penetrating):
    objs = []
    for o in _bin_scan(p_ref, location, penetrating):
        if o.apparent_mass > 0 and location - o.location < penetrating:
            _bin_found(p_ref, o)
            objs.append(o)
    return objs


""" Search the bins and return the ships seen """
def _bin_scan_normal(p_ref, location, normal):
    objs = []
    for o in _bin_scan(p_ref, location, normal):
        distance = location - o.location
        if not o.location.in_system and o.apparent_mass > 0 and distance < normal and o.ke > ((-500000 * normal) / (distance - normal) - 500000):
            _bin_found(p_ref, o)
            objs.append(o)
    return objs


""" Default values (default, min, max)  """
__defaults = {
    'anti_cloak': (0.0, 0.0, sys.maxsize),
    'penetrating': (0.0, 0.0, sys.maxsize),
    'normal': (0.0, 0.0, sys.maxsize),
}


""" Represent 'scanner' """
class Scanner(Defaults):
    """ Calculate the range an apparent mass is visible at """
    def range_visible(self, apparent_mass):
        visible_at = 0
        if apparent_mass > 0:
            visible_at = max(visible_at, self.penetrating)
            ly_per_kt = self.normal / 100.0
            visible_at = max(visible_at, apparent_mass * ly_per_kt)
        return visible_at

    """ Addition operator """
    def __add__(self, other):
        s = Scanner()
        s.anti_cloak = stars_math.volume_add(self.anti_cloak, other.anti_cloak)
        s.penetrating = stars_math.volume_add(self.penetrating, other.penetrating)
        s.normal = stars_math.volume_add(self.normal, other.normal) 
        return s

    """ Add scan reports to the player from a location """
    def scan(self, player, location):
        p_ref = Reference(player)
        if self.anti_cloak > 0:
            for obj in _bin_scan_cloak(p_ref, location, self.anti_cloak):
                self._scan_report(player, obj, anti_cloak=True)
        if self.penetrating > 0:
            for obj in _bin_scan_penetrating(p_ref, location, self.penetrating):
                self._scan_report(player, obj)
        if self.normal > 0:
            for obj in _bin_scan_normal(p_ref, location, self.normal):
                self._scan_report(player, obj)

    """ Report about an object """
    def _scan_report(self, player, obj, anti_cloak=False):
        report = {}
        if isinstance(obj, Ship):
            report['location'] = obj.location
            report['player'] = obj.player
            if anti_cloak:
                report['actual_mass'] = obj.calc_mass()
            else:
                report['apparent_mass'] = obj.calc_apparent_mass()
        elif isinstance(obj, Asteroid):
            report['location'] = obj.location
            report['mass'] = obj.mass
            report['kinetic_energy'] = obj.kinetic_energy
        elif isinstance(obj, Wormhole):
            report['location'] = obj.location
        elif isinstance(obj, Planet):
            report['location'] = obj.location
            report['color'] = obj.get_color()
            report['gravity'] = obj.gravity
            report['temperature'] = obj.temperature
            report['radiation'] = obj.radiation
            if obj.is_colonized():
                report['player']: obj.player
                report['population']: obj.on_surface.people
            report['lithium availability']: obj.mineral_availability('lithium')
            report['silicon availability']: obj.mineral_availability('silicon')
            report['titanium availability']: obj.mineral_availability('titanium')
        player.add_intel(**report)


Scanner.set_defaults(Scanner, __defaults)
