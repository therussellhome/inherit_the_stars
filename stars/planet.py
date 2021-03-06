import sys
from colorsys import hls_to_rgb
from math import cos, sin
from random import randint, uniform
from . import game_engine
from . import stars_math
from .cargo import Cargo
from .cost import Cost
from .defaults import Defaults
from .facility import Facility, FACILITY_TYPES
from .location import Location
from .location import Location
from .minerals import Minerals, MINERAL_TYPES
from .reference import Reference
from .scanner import Scanner
from .tech import Tech
from .terraform import Terraform


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'location': Location(),
    'distance': (50, 0, 100),
    'temperature': (50, -50, 150),
    'radiation': (50, -50, 150),
    'gravity': (50, -50, 150),
    'temperature_terraform': (0, 0, 100),
    'radiation_terraform': (0, 0, 100),
    'gravity_terraform': (0, 0, 100),
    'remaining_minerals': Minerals(),
    'on_surface': Cargo(),
    'player': Reference('Player'),
    'homeworld': False,
    'location': Location(),
    'star_system': Reference('StarSystem'),
    'space_station': [],
    # facilities where the key matches from the facility class
    'power_plants': (0, 0, sys.maxsize),
    'factories': (0, 0, sys.maxsize),
    'mines': (0, 0, sys.maxsize),
    'defenses': (0, 0, sys.maxsize),
}


""" Planets are colonizable by only one player, have minerals, etc """
class Planet(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'temperature' not in kwargs:
            self.temperature = randint(0, 100)
            if 'star_system' in kwargs:
                sun = self.star_system.sun()
                if sun:
                    self.temperature = round(self.distance * 0.35 + sun.temperature * 0.65 + randint(-15, 15))
        if 'radiation' not in kwargs:
            self.radiation = randint(0, 100)
        if 'gravity' not in kwargs:
            self.gravity = min(100, abs(randint(0, 110) - randint(0, 110)))
        if 'remaining_minerals' not in kwargs:
            self.remaining_minerals.titanium += ((randint(1, 100) - 1) ** 0.5) * (((self.gravity * 6 / 100) + 1) * 1000)
            self.remaining_minerals.lithium += ((randint(1, 100) - 1) ** 0.5) * (((self.gravity * 6 / 100) + 1) * 1000)
            self.remaining_minerals.silicon += ((randint(1, 100) - 1) ** 0.5) * (((self.gravity * 6 / 100) + 1) * 1000)
        if 'location' not in kwargs:
            distance_ly = self.distance / 100 * stars_math.TERAMETER_2_LIGHTYEAR
            self.location = Location(reference=self.star_system, offset=distance_ly, lat=0)
        if 'orbit_speed' not in kwargs:
            self.orbit_speed = uniform(0.01, 1.0)
        if 'age' not in kwargs:
            self.age = randint(0, 3000)
        game_engine.register(self)

    """ Get the planets color """
    # return it in a hexdecimal string so the webpage can use it
    def get_color(self):
        t = (min(100, max(0, self.temperature)) / 100) * .75
        r = .5 + (min(100, max(0, self.radiation)) * .005)
        color = hls_to_rgb(t, .5, r)
        color_string = '#' + format(round(color[0] * 255), '02X') + format(round(color[1] * 255), '02X') + format(round(color[2] * 255), '02X')
        return color_string

    """ Code the planet orbiting its star """
    # t = years it takes planet to orbit, min 1 year, max 30 years
    # m = the sun's gravity clicks
    # r = the distance from the sun
    # angle = the planet's angle
    #TODO date = year in 1/100
    #def orbit(self):
    #    return #TODO orbit not finished
    """
        if date < 1:
            date += 1
        else:
            date = 1 + self.age
        r = self.distance
        m = max(self.sun_gravity, 1)
        t = max(1, (((r ** 3)/m) ** .5) * (30/.85))
        angle = date * (360/(100 * t))
        self.y = r * sin(angle)
        self.x = r * cos(angle)
        #"""

    """ Check if the planet is colonized """
    def is_colonized(self):
        return self.on_surface.people > 0

    """ Colonize the planet """
    # player is a Player object (reference created internally)
    def colonize(self, player):
        if self.is_colonized():
            return False
        # only Pa'anuri are allowed to colonize suns
        elif player.race.primary_race_trait == 'Pa\'anuri':
            if self.__class__.__name__ != 'Sun':
                return False
        else:
            if self.__class__.__name__ == 'Sun':
                return False
        self.player = Reference(player)
        #minister = PlanetaryMinister()
        #player.planetary_minister_map[Reference(self)] = 
        return True

    """ Calculate the planet's value for the current player (-100 to 100)
    where
    Hab%=SQRT[(1-g)^2+(1-t)^2+(1-r)^2]*(1-x)*(1-y)*(1-z)/SQRT[3]
    g, t, and r are planet_clicks_from_race_center/race_clicks_from_race_center_to_race_edge
    x=g-1/2 for g>1/2 | x=0 for g<1/2
    y=t-1/2 for t>1/2 | y=0 for t<1/2
    z=r-1/2 for r>1/2 | z=0 for r<1/2
    negative planet value is calculated using the same equasion
    with g, t, and r = 0 if < 1 | g, t, r = value - 1
    and 100 subtracted from the result
    """
    def habitability(self, race, terraform=(0, 0, 0)):
        g = self._calc_range_from_center(self.gravity, race.hab_gravity, race.hab_gravity_stop, terraform[0])
        t = self._calc_range_from_center(self.temperature, race.hab_temperature, race.hab_temperature_stop, terraform[1])
        r = self._calc_range_from_center(self.radiation, race.hab_radiation, race.hab_radiation_stop, terraform[2])
        negative_offset = 0
        if t > 1.0 or r > 1.0 or g > 1.0:
            negative_offset = -100.0
            g = max(0.0, g - 1.0)
            t = max(0.0, t - 1.0)
            r = max(0.0, r - 1.0)
        x = max(0.0, g - 0.5)
        y = max(0.0, t - 0.5)
        z = max(0.0, r - 0.5)
        return round(100 * (((1.0 - g)**2 + (1.0 - t)**2 + (1.0 - r)**2)**0.5) * (1.0 - x) * (1.0 - y) * (1.0 - z) / (3.0**0.5) + negative_offset)

    """ Calculate the distance from the center of the habital range to the planet's attribute
    if inside habitable range return (0..1)
    if outside habitable range return (1..2) bounding at 2
    """
    def _calc_range_from_center(self, planet, race_start, race_stop, terraform):
        race_radius = float(race_stop - race_start) / 2.0
        if race_radius == 0 and planet == race_start:
            return 0.0
        elif race_radius == 0:
            return 2.0
        else:
            return min([2.0, (abs((race_start + race_radius) - planet) - terraform) / abs(race_radius)])

    """ Calculate growth rate """
    def growth_rate(self, race, terraform=(0, 0, 0)):
        return race.growth_rate * self.habitability(race, terraform) / 100.0

    """ Calculate planet's max population """
    def maxpop(self, race):
        return int(200000000.0 / race.body_mass * (6.0 * self.gravity / 100.0 + 1.0))

    """ Grow the current population """
    def have_babies(self):
        # all population calculations are done using people but stored using kT (1000/kT)
        pop = self.on_surface.people * self.player.race.pop_per_kt()
        # adjust rate for planet habitability and turn hundreth
        rate = self.growth_rate(self.player.race, (self.gravity_terraform, self.temperature_terraform, self.radiation_terraform)) / 100.0 / 100.0
        # adjust maxpop for size of the world
        pop = pop + (pop * rate) - (pop * pop / self.maxpop(self.player.race) * rate)
        # population is in whole people but stored in kT
        self.on_surface.people = round(pop) / self.player.race.pop_per_kt()
        return self.on_surface.people

    """ how many facilities can be operated """
    # avoid creating facilities
    def _operate(self, facility_type, ideal=False):
        allocation = getattr(self.player.get_minister(self), facility_type)
        workers = allocation / 100 * self.on_surface.people * self.player.race.pop_per_kt()
        operate = self.player.race[facility_type + '_per_10k_colonists'] * workers / 10000
        if ideal:
            return operate
        return min(self[facility_type], operate)

    """ Incoming! """
    def raise_shields(self):
        return self._operate('defenses') * self.playertech_level.energy * 1234 # TODO Pam please come up with equasion

    """ power plants make energy """
    def generate_energy(self):
        facility_yj =  self._operate('power_plants') * self.player.tech_level.propulsion * 1234 # TODO Pam please come up with equasion
        pop_yj = self.on_surface.people * self.player.race.pop_per_kt() * self.player.race.energy_per_10k_colonists / 10000 / 100
        self.player.energy += facility_yj + pop_yj
        return facility_yj + pop_yj

    """ mines mine the minerals """
    def mine_minerals(self):
        factor = 1 / (self.player.tech_level.weapons + 1) # TODO Pam please come up with equasion
        operate = self._operate('mines')
        for mineral in MINERAL_TYPES:
            availability = self.mineral_availability(mineral)
            self.on_surface[mineral] += round(operate * availability)
            self.remaining_minerals[mineral] -= round(operate * availability * factor)

    """ Availability of the mineral type """
    def mineral_availability(self, mineral):
        return (((self.remaining_minerals[mineral] / (((self.gravity * 6 / 100) + 1) * 1000)) ** 2) / 10) + 0.1

    """ calculates max production capasity """
    def operate_factories(self):
        # 1 unit of production free
        self.__cache__['production'] = 1 + self._operate('factories') * self.player.tech_level.construction * 1234 # TODO Pam please come up with equasion
        return self.__cache__['production']

    """ Build an item """
    def build(self, item, from_queue=True):
        production = self.__cache__['production']
        item.cost.energy -= self.player.spend(item.__class__.__name__, item.cost.energy)
        for m in MINERAL_TYPES:
            use_p = min(production, item.cost[m], self.on_surface[m])
            production -= use_p
            self.on_surface[m] -= use_p
            item.cost[m] -= use_p
            if item.cost[m] > 0 and item.baryogenesis:
                spend_e = self.player.spend('baryogenesis', min(production / 2, item.cost[m]) * self.player.race.cost_of_baryogenesis)
                baryogenesis_minerals = spend_e / self.player.race.cost_of_baryogenesis
                production -= baryogenesis_minerals * 2
                item.cost[m] -= baryogenesis_minerals
        self.__cache__['production'] = production
        if item.cost.is_zero():
            item.finish()
            return true
        if not from_queue:
            self.player.build_queue.append(item)
        self.__cache__['production_blocked'] = True
        return False

    """ Add planetary facilities / capabilities """
    def build_planetary(self):
        minister = self.player.get_minister(self)
        keep_going = True
        while keep_going and not self.__cache__.get('production_blocked', False):
            # Terraforming
            worst_hab = None
            worst_hab_from_center = 0.0
            if minister.min_terraform_only:
                worst_hab_from_center = 1.0
            max_offset = min(40, self.player.tech_level.biotechnology)
            if not self.player.race.lrt_Bioengineer:
                max_offset = int(max_offset / 2)
            for hab in ['temperature', 'radiation', 'gravity']:
                hab_from_center = self._calc_range_from_center(self[hab], self.player.race['hab_' + hab], self.player.race['hab_' + hab + '_stop'], self[hab + '_terraform'])
                if hab_from_center > worst_hab_from_center and self[hab + '_terraform'] < max_offset:
                    worst_hab = hab
                    worst_hab_from_center = hab_from_center
            if worst_hab:
                keep_going = self.build(Terraform(hab=worst_hab, planet=self))
            else:
                # Build facility
                worst_facility = None
                worst_facility_percent = 1.0
                for facility in FACILITY_TYPES:
                    operate = self._operate(facility)
                    ideal = self._operate(facility, True)
                    if operate / ideal < worst_facility_percent:
                        worst_facility = facility
                        worst_facility_percent = operate / ideal
                if worst_facility:
                    keep_going = self.build(Facility(facility_type=worst_facility, planet=self, baryogenesis=minister.allow_baryogenesis))
                else:
                    keep_going = False

    """ Do baryogenesis """
    def baryogenesis(self):
        if self.player.get_minister(self).allow_baryogenesis:
            spend_e = self.player.spend('baryogenesis', self.__cache__['production'] * self.player.race.cost_of_baryogenesis)
            minerals = spend_e / self.player.race.cost_of_baryogenesis
            lowest = ''
            lowest_kt = sys.maxsize
            for m in MINERAL_TYPES:
                if self.on_surface[m] < lowest_kt:
                    lowest = m
                    lowest_kt = self.on_surface[m]
            self.on_surface[lowest] += minerals
            self.__cache__['production'] -= minerals

    """ build stuff in build queue """
    def do_construction(self, auto_build=False, allow_baryogenesis=False):
        minister = self.player.get_minister(self)
        zero_cost = Cost()
        while len(self.build_queue) > 0:
            item = self.build_queue[0]
            # energy
            item_type = 'planetary'
            if type(item) == type(Ship()):
                item_type = 'ship'
            e = self.player.energy_minister.spend_budget(item_type, item.cost_incomplete.energy)
            item.cost_incomplete.energy -= e
            # use on_surface minerals
            for mineral in ['titanium', 'lithium', 'silicon']:
                spend = min([self.production, getattr(item.cost_incomplete, mineral), getattr(self.on_surface, mineral)])
                self.production -= spend
                setattr(item.cost_incomplete, mineral, getattr(item.cost_incomplete, mineral) - spend)
                setattr(self.on_surface, mineral, getattr(self.on_surface, mineral) - spend)
            if item.cost_incomplete != zero_cost:
                # use baryogenesis to unblock the queue
                if self.production > 0 and minister.baryogenesis and allow_baryogenesis:
                    for mineral in ['titanium', 'lithium', 'silicon']:
                        max_baryogenesis = self.player.energy_minister.check_budget('baryogenesis') / self.player.race.cost_of_baryogenesis
                        spend = min([int(self.production / 2), getattr(item.cost_incomplete, mineral), max_baryogenesis])
                        self.production -= spend * 2
                        setattr(item.cost_incomplete, mineral, getattr(item.cost_incomplete, mineral) - spend)
                        self.player.energy_minister.spend_budget('baryogenesis', spend * self.player.race.cost_of_baryogenesis)
            if item.cost_incomplete == zero_cost:
                self.build_queue.pop(0)
                #TODO do something with the item
            if len(self.build_queue) == 0 and auto_build:
                self.build_queue.extend(self.auto_build())

    """ Perform scanning """
    def scan(self):
        if self.is_colonized():
            scanner = Scanner(normal = 250, penetrating = 2 * stars_math.TERAMETER_2_LIGHTYEAR) #TODO Pam please update the scanner normal range
            scanner.scan(self.player, self.location)

    """ Generate fuel if the planet has a space station """
    def generate_fuel(self):
        for station in self.space_station:
            pass #TODO

    """ Shift population via orbital mattrans """
    def mattrans(self):
        for station in self.space_station:
            pass #TODO


Planet.set_defaults(Planet, __defaults)
