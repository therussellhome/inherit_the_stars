import sys
import game_engine
from cargo import Cargo
from minerals import Minerals
from random import randint

""" List of gravity values for display (0..100) """
_grav_values = [0.20, 0.22, 0.23, 0.24, 0.26, 0.28, 0.29, 0.30, 0.32, 0.34, 0.35, 0.36, 0.38, 0.40, 0.41, 0.42, 0.44, 0.46, 0.47, 0.48, 0.50, 0.52, 0.53, 0.54, 0.56, 0.57, 0.59, 0.60, 0.62, 0.64, 0.65, 0.67, 0.68, 0.70, 0.71, 0.73, 0.74, 0.75, 0.77, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.00, 1.04, 1.08, 1.12, 1.16, 1.20, 1.24, 1.28, 1.32, 1.36, 1.40, 1.44, 1.48, 1.52, 1.56, 1.60, 1.64, 1.68, 1.72, 1.76, 1.80, 1.84, 1.88, 1.92, 1.96, 2.00, 2.11, 2.22, 2.33, 2.44, 2.55, 2.66, 2.77, 2.88, 3.00, 3.12, 3.24, 3.36, 3.48, 3.60, 3.72, 3.84, 3.96, 4.09, 4.22, 4.35, 4.48, 4.61, 4.74, 4.87, 5.00]

""" Default values (default, min, max)  """
__defaults = {
    'distance': [50, 0, 100],
    'temperature': [50, -15, 115],
    'radiation': [50, 0, 100],
    'gravity': [50, 0, 100],
    'effort': [0, 0, sys.maxsize],
    'energy': [0, 0, sys.maxsize],
    'power_plants': [0, 0, sys.maxsize],
    'factories': [0, 0, sys.maxsize],
    'mines': [0, 0, sys.maxsize],
    'power_plant_tech': [{}],
    'factory_tech': [{}],
    'mine_tech': [{}],
    'is_tax_haven': [False],
    'mineral_concentration': [Minerals(titanium=100.0, lithium=100.0, silicon=100.0)],
    'on_surface': [Cargo()],
    'player': [game_engine.Reference()],
    'star_system': [game_engine.Reference()]
}

""" TODO """
class Planet(game_engine.Defaults):

    """ Initialize defaults """
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)
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

                

#    """ Handle planet renaming """
#    def __setattr__(self, name, value):
#        self.__dict__[name] = value
#        if name == 'name':
#            game_engine.register(self)

    """ Return the planet temperature (-260C to 260C) """
    def display_temp(self):
        return str(self.temperature * 4 - 200) + 'C'

    """ Return the planet gravity (0.20g to 5.00g) """
    def display_grav(self):
        return str(_grav_values[self.gravity]) + 'g'
    
    """ Colonize the planet """
    """ where player is a game_engine.Reference to "Player/<player_name>" """
    def colonize(self, population, player):
        self.on_surface.people = int(population)
        self.player = player
        #TODO self.power_plant_tech = self.player.max_tech('power_plant')
        #TODO self.factory_tech = self.player.max_tech('factory')
        #TODO self.mine_tech = self.player.max_tech('mine')

    """ runs the turn """
    def take_turn(self):
        self.grow_population()
        self.calculate_effort()
        self.pay_effort_tax()
        self.generate_energy()
        self.pay_energy_tax()
        self.recv_stimulus()
        self.mine_minerals()
        self.build_stuff()
        self.donate_surplus()
    
    """ Grow the current population """
    def grow_population(self):
        # all population calculations are done using people but stored using kT (1000/kT)
        if not self.player.is_valid:
            return
        try:
            pop = max(0, int(self.on_surface.people) * 1000)
        except ValueError:
            pop = 0
        try:
            rate = self.player.race.growth_rate / 100.0
        except ValueError:
            rate = 0.0
        try:
            maxpop = self.player.race.population_max
        except ValueError:
            maxpop = 10000000
        planetvalue = self.calc_planet_value()
        maxpop *= planetvalue
        h = maxpop / 2.0
        g = float(float(maxpop) / float(h + pop)) / 2.0
        rate = (g * rate)
        if pop < maxpop:
            pop *= (rate + 1.0)
            if pop > maxpop:
                pop = maxpop
        elif pop > maxpop:
            pop *= (-rate + 1.0)
            if pop < maxpop:
                pop = maxpop
        self.on_surface.people = int(round(pop, -3))

    """ calculate how much effort is produced by the population """
    def calculate_effort(self):
        if self.player.is_valid:
            self.effort = round(self.on_surface.people * 1000 * self.player.race.effort_efficency / 100)
    
    """ power plants make energy """
    def generate_energy(self):
        energy_per_plant = int(self.power_plant_tech.get('energy_per_plant', 100))
        effort_per_plant = int(self.power_plant_tech.get('effort_per_plant', 1000))
        operate = self.power_plants
        if effort_per_plant > 0:
            max_effort = self.power_plants * effort_per_plant
            effort = min([self.effort, max_effort])
            self.effort -= effort
            operate = operate * effort / max_effort
        self.energy = operate * energy_per_plant
    
    """ pays the tax on effort for research """
    def pay_effort_tax(self):
        if self.player.is_valid:
            if not self.is_tax_haven:
                tax_effort = round(self.effort * (self.player.research_rate / 100))
                self.player.effort += tax_effort
                self.effort -= tax_effort
    
    """ pays the tax in energy """
    def pay_energy_tax(self):
        if self.player.is_valid:
            if not self.is_tax_haven:
                tax_energy = round(self.energy * (self.player.tax_rate / 100))
                self.player.energy += tax_energy
                self.energy -= tax_energy
    
    """ invests energy into planetary economy """
    def recv_stimulus(self):
        if self.player.is_valid:
            stimulus_package = min(self.player.energy, round(self.on_surface.people * self.player.stimulus_package))
            self.energy += stimulus_package
            self.player.energy -= stimulus_package
    
    """ mines mine the minerals """
    def mine_minerals(self):
        minerals_per_mine = float(self.mine_tech.get('minerals_per_mine', 1.0))
        effort_per_mine = int(self.mine_tech.get('effort_per_mine', 1000))
        operate = self.mines
        if effort_per_mine > 0:
            max_effort = self.mines * effort_per_plant
            effort = min([self.effort, max_effort])
            self.effort -= effort
            operate = operate * effort / max_effort
        self.on_surface.titanium += round(operate * minerals_per_mine)
        self.on_surface.lithium += round(operate * minerals_per_mine)
        self.on_surface.silicon += round(operate * minerals_per_mine)
        #TODO reduce mineral concentration
    
    """ build stuff in build queue """
    def build_stuff(self):
        #TODO fix method for player access
        if not self.player.is_valid:
            return
        for item in self.build_queue:
            s_item = item.split(":")
            for i in range(int(s_item[1])):
                if s_item[0] == "uf" and self.player.research_level > self.factory_level:
                    factory_upgrade_cost_minerals = round(0.01 * self.factory_level * self.player.factory_cost.minerals * (self.factories))
                    factory_upgrade_cost_money = round(0.01 * self.factory_level * self.player.factory_cost.money * (self.factories))
                    factory_upgrade_cost_effort = round(0.01 * self.factory_level * self.player.factory_cost.effort * (self.factories))
                    if self.minerals >= factory_upgrade_cost_minerals and self.money >= factory_upgrade_cost_money and self.effort >= factory_upgrade_cost_effort:
                        self.minerals -= factory_upgrade_cost_minerals
                        self.money -= factory_upgrade_cost_money
                        self.effort -= factory_upgrade_cost_effort
                        self.factory_level += 1
                if s_item[0] == "um" and self.player.research_level > self.mine_level:
                    mine_upgrade_cost_minerals = round(0.01 * self.mine_level * self.player.mine_cost.minerals * (self.mines))
                    mine_upgrade_cost_money = round(0.01 * self.mine_level * self.player.mine_cost.money * (self.mines + 1))
                    mine_upgrade_cost_effort = round(0.01 * self.mine_level * self.player.mine_cost.effort * (self.mines + 1))
                    if self.minerals >= mine_upgrade_cost_minerals and self.money >= mine_upgrade_cost_money and self.effort >= mine_upgrade_cost_effort:
                        self.minerals -= mine_upgrade_cost_minerals
                        self.money -= mine_upgrade_cost_money
                        self.effort -= mine_upgrade_cost_effort
                        self.mine_level += 1
                if s_item[0] == "f" and self.minerals >= self.player.factory_cost.minerals and self.money >= self.player.factory_cost.money and self.effort >= self.player.factory_cost.effort:
                    self.minerals -= self.player.factory_cost.minerals
                    self.money -= self.player.factory_cost.money
                    self.effort -= self.player.factory_cost.effort
                    self.factories += 1
                if s_item[0] == "m" and self.minerals >= self.player.mine_cost.minerals and self.money >= self.player.mine_cost.money and self.effort >= self.player.mine_cost.effort:
                    self.minerals -= self.player.mine_cost.minerals
                    self.money -= self.player.mine_cost.money
                    self.effort -= self.player.mine_cost.effort
                    self.mines += 1
    
    """ give player extra energy and effort and set planet energy and effort to 0 """
    def donate_surplus(self):
        if self.player.is_valid:
            self.player.energy += self.energy
            self.energy = 0
            self.player.effort += self.effort
            self.effort = 0

    """ todo """
    """ if inside habitable range return (0..1) """
    """ if outside habitable range return (1..2) bounding at 2 """
    def __calc_range_from_center(self, planet, race_start, race_stop):
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
    def calc_planet_value(self):
        if not self.player.is_valid:
            return 0.0
        g = self.__calc_range_from_center(self.gravity, self.player.race.gravity_start, self.player.race.gravity_stop)
        t = self.__calc_range_from_center(self.temperature, self.player.race.temperature_start, self.player.race.temperature_stop)
        r = self.__calc_range_from_center(self.radiation, self.player.race.radiation_start, self.player.race.radiation_stop)
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

# Register the class with the game engine
game_engine.register(Planet, defaults=__defaults)


""" Test the Planet class """
def _test():
    print('planet._test - begin')
    _test_grow_population()
    _test_calc_planet_value()
    print('planet._test - end')

def test_expect(actual, expect, test_id):
    if expect != actual:
        print('ERROR ', test_id, ' got ', actual, ' expected ', expect)

""" Test the Planet.grow_population method """
def _test_grow_population():
    print('planet._test_grow_population - begin')
    p = Planet()
    player = Player(name='test_grow')
    p.colonize(25000, 'Player/test_grow')
    p.grow_population()
    p = Planet()
    player.race.growth_rate = 10
    player.race.maximum_population = 10000000
    player.race.gravity_start = 25
    player.race.gravity_stop = 75
    player.race.temperature_start = 25
    player.race.temperature_stop = 75
    player.race.radiation_start = 25
    player.race.radiation_stop = 75
    p.colonize(250, 'Player/test_grow')
    p.grow_population()
    test_expect(p.on_surface.people, 274, 'grow_test #1')
    p.on_surface.people = 0
    p.grow_population()
    test_expect(p.on_surface.people, 0, 'grow_test #2')
    p.on_surface.people = -10
    p.grow_population()
    test_expect(p.on_surface.people, 0, 'grow_test #3')
    p.on_surface.people = 250
    player.race.growth_rate = 0
    p.grow_population()
    test_expect(p.on_surface.people, 250, 'grow_test #4')
    p.on_surface.people = 250
    player.race.growth_rate = -10
    p.grow_population()
    test_expect(p.on_surface.people, 226, 'grow_test #5')
    p.on_surface.people = 'me'
    p.grow_population()
    test_expect(p.on_surface.people, 0, 'grow_test #6')
    p.on_surface.people = 250
    player.race.growth_rate = 'chicken'
    p.grow_population()
    test_expect(p.on_surface.people, 250, 'grow_test #7')
    p.temperature = 100
    p.gravity = 100
    p.radiation = 100
    p.on_surface.people = 250
    player.race.growth_rate = -10
    p.grow_population()
    test_expect(p.on_surface.people, 276, 'grow_test #8')
    p.on_surface.people = 250
    player.race.growth_rate = 10
    p.grow_population()
    test_expect(p.on_surface.people, 224, 'grow_test #9')
    p.temperature = 50
    p.gravity = 50
    p.radiation = 50
    p.on_surface.people = 250
    player.race.growth_rate = -20
    p.grow_population()
    test_expect(p.on_surface.people, 202, 'grow_test #10')
    p.temperature = 100/4
    p.gravity = 100/4
    p.radiation = 100/4
    p.on_surface.people = 250
    player.race.growth_rate = 10
    p.grow_population()
    p.grow_population()
    test_expect(p.on_surface.people, 250, 'grow_test #11')
    p.on_surface.people = 100
    player.race.growth_rate = 20
    p.grow_population()
    test_expect(p.on_surface.people, 120, 'grow_test #12')
    p.grow_population()
    test_expect(p.on_surface.people, 144, 'grow_test #13')
    p.on_surface.population = 10000
    p.grow_population()
    test_expect(p.on_surface.people, 10000, 'grow_test #14')

def _test_calc_planet_value_expect(planet, g, t, r, g_start, g_stop, t_start, t_stop, r_start, r_stop, expect, test_id):
    planet.gravity = g
    planet.temperature = t
    planet.radiation = r
    planet.player.race.gravity_start = g_start
    planet.player.race.gravity_stop = g_stop
    planet.player.race.temperature_start = t_start
    planet.player.race.temperature_stop = t_stop
    planet.player.race.radiation_start = r_start
    planet.player.race.radiation_stop = r_stop
    try:
        test_expect(planet.calc_planet_value(), expect, test_id)
    except BaseException as e:
        print('ERROR ', test_id, e)

""" Test the Planet.calc_planet_value method """
def _test_calc_planet_value():
    print('planet._test_calc_planet_value - begin')
    planet = Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
    planet.colonize(25000, game_engine.Reference('Player', 'test_planet_value'))
    _test_calc_planet_value_expect(planet, 50, 50, 50, 0, 100, 0, 100, 0, 100, 100, "test 1")
    _test_calc_planet_value_expect(planet, 0, 50, 50, 0, 100, 0, 100, 0, 100, 41, "test 2")
    _test_calc_planet_value_expect(planet, 0, -15, 50, 0, 100, 0, 100, 0, 100, -9, "test 3") 
    _test_calc_planet_value_expect(planet, 4, 114, 12, 0, 100, 0, 100, 0, 100, -8, "test 4") 
    _test_calc_planet_value_expect(planet, 100, -12, 0, 0, 100, 110, 114, 0, 100, -59, "test 5")
    _test_calc_planet_value_expect(planet, 0, 115, 100, 99, 100, -1, -15, 0, 12, -100, "test 6")
    _test_calc_planet_value_expect(planet, 99, 1, 6, 98, 100, -1, -15, 0, 12, -59, "test 7")
    _test_calc_planet_value_expect(planet, 30, 30, 30, 0, 100, 0, 100, 0, 100, 60, "test 8")
    _test_calc_planet_value_expect(planet, 30, 90, 60, 0, 100, 0, 100, 0, 100, 41, "test 9")
    _test_calc_planet_value_expect(planet, 18, 1, 40, 0, 100, 0, 100, 0, 100, 23, "test 10") 
    _test_calc_planet_value_expect(planet, 300, 2000, 'me', 0, 100, 0, 100, 0, 100, -9, "test 11")
    _test_calc_planet_value_expect(planet, 150, 304, 30, -900, 100, 0, -8000, 0, 100, -59, "test 12")
    _test_calc_planet_value_expect(planet, -30, 30, -0, 0, 10, 0, 00, 0, 360, -59, "test 13")
    _test_calc_planet_value_expect(planet, 950, 3300, -430, 0, 100, 0, 1010, 'break', 100, -9, "test 14")
    _test_calc_planet_value_expect(planet, 70, 33, -430, 0, 100, 0, 68, 90, 100, -59, "test 15")
    _test_calc_planet_value_expect(planet, 950, 60, 70, 70, 100, 70, 100, 70, 100, -30, "test 16")
    print('planet._test_calc_planet_value - end')    
