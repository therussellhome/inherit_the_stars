import sys
from random import randint
from random import uniform
from . import game_engine
from . import stars_math
from math import sin
from math import cos
from random import randint
from random import uniform
from colorsys import hls_to_rgb
from . import game_engine
from .cost import Cost
from .cargo import Cargo
from .defaults import Defaults
from .location import Location
from .minerals import Minerals
from .facility import Facility
from .location import Location
from .reference import Reference
from .tech import Tech


""" Default values (default, min, max)  """
__defaults = {
    'location': [Location()],
    'distance': [50, 0, 100],
    'temperature': [50, -50, 150],
    'radiation': [50, -50, 150],
    'gravity': [50, -50, 150],
    'remaining_minerals': [Minerals()],
    'on_surface': [Cargo()],
    'player': [Reference('Player')],
    'minister': [''],
    'location': [Location()],
    'star_system': [Reference('StarSystem')],
    'factory_capacity': [0, 0, sys.maxsize],
    'build_queue': [[]], # array of tuples (cost_incomplete, buildable)
    # facilities where the key matches the tech category
    'Power Plant': [Facility()],
    'Factory': [Facility()],
    'Mineral Extractor': [Facility()],
    'Planetary Shield': [Facility()],
}


""" Planets are colonizable by only one player, have minerals, etc """
class Planet(Defaults):

    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Planet_' + str(id(self))
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
        return self.player.is_valid

    """ Colonize the planet """
    # player is a Player object (reference created internally)
    # because minister names can change, minister is a string
    def colonize(self, player, minister):
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
        self.minister = minister
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
    def habitability(self, race):
        g = self._calc_range_from_center(self.gravity, race.hab_gravity, race.hab_gravity_stop)
        t = self._calc_range_from_center(self.temperature, race.hab_temperature, race.hab_temperature_stop)
        r = self._calc_range_from_center(self.radiation, race.hab_radiation, race.hab_radiation_stop)
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
    def _calc_range_from_center(self, planet, race_start, race_stop):
        race_radius = float(race_stop - race_start) / 2.0
        if race_radius == 0 and planet == race_start:
            return 0.0
        elif race_radius == 0:
            return 2.0
        else:
            return min([2.0, abs((race_start + race_radius) - planet) / abs(race_radius)])

    """ Calculate growth rate """
    def growth_rate(self, race):
        return race.growth_rate * self.habitability(race) / 100.0

    """ Calculate planet's max population """
    def maxpop(self, race):
        return int(200000000.0 / race.body_mass * (6.0 * self.gravity / 100.0 + 1.0))

    """ Grow the current population """
    def have_babies(self):
        # all population calculations are done using people but stored using kT (1000/kT)
        pop = self.on_surface.people * self.player.race.pop_per_kt()
        # adjust rate for planet habitability and turn hundreth
        rate = self.growth_rate(self.player.race) / 100.0 / 100.0
        # adjust maxpop for size of the world
        pop = pop + (pop * rate) - (pop * pop / self.maxpop(self.player.race) * rate)
        # population is in whole people but stored in kT
        self.on_surface.people = round(pop) / self.player.race.pop_per_kt()
        return self.on_surface.people

    """ how many facilities can be operated """
    # avoid creating facilities
    def __operate(self, facility_type, race_trait):
        allocation = getattr(self.player.get_minister(self.name), facility_type)
        workers = allocation / 100 * self.on_surface.people * self.player.race.pop_per_kt()
        return min(getattr(self, facility_type).quantity, getattr(self.player.race,race_trait) * workers / 10000)

    """ Incoming! """
    def raise_shields(self):
        return self.__operate('Planetary Shield', 'defenses_per_10k_colonists') * getattr(self, 'Planetary Shield').tech.shield

    """ power plants make energy """
    def generate_energy(self):
        plants = self.__operate('Power Plant', 'power_plants_per_10k_colonists') * getattr(self, 'Power Plant').tech.facility_output / 100
        print(plants)
        pop = self.on_surface.people * self.player.race.pop_per_kt() * self.player.race.energy_per_10k_colonists / 10000 / 100
        print(self.player.race.energy_per_10k_colonists)
        return plants + pop

    """ mines mine the minerals """
    def mine_minerals(self):
        factor = getattr(self, 'Mineral Extractor').tech.mineral_depletion_factor
        operate = self.__operate('Mineral Extractor', 'mines_per_10k_colonists')
        print(operate)
        for mineral in ['silicon', 'titanium', 'lithium']:
            availability = self.mineral_availability(mineral)
            setattr(self.on_surface, mineral, getattr(self.on_surface, mineral) + round(operate * availability))
            setattr(self.remaining_minerals, mineral, getattr(self.remaining_minerals, mineral) - round(operate * availability * factor))

    """ Availability of the mineral type """
    def mineral_availability(self, mineral):
        return (((getattr(self.remaining_minerals, mineral, 0) / (((self.gravity * 6 / 100) + 1) * 1000)) ** 2) / 10) + 0.1

    """ calculates max production capasity """
    def calc_production(self):
        # 1 unit of production free
        self.factory_capacity = 1 + self.__operate('Factory', 'factories_per_10k_colonists') * getattr(self, 'Factory').tech.facility_output / 100

    """ minister checks to see if you need to build more facilities """
    def auto_build(self):
        if not self.player.is_valid:
            return
        #facility = self.auto_upgrade()
        #if facility != None:
        #    return facility
        minister = self.player.get_minister(self.name)
    #TODO    scanner_tech = self.player.max_tech('planetary_scanner')
    #TODO    penetrating_tech = self.player.max_tech('planetary_penetrating')
        num_facilities = (self.factories + self.power_plants + self.mines + self.defenses)
        if minister.build_penetrating_after_num_facilities <= num_facilities: # and self.penetrating_tech != penetrating_tech:
            self.penetrating_tech = 'penetrating_tech'
            return self.penetrating_tech
        elif minister.build_scanner_after_num_facilities <= num_facilities: # and self.scanner_tech != scanner_tech:
            self.scanner_tech = 'scanner_tech'
            return self.scanner_tech
        else:
            factory_percent = ((self.player.race.colonists_to_operate_factory * getattr(self, 'Factory').quantity) / self.on_surface.people) - (minister.factories / 100)
            power_plant_percent = ((self.player.race.colonists_to_operate_power_plant * getattr(self, 'Power Plant').quantity) / self.on_surface.people) - (minister.power_plants / 100)
            mine_percent = ((self.player.race.colonists_to_operate_mine * getattr(self, 'Mineral Extractor').quantity) / self.on_surface.people) - (minister.mines / 100)
            defense_percent = ((self.player.race.colonists_to_operate_defense * getattr(self, 'Planetary Shields').quantity) / self.on_surface.people) - (minister.defenses / 100)
            check = [[factory_percent, 'Factory'], [power_plant_percent, 'Power'], [mine_percent, 'Mine'], [defense_percent, 'Defense']]
            #print(check)
            least = 1
            lest = 0
            for i in range(len(check)):
                if check[i][0] <= least:
                    least = check[i][0]
                    lest = i
            self.facilities[check[lest][1]].build_prep()
            return self.facilities[check[lest][1]]#Reference()#?

    """ checks for upgrades """
    """
    def auto_upgrade(self):
        if not self.player.is_valid:
            return None
        for facility in self.facilities:
            upgrade = facility.upgrade_available(self.player)
            if upgrade:
                facility.cost_incomeplete = facility.upgrade_cost(self.player, upgrade)
                return facility
        return None
    #"""

    """ build stuff in build queue """
    def do_construction(self, auto_build=False, allow_baryogenesis=False):
        if not self.player.is_valid:
            return
        minister = self.player.get_minister(self.name)
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



Planet.set_defaults(Planet, __defaults)
