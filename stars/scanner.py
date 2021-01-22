import sys
from . import game_engine
from . import stars_math
from .defaults import Defaults
from .reference import Reference


""" Location binning """
__RANGE_BIN_SIZE = 50
__MASS_BIN_MAX = 5000
# First level of bins is the player
# Second level for the cloak, insystem, and bymass bins is a tuple of (x_bin, y_bin, z_bin)
# The bymass bins are further indexed by a mass bin where objects are in all mass bins from 0 to their apparent mass
# Objects larger than __MASS_BIN_MAX go in the 'massive' bin
__bins_cloak = {}
__bins_penetrating = {}
__bins_bymass = {}
__bins_massive = {}


""" Clear the bins prior to updating them """
def reset_scan_bins(players):
    global __bins_cloak, __bins_penetrating, __bins_bymass, __bins_massive
    __bins_cloak = {}
    __bins_penetrating = {}
    __bins_bymass = {}
    __bins_massive = {}
    for p in players:
        p_ref = Reference(p)
        __bins_cloak[p_ref] = {}
        __bins_penetrating[p_ref] = {}
        __bins_bymass[p_ref] = {}
        __bins_massive[p_ref] = {}


""" Update a location """
def bin_for_scanning(obj, location, apparent_mass, has_cloak=False, in_system=False):
    global __bins_cloak, __bins_penetrating, __bins_bymass, __bins_massive, __RANGE_BIN_SIZE, __MASS_BIN_SIZE, __MASS_BIN_MAX
    o_ref = Reference(obj)
    b = (int(location.x / __RANGE_BIN_SIZE), int(location.y / __RANGE_BIN_SIZE), int(location.z / __RANGE_BIN_SIZE))
    if has_cloak:
        _add_to_bin(__bins_cloak, o_ref, b)
    if apparent_mass > 0:
        _add_to_bin(__bins_penetrating, o_ref, b)
        if not in_system:
            if apparent_mass > __MASS_BIN_MAX:
                _add_to_bin(__bins_massive, o_ref, b)
            else:
                _add_to_bin(__bins_bymass, o_ref, b, int(apparent_mass / __MASS_BIN_SIZE))


""" Add to bin """
def _add_to_bin(which_bin, o_ref, b, mass_bin = None):
    global __MASS_BIN_SIZE, __MASS_BIN_MAX
    for p_ref in which_bin:
        if not mass_bin:
            if b not in which_bin[p_ref]:
                which_bin[p_ref][b] = []
            which_bin[p_ref][b].append(o_ref)
        else:
            if b not in which_bin[p_ref]:
                which_bin[p_ref][b] = [[]] * int(__MASS_BIN_MAX / __MASS_BIN_SIZE)
            for m in range(mass_bin + 1):
                which_bin[p_ref][b][m].append(o_ref)
            print(which_bin[p_ref][b])


""" ONLY FOR TESTING """
def _bin_testing(cloak=False, penetrating=False, bymass=False, massive=False):
    global __bins_cloak, __bins_penetrating, __bins_bymass, __bins_massive
    if cloak:
        return __bins_cloak
    if penetrating:
        return __bins_penetrating
    if bymass:
        return __bins_bymass
    if massive:
        return __bins_massive


""" Search the bins and return the ships seen """
def _bin_scan_cloak(p_ref, location, anti_cloak):
    return []


""" Search the bins and return the ships seen """
def _bin_scan_penetrating(p_ref, location, penetrating):
    return []


""" Search the bins and return the ships seen """
def _bin_scan_normal(p_ref, location, normal):
    return []


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
