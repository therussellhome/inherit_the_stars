import sys
from random import randint
from .cargo import Cargo
from .defaults import Defaults
from .minerals import Minerals
from .minister import Minister
from .facility import Facility
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'distance': [50, 0, 100],
    'temperature': [50, -15, 115],
    'radiation': [50, 0, 100],
    'gravity': [50, 0, 100],
    'power_plants': [0, 0, sys.maxsize],
    'factories': [0, 0, sys.maxsize],
    'mines': [0, 0, sys.maxsize],
    'power_plant_tech': [Facility()],
    'factory_tech': [Facility()],
    'mine_tech': [Facility()],
    'defense_tech': [Facility()],
    'is_tax_haven': [False],
    'mineral_concentration': [Minerals(titanium=100.0, lithium=100.0, silicon=100.0)],
    'on_surface': [Cargo()],
    'player': [Reference()],
    'minister': [''],
    'planet_value': [0, -100, 100],
    'star_system': [Reference()],
    'penetrating_tech': [Facility()],
    'scanner_tech': [Facility()]
}


""" Planets are colonizable by only one player, have minerals, etc """
class Planet(Defaults):
    
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Planet_' + str(id(self))
        if 'temperature' not in kwargs and 'sun' in kwargs and 'distance' in kwargs:
            self.temperature = round(self.distance * 0.35 + self.sun.temperature * 0.65 + randint(-15, 15))
        if 'sun' in kwargs:
            self.radiation = self.sun.radiation
        if 'gravity' not in kwargs:
            self.gravity = randint(0, 100)
        if 'mineral_concentration' not in kwargs:
            # TODO randomize concentrations
            modifier = self.gravity - 50
            self.mineral_concentration.titanium += modifier
            self.mineral_concentration.lithium += modifier
            self.mineral_concentration.silicon += modifier
    
    """ Colonize the planet """
    # player is a Reference to Player
    # because minister names can change, minister is a string
    def colonize(self, player, minister, population, factories):
        self.player = player
        self.minister = minister
        self.on_surface.people = int(population)
        self.factories += factories
        if self.power_plant_tech == Facility():
            self.power_plant_tech = self._get_facility_upgrade('Power')
        if self.factory_tech == Facility():
            self.factory_tech = self._get_facility_upgrade('Factory')
        if self.mine_tech == Facility():
            self.mine_tech = self._get_facility_upgrade('Mine')
        self.planet_value = self.calc_planet_value(self.player.race)
    
    """ Return the highest facility of the specified type """
    def _get_facility_upgrade(self, facility_type):
        best = Facility()
        for f in game_engine.get('Facility/'):
            if f.upgrade_path == facility_type and f.upgrade_level > best.upgrade_level and f.is_available(self.player):
                best = f
        return best
    
    """ Operate facilities """
    def generate_resources(self):
        self.effort = self._calc_effort()
        self._generate_energy()
        self._mine_minerals()
    
    """ Grow the current population """
    def have_babies(self):
        # all population calculations are done using people but stored using kT (1000/kT)
        if not self.player.is_valid:
            return
        pop = self.on_surface.people * 1000
        rate = self.player.race.growth_rate / 100.0
        maxpop = self.player.race.population_max
        maxpop *= self.planet_value / 100
        if pop < maxpop:
            p = pop/maxpop
            rate -= rate*(p**4)
            pop *= (rate + 1.0)
        elif pop > maxpop:
            pop *= (1.0 - rate)
            if pop < maxpop:
                pop = maxpop
        self.on_surface.people = int(round(pop, -3)/1000)
    
    """ Get the requested minister """
    def _get_minister(self):
        if self.player.is_valid:
            for minister in self.player.ministers:
                if minister.name == self.minister:
                    return minister
            minister = Minister(name=self.minister)
            self.player.ministers.append(minister)
            return minister
        return Minister(name=self.minister)
    
    """ power plants make energy """
    def _generate_energy(self):
        if self.player.is_valid:
            allocation = self._get_minister().power_plants / 100
            energy_per_plant = self.power_plant_tech.output_per_facility
            population_per_plant = self.power_plant_tech.population_per_facility
            operate = min([self.power_plants, allocation * (self.on_surface.people * 1000) / population_per_plant])
            self.player.energy += operate * energy_per_plant
    
    """ calculates max production capasity """
    def _calc_max_production_capacity(self):
        if self.player.is_valid:
            allocation = self._get_minister().factories / 100
            production_capacity_per_factory = self.factory_tech.output_per_facility
            effort_per_factory = self.factory_tech.effort_per_facility
            operate = min([self.power_plants, allocation * self.effort / effort_per_plant])
            max_production_capacity = operate * production_capacity_per_plant
            return max_production_capacity
    
    """ mines mine the minerals """
    def _mine_minerals(self):
        if self.player.is_valid:
            allocation = self._get_minister().mines / 100
            minerals_per_mine = self.mine_tech.output_per_facility
            population_per_mine = self.mine_tech.population_per_facility
            operate = min([self.power_plants, allocation * self.effort / population_per_plant])
            #TODO apply mineral concentration
            self.on_surface.titanium += round(operate * minerals_per_mine)
            self.on_surface.lithium += round(operate * minerals_per_mine)
            self.on_surface.silicon += round(operate * minerals_per_mine)
            #TODO reduce mineral concentration
    
    """ minister checks to see if you need to build more facilities """
    def auto_build(self):
        if not self.player.is_valid:
            return
        minister = self._get_minister()
    #TODO    scanner_tech = self.player.max_tech('planetary_scanner')
    #TODO    penetrating_tech = self.player.max_tech('planetary_penetrating')
        num_facilities = (self.factories + self.power_plants + self.mines + self.defenses)
        if minister.build_penetrating_after_num_facilitys <= num_facilities: # and self.penetrating_tech != penetrating_tech:
    #TODO        self.penetrating_tech = penetrating_tech
            return self.penetrating_tech
        elif minister.build_scanner_after_num_facilitys <= num_facilities: # and self.scanner_tech != scanner_tech:
    #TODO        self.scanner_tech = scanner_tech
            return self.scanner_tech
        else:
            factory_percent = ((self.factory_tech.population_per_facility * self.factories) / self.on_surface.people) - (minister.factories / 100)
            power_plant_percent = ((self.power_plant_tech.population_per_facility * self.power_plants) / tself.on_surface.people) - (minister.power_plants / 100)
            mine_percent = ((self.mine_tech.population_per_facility * self.mines) / self.on_surface.people) - (minister.mines / 100)
            defense_percent = ((self.defense_tech.population_per_facility * self.defenses) / self.on_surface.people) - (minister.defenses / 100)
            check = [[factory_percent, self.factory_tech], [power_plant_percent, self.power_plant_tech], [mine_percent, self.mine_tech], [defense_percent, self.defense_tech]]
            #print(check)
            least = 1
            lest = 0
            for i in range(len(check)):
                if check[i][0] <= least:
                    least = check[i][0]
                    lest = i
            return check[lest][1]
    
    """ build stuff in build queue """
    def do_construction(self, unblock):
        if not self.player.is_valid:
            return
        minister = self._get_minister()
        keep_going = True
        self.remaining_production = self._calc_max_production_capacity()
        while keep_going:
            item = self.build_queue[0]
            percent_t = math.ceil(item.cost.titanium /100)
            percent_l = math.ceil(item.cost.lithium /100)
            percent_s = math.ceil(item.cost.silicon /100)
            percent_e = math.ceil(item.cost.energy /100)
            while item.cost.titanium != item.cost_complete.titanium or item.cost.lithium != item.cost_complete.lithium or item.cost.silicon != item.cost_complete.silicon or item.cost.energy != item.cost_complete.energy:
                spend_t = min([percent_t, item.cost.titanium - item.cost_complete.titanium])
                spend_l = min([percent_l, item.cost.lithium - item.cost_complete.lithium])
                spend_s = min([percent_s, item.cost.silicon - item.cost_complete.silicon])
                o_spend_e = min([percent_e, item.cost.energy - item.cost_complete.energy])
                if type(item) == type(Facility()):
                    item_type = 'planetary'
                else:
                    item_type = 'ship'
                spend_e = self.player.energy_minister.check_budget(item_type, o_spend_e)
                if spend_t <= self.minerals.titanium and spend_l <= self.minerals.lithium and spend_s <= self.minerals.silicon and spend_e == o_spend_e and (spend_t + spend_l + spend_s) <= self.remaining_production:
                    self.minerals.titanium -= spend_t
                    self.minerals.lithium -= spend_l
                    self.minerals.silicon -= spend_s
                    self.player.energy_minister.spend_budget(item_type, spend_e)
                    item.cost_complete.titanium += spend_t
                    item.cost_complete.lithium += spend_l
                    item.cost_complete.silicon += spend_s
                    item.cost_complete.energy += spend_e
                    self.remaining_production -= spend_t + spend_l + spend_s
                else:
                    b_spend_e = self.player.energy_minister.check_budget('baryogenesis', 100)
                    if self.remaining_production >= (10 + spend_t + spend_l + spend_s) and spend_e == o_spend_e and b_spend_e == 100 and minister.unblock:
                        if spend_t  > 0 or spend_l > 0 or spend_s > 0:
                            self.remaining_production - 10
                            self.minerals.titanium += 1
                            self.minerals.lithium += 1
                            self.minerals.silicon += 1
                            self.player.energy_minister.spend_budget('baryogenesis', b_spend_e)
                    else:
                        keep_going = False
            if len(build_queue) == 0:
                build_queue.push(self.auto_build())
        
        
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
        g = self._calc_range_from_center(self.gravity, race.gravity_start, race.gravity_stop)
        t = self._calc_range_from_center(self.temperature, race.temperature_start, race.temperature_stop)
        r = self._calc_range_from_center(self.radiation, race.radiation_start, race.radiation_stop)
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