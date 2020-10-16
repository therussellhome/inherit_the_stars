import sys
from random import randint
from random import uniform
from . import game_engine
from math import sin
from math import cos
from colorsys import hls_to_rgb
from .cargo import Cargo
from .cost import Cost
from .defaults import Defaults
from .minerals import Minerals
from .facility import Facility
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'distance': [50, 0, 100],
    'temperature': [50, -50, 150],
    'radiation': [50, -50, 150],
    'gravity': [50, -50, 150],
    'facilities': [{'Power': Facility(), 'Factory': Facility(), 'Mine': Facility(), 'Defense': Facility(), 'Scanner': Facility()}],
    'mineral_concentration': [Minerals(titanium=100.0, lithium=100.0, silicon=100.0)],
    'on_surface': [Cargo()],
    'player': [Reference()],
    'minister': [''],
    'planet_value': [0, -100, 100],
    'star_system': [Reference()],
}


""" Planets are colonizable by only one player, have minerals, etc """
class Planet(Defaults):
    
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Planet_' + str(id(self))
        if 'temperature' not in kwargs:
            if 'sun' in kwargs and 'distance' in kwargs:
                self.temperature = round(self.distance * 0.35 + self.sun.temperature * 0.65 + randint(-15, 15))
            else:
                self.temperature = randint(0, 100)
        if 'radiation' not in kwargs:
            self.radiation = randint(0, 100)
        if 'gravity' not in kwargs:
            self.gravity = min(100, abs(randint(0, 110) - randint(0, 110)))
        if 'mineral_concentration' not in kwargs:
            # TODO randomize concentrations
            modifier = self.gravity - 50
            self.mineral_concentration.titanium += modifier
            self.mineral_concentration.lithium += modifier
            self.mineral_concentration.silicon += modifier
        if 'orbit_speed' not in kwargs:
            self.orbit_speed = uniform(0.01, 1.0)
        if 'age' not in kwargs:
            self.age = randint(0, 3000)
        game_engine.register(self)

    """ Check if the planet is colonized """
    def is_colonized(self):
        return self.player.is_valid

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
    #TODO r = the distance from the sun
    # a = the planet's angle
    #TODO n = year 1/100
    def orbit(self):
        return #TODO orbit not finished
        if n < 1:
            n += 1
        else:
            n = 1 + self.age
        m = max(self.sun_gravity, 1)
        t = max(1, (((r ** 3)/m) ** .5) * (30/.85))
        a = n * (360/(100 * t)) 
        self.y = r * sin(a)
        self.x = r * cos(a)

    """ Colonize the planet """
    # player is a Reference to Player
    # because minister names can change, minister is a string
    def colonize(self, player, minister, population, create_facilities=True):
        self.player = player
        self.minister = minister
        self.on_surface.people = int(population)
        if create_facilities:
            self.facilities['Power'].colonize(self._get_facility_upgrade('Power'))
            self.facilities['Factory'].colonize(self._get_facility_upgrade('Factory'))
            self.facilities['Mine'].colonize(self._get_facility_upgrade('Mine'))
    
    """ Return the highest facility of the specified type """
    def _get_facility_upgrade(self, facility_type):
        #TODO this should reference player's tech tree
        return
        #best = Tech()
        for f in game_engine.get('Tech'):
            if f.category == 'Facility' and f.upgrade_path == facility_type and f.upgrade_level > best.upgrade_level and f.is_available(self.player):
                best = f
        return best
    
    """ Grow the current population """
    def have_babies(self):
        # all population calculations are done using people but stored using kT (1000/kT)
        if not self.player.is_valid:
            return
        pop = self.on_surface.people * 1000
        planet_value = self.calc_planet_value(self.player.race)
        rate = self.player.race.growth_rate / 100.0 * planet_value / 100.0
        maxpop = self.player.race.population_max
        pop = pop + (pop * rate) - (pop * pop / maxpop * rate)
        self.on_surface.people = int(round(pop, -3)/1000)
    
    """ Incoming! """
    def raise_shields(self):
        if self.player.is_valid:
            facility = self.facilities['Defense']
            workers = self.player.get_minister(self.name).defenses / 100 * self.on_surface.people * 1000
            colonists_to_operate_facility = self.player.race.colonists_to_operate_defense
            operate = min(facility.quantity, (workers / colonists_to_operate_facility))
            return operate * facility.tech.shields
    
    """ power plants make energy """
    def generate_energy(self):
        if self.player.is_valid:
            facility = self.facilities['Power']
            workers = self.player.get_minister(self.name).power_plants / 100 * self.on_surface.people * 1000
            colonists_to_operate_facility = self.player.race.colonists_to_operate_power_plant
            operate = min(facility.quantity, (workers / colonists_to_operate_facility))
            self.player.energy += operate * facility.tech.energy_output
    
    """ calculates max production capasity """
    def calc_production(self):
        if self.player.is_valid:
            facility = self.facilities['Factory']
            workers = self.player.get_minister(self.name).factories / 100 * self.on_surface.people * 1000
            colonists_to_operate_facility = self.player.race.colonists_to_operate_factory
            operate = min(facility.quantity, (workers / colonists_to_operate_facility))
            self.production = (operate + 1) * facility.tech.production_capacity
    
    """ mines mine the minerals """
    def _mine_minerals(self):
        if self.player.is_valid:
            allocation = self.player.get_minister(self.name).mines / 100
            minerals_per_mine = self.mine_tech.facility_output
            colonists_to_operate_mine = self.player.race.colonists_to_operate_mine
            operate = min([self.power_plants, allocation * self.effort / colonists_to_operate_mine])
            #TODO apply mineral concentration
            self.on_surface.titanium += round(operate * minerals_per_mine)
            self.on_surface.lithium += round(operate * minerals_per_mine)
            self.on_surface.silicon += round(operate * minerals_per_mine)
            #TODO reduce mineral concentration

    def get_availability(self, mineral):
        if mineral in ['titanium', 'silicon', 'lithium']:
            return (((getattr(self.remaining_minerals, mineral) / (((self.gravity * 6 / 100) + 1) * 1000)) ** 2) / 10) + 0.1
    
    """ minister checks to see if you need to build more facilities """
    def auto_build(self):
        if not self.player.is_valid:
            return
        minister = self.player.get_minister(self.name)
    #TODO    scanner_tech = self.player.max_tech('planetary_scanner')
    #TODO    penetrating_tech = self.player.max_tech('planetary_penetrating')
        num_facilities = (self.factories + self.power_plants + self.mines + self.defenses)
        if minister.build_penetrating_after_num_facilities <= num_facilities: # and self.penetrating_tech != penetrating_tech:
    #TODO        self.penetrating_tech = penetrating_tech
            return self.penetrating_tech
        elif minister.build_scanner_after_num_facilities <= num_facilities: # and self.scanner_tech != scanner_tech:
    #TODO        self.scanner_tech = scanner_tech
            return self.scanner_tech
        else:
            factory_percent = ((self.player.race.colonists_to_operate_factory * self.factories) / self.on_surface.people) - (minister.factories / 100)
            power_plant_percent = ((self.player.race.colonists_to_operate_power_plant * self.power_plants) / self.on_surface.people) - (minister.power_plants / 100)
            mine_percent = ((self.player.race.colonists_to_operate_mine * self.mines) / self.on_surface.people) - (minister.mines / 100)
            defense_percent = ((self.player.race.colonists_to_operate_defense * self.defenses) / self.on_surface.people) - (minister.defenses / 100)
            check = [[factory_percent, self.factory_tech], [power_plant_percent, self.power_plant_tech], [mine_percent, self.mine_tech], [defense_percent, self.defense_tech]]
            print(check)
            least = 1
            lest = 0
            for i in range(len(check)):
                if check[i][0] <= least:
                    least = check[i][0]
                    lest = i
            return check[lest][1]
    
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
                        self.player.energy_minister.spend_budget('baryogenesis', spend * self.player.race.cost_of_baryogenesis )
            if item.cost_incomplete == zero_cost:
                self.build_queue.pop(0)
                #TODO do something with the item
            if len(self.build_queue) == 0 and auto_build:
                self.build_queue.extend(self.auto_build())
        
        
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
    def calc_planet_value(self, race):
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

Planet.set_defaults(Planet, __defaults)
