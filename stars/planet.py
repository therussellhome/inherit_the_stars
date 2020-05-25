import sys
from random import randint
from .cargo import Cargo
from .defaults import Defaults
from .minerals import Minerals
from .minister import Minister
from .facility import Facility
from .reference import Reference

""" List of gravity values for display (0..100) """
_grav_values = [0.20, 0.22, 0.23, 0.24, 0.26, 0.28, 0.29, 0.30, 0.32, 0.34, 0.35, 0.36, 0.38, 0.40, 0.41, 0.42, 0.44, 0.46, 0.47, 0.48, 0.50, 0.52, 0.53, 0.54, 0.56, 0.57, 0.59, 0.60, 0.62, 0.64, 0.65, 0.67, 0.68, 0.70, 0.71, 0.73, 0.74, 0.75, 0.77, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.00, 1.04, 1.08, 1.12, 1.16, 1.20, 1.24, 1.28, 1.32, 1.36, 1.40, 1.44, 1.48, 1.52, 1.56, 1.60, 1.64, 1.68, 1.72, 1.76, 1.80, 1.84, 1.88, 1.92, 1.96, 2.00, 2.11, 2.22, 2.33, 2.44, 2.55, 2.66, 2.77, 2.88, 3.00, 3.12, 3.24, 3.36, 3.48, 3.60, 3.72, 3.84, 3.96, 4.09, 4.22, 4.35, 4.48, 4.61, 4.74, 4.87, 5.00]

""" Default values (default, min, max)  """
__defaults = {
    'distance': [50, 0, 100],
    'temperature': [50, -15, 115],
    'radiation': [50, 0, 100],
    'gravity': [50, 0, 100],
    'effort': [0, 0, sys.maxsize],
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

""" TODO """
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
            modifier = self.gravity - 50
            self.mineral_concentration.titanium += modifier
            self.mineral_concentration.lithium += modifier
            self.mineral_concentration.silicon += modifier

    """ Return the planet temperature (-260C to 260C) """
    def display_temp(self):
        return str(self.temperature * 4 - 200) + 'C'

    """ Return the planet gravity (0.20g to 5.00g) """
    def display_grav(self):
        return str(_grav_values[self.gravity]) + 'g'
    
    """ Colonize the planet """
    """ where player is a Reference to "Player/<player_name>" """
    def colonize(self, population, player, minister='default', fact=1, mine=1, power=1):
        self.on_surface.people = int(population)
        self.player = player
        self.factories += fact
        self.mines += mine
        self.power_plants += power
        #TODO self.power_plant_tech = self.player.max_tech('Power')
        #TODO self.factory_tech = self.player.max_tech('Factory')
        #TODO self.mine_tech = self.player.max_tech('Mine')

    """ runs the turn """
    def take_turn(self):
        self.remaining_production = _calc_max_production_capacity()
        self._grow_population()
        self._calculate_effort()
        self._generate_energy()
        self._mine_minerals()
        self._auto_build()
        self._donate_surplus()
        
    
    def _do_bariogenisis():
        pass
    
    """ Grow the current population """
    def _grow_population(self):
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
        #print(pop)
        self.on_surface.people = int(round(pop, -3)/1000)

    """ calculate how much effort is produced by the population """
    def _calculate_effort(self):
        if self.player.is_valid:
            self.effort = round(self.on_surface.people * 1000 * self.player.race.effort_efficency)
    
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
            energy_per_plant = self.power_plant_tech['output_per_facility']
            effort_per_plant = self.power_plant_tech['effort_per_facility']
            operate = min([self.power_plants, allocation * self.effort / effort_per_plant])
            self.effort -= operate * effort_per_plant
            self.player.energy += operate * energy_per_plant
    
    """ calculates max production capasity """
    def _calc_max_production_capacity(self):
        if self.player.is_valid:
            allocation = self._get_minister().factories / 100
            production_capacity_per_factory = self.factory_tech.output_per_facility
            effort_per_factory = self.factory_tech.effort_per_facility
            operate = min([self.power_plants, allocation * self.effort / effort_per_plant])
            effort = operate * effort_per_plant
            max_production_capacity = operate * production_capacity_per_plant
            return max_production_capacity
        
    """ calculates effort cost of spending production capasity  """
    def _spend_production_capacity(self, used=1):
        if self.player.is_valid:
            allocation = self._get_minister().factories / 100 * used
            effort_per_factory = self.factory_tech.effort_per_facility
            operate = min([self.power_plants, allocation * self.effort / effort_per_plant])
            self.effort -= operate * effort_per_plant
    
    """ mines mine the minerals """
    def _mine_minerals(self):
        if self.player.is_valid:
            allocation = self._get_minister().mines / 100
            minerals_per_mine = self.mine_tech.output_per_facility
            effort_per_mine = self.mine_tech.effort_per_facility
            operate = min([self.power_plants, allocation * self.effort / effort_per_plant])
            self.effort -= operate * effort_per_plant
            #TODO apply mineral concentration
            self.on_surface.titanium += round(operate * minerals_per_mine)
            self.on_surface.lithium += round(operate * minerals_per_mine)
            self.on_surface.silicon += round(operate * minerals_per_mine)
            #TODO reduce mineral concentration
    
    """ minister checks to see if you need to build more facilities """
    def _check_should_build_facility(self):
        if not self.player.is_valid:
            return
        minister = self._get_minister()
        #scanner_tech = self.player.max_tech('planetary_scanner')
        #penetrating_tech = self.player.max_tech('planetary_penetrating')
        num_facilities = (self.factories + self.power_plants + self.mines + self.defenses)
        if minister.build_penetrating_after_num_facilitys <= num_facilities: # and self.penetrating_tech != penetrating_tech:
        #    self.penetrating_tech = penetrating_tech
            return 'self.penetrating_tech'
        elif minister.build_scanner_after_num_facilitys <= num_facilities: # and self.scanner_tech != scanner_tech:
        #    self.scanner_tech = scanner_tech
            return 'self.scanner_tech'
        else:
            total_effort = round(self.on_surface.people * 1000 * self.player.race.effort_efficency)
            factory_percent = ((self.factory_tech.effort_per_facility * self.factories) / total_effort) - (minister.factories / 100)
            power_plant_percent = ((self.power_plant_tech.effort_per_facility * self.power_plants) / total_effort) - (minister.power_plants / 100)
            mine_percent = ((self.mine_tech.effort_per_facility * self.mines) / total_effort) - (minister.mines / 100)
            defense_percent = ((self.defense_tech.effort_per_facility * self.defenses) / total_effort) - (minister.defenses / 100)
            check = [[factory_percent, 'self.factory_tech'], [power_plant_percent, 'self.power_plant_tech'], [mine_percent, 'self.mine_tech'], [defense_percent, 'self.defense_tech']]
            print(check)
            least = 1
            lest = 0
            for i in range(len(check)):
                if check[i][0] <= least:
                    least = check[i][0]
                    lest = i
            return check[lest][1]
        
    
#TODO    
    """ FIX THIS IN ECONOMY OR MINISTER """
    """ build stuff in build queue """
    def auto_build(self):
        if not self.player.is_valid:
            return
        keep_going = True
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
                spend_e = min([percent_e, item.cost.energy - item.cost_complete.energy])
                if spend_t <= self.minerals.titanium and spend_l <= self.minerals.lithium and spend_s <= self.minerals.silicon and spend_e <= self.player.energy and (spend_t + spend_l + spend_s) <= remaining_production:
                    self.minerals.titanium -= spend_t
                    self.minerals.lithium -= spend_l
                    self.minerals.silicon -= spend_s
                    self.player.energy -= spend_e
                    item.cost_complete.titanium += spend_t
                    item.cost_complete.lithium += spend_l
                    item.cost_complete.silicon += spend_s
                    item.cost_complete.energy += spend_e
                    remaining_production -= spend_t + spend_l + spend_s
                else:
                    keep_going = False
            if len(build_queue) == 0:
                build_queue.push(self._check_should_build_facility())
        max_cap = self._calc_max_production_capacity()
        self._spend_production_capacity((max_cap-self.remaining_production)/max_cap)
        
        
        
    #
    
    """ give player extra effort and set planet effort to 0 """
    def _donate_surplus(self):
        if self.player.is_valid:
            self.player.effort += self.effort
            self.effort = 0

    """ todo """
    """ if inside habitable range return (0..1) """
    """ if outside habitable range return (1..2) bounding at 2 """
    def _calc_range_from_center(self, planet, race_start, race_stop):
        race_radius = float(race_stop - race_start) / 2.0
        if race_radius == 0 and planet == race_start:
            return 0.0
        elif race_radius == 0:
            return 2.0
        else:
            return min([2.0, abs((race_start + race_radius) - planet) / abs(race_radius)])

    """ Calculate the planet's value for the current player (-100 to 100) """
    """ where """
    """ Hab%=SQRT[(1-g)^2+(1-t)^2+(1-r)^2]*(1-x)*(1-y)*(1-z)/SQRT[3] """
    """ g, t, and r are planet_clicks_from_race_center/race_clicks_from_race_center_to_race_edge """
    """ x=g-1/2 for g>1/2 | x=0 for g<1/2 """
    """ y=t-1/2 for t>1/2 | y=0 for t<1/2 """
    """ z=r-1/2 for r>1/2 | z=0 for r<1/2 """
    """ negative planet value is calculated using the same equasion """
    """ with g, t, and r = 0 if < 1 | g, t, r = value - 1 """
    """ and 100 subtracted from the result """
    def _calc_planet_value(self):
        if not self.player.is_valid:
            return 0.0
        g = self._calc_range_from_center(self.gravity, self.player.race.gravity_start, self.player.race.gravity_stop)
        t = self._calc_range_from_center(self.temperature, self.player.race.temperature_start, self.player.race.temperature_stop)
        r = self._calc_range_from_center(self.radiation, self.player.race.radiation_start, self.player.race.radiation_stop)
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

    #def transferpop(self, otherplanet, amount):
    #    for i in range(amount):
    #        if self.pop == 0:
    #            break
    #        self.pop -= 1
    #        otherplanet.pop += 1


Planet.set_defaults(Planet, __defaults)
