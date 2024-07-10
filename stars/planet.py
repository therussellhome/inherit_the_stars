import sys
from colorsys import hls_to_rgb
from math import cos, sin, sqrt, pi
from random import randint, uniform
from . import game_engine
from . import scan
from . import stars_math
from .fleet import Fleet
from .cargo import Cargo
from .cost import Cost
from .defaults import Defaults
from .facility import Facility, FACILITY_TYPES
from .location import Location
from .location import Location
from .minerals import Minerals, MINERAL_TYPES
from .reference import Reference
from .tech import Tech
from .terraform import Terraform
from math import ceil


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
    # facilities where the key matches from the facility class
    'power_plants': (0, 0, sys.maxsize),
    'factories': (0, 0, sys.maxsize),
    'mineral_extractors': (0, 0, sys.maxsize),
    'defenses': (0, 0, sys.maxsize),
}


""" Temporary values (default, min, max)  """
__tmp_defaults = {
    'shields': 0,
    'impact_shields': 0.0,
    'impact_people': 0.0,
    'production': 0.0,
    'production_blocked': False,
}


""" Planets are colonizable by only one player, have minerals, etc """
class Planet(Defaults):
    """ Initialize defaults """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'temperature' not in kwargs:
            self.temperature = randint(0, 100)
            if 'star_system' in kwargs:
                sun = self.star_system.sun()
                if sun is not None:
                    self.temperature = round(self.distance * 0.35 + sun.temperature * 0.65 + randint(-15, 15))
        if 'radiation' not in kwargs:
            self.radiation = randint(0, 100)
            if 'star_system' in kwargs:
                sun = self.star_system.sun()
                if sun is not None:
                    self.radiation = sun.radiation
        if 'gravity' not in kwargs:
            self.gravity = min(100, abs(randint(0, 110) - randint(0, 110)))
        if 'remaining_minerals' not in kwargs:
            if self.homeworld:
                self.init_minerals(49)
            else:
                self.init_minerals(1)
        if 'location' not in kwargs:
            distance_ly = self.distance / 100 * stars_math.TERAMETER_2_LIGHTYEAR
            self.location = Location(reference=self.star_system, offset=distance_ly, lat=0)
        if 'orbit_speed' not in kwargs:
            self.orbit_speed = uniform(0.01, 1.0)
        if 'age' not in kwargs:
            self.age = randint(0, 3000)
        game_engine.register(self)

    """ Create remaining minerals with a minimum value 1-99 """
    def init_minerals(self, minimum):
        minimum = max(1, min(99, minimum))
        for mineral in MINERAL_TYPES:
            self.remaining_minerals[mineral] = (randint(minimum, 99) ** 0.5) * (((self.gravity * 6 / 100) + 1) * 1000)


    """ Get the planet's color """
    # return it in a hexdecimal string so the webpage can use it
    def get_color(self):
        t = (min(100, max(0, self.temperature)) / 100) * .75
        r = .5 + (min(100, max(0, self.radiation)) * .005)
        color = hls_to_rgb(t, .5, r)
        color_string = '#' + format(round(color[0] * 255), '02X') + format(round(color[1] * 255), '02X') + format(round(color[2] * 255), '02X')
        return color_string
    
    """ Planets orbit their star """
    def orbit(self):
        self.location.orbit()

    """ Check whether the planet is colonized """
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
    negative planet value is calculated using the same equation
    with g, t, and r = 0 if < 1 | g, t, r = value - 1
    and 100 subtracted from the result
    """
    def habitability(self, race, terraform=(0, 0, 0)):
        if self.__class__.__name__ != 'Sun' and race.primary_race_trait == 'Pa\'anuri':
            return -100
        elif self.__class__.__name__ == 'Sun' and race.primary_race_trait != 'Pa\'anuri':
            return -100
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

    """ Calculate the distance from the center of the habitable range to the planet's attribute
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
    def _operate(self, facility_type, ideal=False):
        allocation = self.player.get_minister(self)[facility_type]
        workers = allocation / 100 * self.on_surface.people * self.player.race.pop_per_kt()
        operate = self.player.race[facility_type + '_per_10k_colonists'] * workers / 10000
        if ideal:
            return operate
        return min(self[facility_type], operate)

    """ Incoming! """
    def raise_shields(self):
        self.shields = 0
        if self.player.race.primary_race_trait == 'Gaerhule':
            self.shields = self._operate('defenses') * max(480, 240 * self.player.tech_level.energy)
        elif self.player.race.primary_race_trait != 'Aku\'Ultan':
            self.shields = self._operate('defenses') * max(200, 200 * self.player.tech_level.energy)
        return self.shields

    """ Calculate bombing """
    def bomb(self, bomb):
        defense = bomb.percent_defense(self.on_surface.people, self.shields)
        if defense < randint(0, 100):
            self.impact_shields += bomb.shield_kill / 100
            self.impact_people += max(bomb.minimum_pop_kill / 100, bomb.percent_pop_kill / 100 * self.on_surface.people)

    """ Apply bombing """
    def bomb_impact(self):
        self.defenses -= self.impact_shields
        self.on_surface.people -= self.impact_people
        self.impact_shields = 0
        self.impact_people = 0
        if self.on_surface.people == 0:
            pass #TODO

    """ Catch packets """
    def catch_packet(self, packet):
        if self.on_surface_people > 0:
            ke_catcher = 0
            self.raise_shields()
            if self.starbase:
                ke_catcher = self.starbase.catcher()
            defence_factor = 1 - max(0, (packet.ke - ke_catcher) / packet.ke)
            self.on_surface += packet.minerals * defence_factor 
            packet.minerals *= (1 - defence_factor)
            if defence_factor < 1:
                kt_damage_shields = packet.ke * (1 - defence_factor) / round(packet.mass)
                kt_damage_pop = 50 * packet.ke * (1 - defence_factor) / round(packet.mass)
                defence = 75.0 - 500.0 / (self.shields / self.on_surface.people + (500.0 / 75.0))
                cnt = 0
                for kt in range(round(packet.mass)):
                    if defence < randint(0, 100):
                        cnt += 1
                self.on_surface += packet.minerals * 0.1 * (cnt / round(packet.mass))
                self.remaining_minerals += packet.minerals * 0.9 * (cnt / round(packet.mass))
                self.impact_shields += cnt * kt_damage_shields
                self.impact_people += cnt * kt_damage_pop
            self.bomb_impact()

    """ power plants make energy per 1/100th """
    def generate_energy(self):
        facility_yj =  round(self._operate('power_plants') * (1 + .05 * self.player.tech_level.propulsion))
        pop_yj = self.on_surface.people * self.player.race.pop_per_kt() * self.player.race.energy_per_10k_colonists / 10000 / 100
        self.player.add_energy(facility_yj + pop_yj)
        return facility_yj + pop_yj

    """ mineral extractors extract the minerals per 100th """
    def extract_minerals(self, component=None, qty=0, max_extraction=sys.maxsize, forecast=False):
        if component:
            operate = component.extraction_rate * qty
            factor = component.mineral_depletion_factor
        else:
            operate = self._operate('mineral_extractors')
            factor = 1 + 0.3 * 0.5 ** (self.player.tech_level.weapons / 7)
        availability = self.mineral_availability()
        extracted = Minerals()
        for mineral in MINERAL_TYPES:
            extract = min(max_extraction, operate * availability[mineral] / 100)
            max_extraction -= extract
            extracted[mineral] = extract
            if not forecast:
                self.remaining_minerals[mineral] -= extract * factor
        if not component and not forecast:
            self.on_surface += extracted
        return extracted

    """ Availability of the mineral type """
    def mineral_availability(self):
        avail = Minerals()
        for m in MINERAL_TYPES:
            avail[m] = (((self.remaining_minerals[m] / (((self.gravity * 6 / 100) + 1) * 1000)) ** 2) / 10) + 0.1
        return avail

    """ calculates max production capacity per 100th """
    def operate_factories(self, forecast=False):
        # 1 unit of production free
        production = 0.01 + self._operate('factories') * (5 + self.player.tech_level.construction / 2) / 100
        if not forecast:
            self.production = production
        return production
    
    def time_til_html(self, total_cost, item_cost):
        html = ''
        extract = self.extract_minerals(forecast=True)
        html += '<td>' + item_cost.to_html() + str(ceil(item_cost.titanium + item_cost.lithium + item_cost.silicon)) + 'P</td>'
        time = 0
        contraining_factor = ''
        for mineral in MINERAL_TYPES:
            t = (total_cost[mineral] - self.on_surface[mineral]) / (extract[mineral] + 0.000000001) / 100
            if t > time:
                time = t
                constraining_factor = mineral
        t = (total_cost['energy'] - self.player.energy * self.player.finance_construction_percent/100) / (self.player.predict_income('construction') + 0.000000001) / 100
        if t > time:
            time = t
            constraining_factor = 'energy'
        pro = total_cost.titanium + total_cost.lithium + total_cost.silicon
        t = pro / self.operate_factories(forecast=True) / 100
        if t > time:
            time = t
            constraining_factor = 'production'
        html += '<td>' + str(ceil(time)) + 'years</td><td>' + constraining_factor + '</td>'
        return html
    
    """ Build an item """
    def build(self, item, from_queue=True):
        self.production_blocked = False
        in_progress = item.build()
        while not in_progress.is_zero():
            spend = Cost()
            spend.energy = self.player.spend(item.__class__.__name__, in_progress.energy)
            for m in MINERAL_TYPES:
                use_p = min(self.production, in_progress[m], self.on_surface[m])
                self.production -= use_p
                self.on_surface[m] -= use_p
                spend[m] = use_p
            for m in MINERAL_TYPES:
                if spend[m] < in_progress[m] and item.baryogenesis:
                    spend_e = self.player.spend('Baryogenesis', min(self.production / 2, in_progress[m] - spend[m]) * self.player.race.cost_of_baryogenesis)
                    baryogenesis_minerals = spend_e / self.player.race.cost_of_baryogenesis
                    self.production -= baryogenesis_minerals * 2
                    spend[m] += baryogenesis_minerals
            # Apply build effort
            in_progress = item.build(spend)
            # Blocked
            if spend.is_zero():
                if not from_queue:
                    self.player.build_queue.append(item)
                self.production_blocked = True
                return False
        return True

    """ Add planetary facilities / capabilities """
    def build_planetary(self):
        minister = self.player.get_minister(self)
        keep_going = True
        while keep_going and not self.production_blocked:
            # Terraforming
            worst_hab = None
            worst_hab_from_center = 0.0
            if minister.min_terraform_only:
                worst_hab_from_center = 1.0
            max_offset = self.player.max_terraform()
            for hab in ['temperature', 'radiation', 'gravity']:
                hab_from_center = self._calc_range_from_center(self[hab], self.player.race['hab_' + hab], self.player.race['hab_' + hab + '_stop'], self[hab + '_terraform'])
                if hab_from_center > worst_hab_from_center and self[hab + '_terraform'] < max_offset:
                    worst_hab = hab
                    worst_hab_from_center = hab_from_center
            if worst_hab:
                keep_going = self.build(Terraform(hab=worst_hab, planet=Reference(self)))
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
                    keep_going = self.build(Facility(facility_type=worst_facility, planet=Reference(self), baryogenesis=minister.allow_baryogenesis))
                else:
                    keep_going = False

    """ Do baryogenesis """
    def baryogenesis(self):
        if self.player.get_minister(self).allow_baryogenesis:
            spend_e = self.player.spend('Baryogenesis', self.production * self.player.race.cost_of_baryogenesis)
            minerals = spend_e / self.player.race.cost_of_baryogenesis
            lowest = ''
            lowest_kt = sys.maxsize
            for m in MINERAL_TYPES:
                if self.on_surface[m] < lowest_kt:
                    lowest = m
                    lowest_kt = self.on_surface[m]
            self.on_surface[lowest] += minerals
            self.production -= minerals

    """ Perform penetrating scanning """
    def scan_penetrating(self):
        if self.is_colonized():
            # Formula is loosely based on the volume to radius equasion
            radius = (self.player.race.pop_per_kt() * self.on_surface.people * 3.0 / 4.0 / pi * (self.player.tech_level.electronics + 1.0) / 3000.0) ** (1.0 / 3.0)
            if self.player.race.lrt_2ndSight:
                radius *= 2.5
            scan.penetrating(self.player, self.location, radius)

    """ Perform normal scanning """
    def scan_normal(self):
        if self.is_colonized():
            # Formula is loosely based on the volume to radius equasion
            radius = (self.player.race.pop_per_kt() * self.on_surface.people * 3.0 / 4.0 / pi * (self.player.tech_level.electronics + 1.0) / 3000.0) ** (1.0 / 3.0) * 10.0
            if self.player.race.lrt_2ndSight:
                radius /= 2.0
            scan.normal(self.player, self.location, radius)

    """ Create a report about itself """
    def scan_self(self):
        if self.is_colonized():
            self.player.add_intel(self, self.scan_report('self'))

    """ Return intel report when scanned """
    def scan_report(self, scan_type=''):
        report = {
            'location': self.location,
            'color': self.get_color(),
            'gravity': self.gravity,
            'temperature': self.temperature,
            'radiation': self.radiation,
            'Lithium Availability': self.mineral_availability().lithium,
            'Silicon Availability': self.mineral_availability().silicon,
            'Titanium Availability': self.mineral_availability().titanium,
        }
        if self.is_colonized():
            report['Player'] = self.player
            report['Population'] = self.on_surface.people
        return report

    """ Shift population via orbital mattrans """
    def mattrans(self):
        pass #TODO get stations in orbit, check for mattrans


Planet.set_defaults(Planet, __defaults, __tmp_defaults)
