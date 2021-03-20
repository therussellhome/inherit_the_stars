import sys
from colorsys import hls_to_rgb
from math import cos, sin
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

    """ Get the planet's color """
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
        if self.player.race.primary_race_trait == 'Gaerhule':
            return self._operate('defenses') * max(480, 240 * self.player.tech_level.energy)
        elif self.player.race.primary_race_trait != 'Aku\'Ultan':
            return self._operate('defenses') * max(200, 200 * self.player.tech_level.energy)
        return 0

    """ power plants make energy 1/100th """
    def generate_energy(self):
        facility_yj =  self._operate('power_plants') * (1 + .05 * self.player.tech_level.propulsion)
        pop_yj = self.on_surface.people * self.player.race.pop_per_kt() * self.player.race.energy_per_10k_colonists / 10000 / 100
        self.player.energy += facility_yj + pop_yj
        return facility_yj + pop_yj

    """ mines mine the minerals per 100th """
    def mine_minerals(self):
        factor = 1 + 0.3 * 0.5 ** (self.player.tech_level.weapons / 7)
        operate = self._operate('mines')
        availability = self.mineral_availability()
        for mineral in MINERAL_TYPES:
            self.on_surface[mineral] += operate * availability[mineral] / 100
            self.remaining_minerals[mineral] -= operate * availability[mineral] * factor / 100

    """ Availability of the mineral type """
    def mineral_availability(self):
        avail = Minerals()
        for m in MINERAL_TYPES:
            avail[m] = (((self.remaining_minerals[m] / (((self.gravity * 6 / 100) + 1) * 1000)) ** 2) / 10) + 0.1
        return avail

    """ calculates max production capacity per 100th """
    def operate_factories(self):
        # 1 unit of production free
        self.__cache__['production'] = 1 + self._operate('factories') * (5 + self.player.tech_level.construction / 2) / 100
        return self.__cache__['production']
    
    """ get the time needed to get all the materials for a production queue item. """
    def time_til_done(self, queue, i):
        ti = 0
        li = 0
        si = 0
        yj = 0
        pro = 0
        # get what is needed
        for j in range(len(queue)):
            item = queue[j]
            yj += item.cost.energy
            if item.planet == self:
                ti += item.cost.titanium
                li += item.cost.lithium
                si += item.cost.silicon
            if j == i:
                break
        pro = ti + li + si
        # calculate the time needed to get what is needed
        try:
            t_ti = ceil(max((ti - self.on_surface.titanium) / (self.mineral_availability('titanium') * self._operate('mines')), 1))/100
        except ZeroDivisionError:
            if ti - self.on_surface.titanium >= 0:
                t_ti = 0.01
            else:
                t_ti = 'never'
        try:
            t_li = ceil(max((li - self.on_surface.lithium) / (self.mineral_availability('lithium') * self._operate('mines')), 1))/100
        except ZeroDivisionError:
            if li - self.on_surface.lithium >= 0:
                t_li = 0.01
            else:
                t_li = 'never'
        try:
            t_si = ceil(max((si - self.on_surface.silicon) / (self.mineral_availability('silicon') * self._operate('mines')), 1))/100
        except ZeroDivisionError:
            if si - self.on_surface.silicon >= 0:
                t_si = 0.01
            else:
                t_si = 'never'
        try:
            t_yj = ceil(max((yj - (self.player.energy * self.player.finance_construction_percent / 100)) / (self.player.predict_budget() * self.player.finance_construction_percent / 100), 1))/100
        except ZeroDivisionError:
            if yj - (self.player.energy * self.player.finance_construction_percent / 100) >= 0:
                t_yj = 0.01
            else:
                t_yj = 'never'
        try:
            t_pro = ceil(max(pro / (1 + self._operate('factories') * (5 + self.player.tech_level.construction / 2)), 1))/100
        except ZeroDivisionError:
            t_pro = 'never'
        return (t_ti, t_li, t_si, t_yj, t_pro, pro)
    
    def time_til_html(self, cost_in_html, queue, i):
        html1 = ''
        html2 = ''
        time = self.time_til_done(queue, i)
        cost = cost_in_html.split('</i>')
        for c in cost:
            if 'Titanium' in c:
                html1 += '<td>' + c + '</i></td>'
                if time[0] == 'never':
                    html2 += '<td>never</td>'
                else:
                    html2 += '<td>' + str(time[0]) + ' years</td>'
            elif 'Lithium' in c:
                html1 += '<td>' + c + '</i></td>'
                if time[1] == 'never':
                    html2 += '<td>never</td>'
                else:
                    html2 += '<td>' + str(time[1]) + ' years</td>'
            elif 'Silicon' in c:
                html1 += '<td>' + c + '</i></td>'
                if time[2] == 'never':
                    html2 += '<td>never</td>'
                else:
                    html2 += '<td>' + str(time[2]) + ' years</td>'
            elif 'Energy' in c:
                html1 += '<td>' + c + '</i></td>'
                if time[3] == 'never':
                    html2 += '<td>never</td>'
                else:
                    html2 += '<td>' + str(time[3]) + ' years</td>'
        html1 += '<td>' + str(queue[i].cost.titanium + queue[i].cost.lithium + queue[i].cost.silicon) + '</i></td>'
        if time[4] == 'never':
            html2 += '<td>never</td>'
        else:
            html2 += '<td>' + str(time[4]) + ' years</td>'
        return (html1, html2)
    
    """ Build an item """
    def build(self, item, from_queue=True):
        production = self.__cache__['production']
        spend = Cost()
        in_progress = item.build()
        while not in_progress.is_zero():
            spend = Cost()
            spend.energy -= self.player.spend(item.__class__.__name__, in_progress.energy)
            for m in MINERAL_TYPES:
                use_p = min(production, in_progress[m], self.on_surface[m])
                production -= use_p
                self.on_surface[m] -= use_p
                spend[m] -= use_p
                if spend[m] < in_progress[m] and item.baryogenesis:
                    spend_e = self.player.spend('baryogenesis', min(production / 2, in_progress[m] - spend[m]) * self.player.race.cost_of_baryogenesis)
                    baryogenesis_minerals = spend_e / self.player.race.cost_of_baryogenesis
                    production -= baryogenesis_minerals * 2
                    spend[m] -= baryogenesis_minerals
            # Apply build effort
            in_progress = item.build(spend)
            # Blocked
            if spend.is_zero():
                if not from_queue:
                    self.player.build_queue.append(item)
                self.__cache__['production'] = production
                self.__cache__['production_blocked'] = True
                return False
        self.__cache__['production'] = production
        return True

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

    """ Perform penetrating scanning """
    def scan_penetrating(self):
        if self.is_colonized():
            scan.penetrating(self.player, self.location, 250) #TODO Pam please update the scanner range

    """ Perform normal scanning """
    def scan_normal(self):
        if self.is_colonized():
            scan.normal(self.player, self.location, 100) #TODO Pam please update the scanner range

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


Planet.set_defaults(Planet, __defaults)
