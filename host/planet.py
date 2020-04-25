import to_json
import cargo
import race

""" List of gravity values for display (0..100) """
__grav_values = [0.20, 0.22, 0.23, 0.24, 0.26, 0.28, 0.29, 0.30, 0.32, 0.34, 0.35, 0.36, 0.38, 0.40, 0.41, 0.42, 0.44, 0.46, 0.47, 0.48, 0.50, 0.52, 0.53, 0.54, 0.56, 0.57, 0.59, 0.60, 0.62, 0.64, 0.65, 0.67, 0.68, 0.70, 0.71, 0.73, 0.74, 0.75, 0.77, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.00, 1.04, 1.08, 1.12, 1.16, 1.20, 1.24, 1.28, 1.32, 1.36, 1.40, 1.44, 1.48, 1.52, 1.56, 1.60, 1.64, 1.68, 1.72, 1.76, 1.80, 1.84, 1.88, 1.92, 1.96, 2.00, 2.11, 2.22, 2.33, 2.44, 2.55, 2.66, 2.77, 2.88, 3.00, 3.12, 3.24, 3.36, 3.48, 3.60, 3.72, 3.84, 3.96, 4.09, 4.22, 4.35, 4.48, 4.61, 4.74, 4.87, 5.00]

""" Planet class """
class Planet(to_json.Serializable):

    """ Create a full class """
    """ name is a string """
    """ radiation int(0..100) """
    """ temperature int(-15, 115) """
    """ gravity int(0..100) """
    def __init__(self, name='', radiation=50, temperature=50, gravity=50):
        self.radiation = int(radiation)
        self.temperature = int(temperature)
        self.gravity = int(gravity)
        self.on_surface = cargo.Cargo()
        self.player = None

    """ Colonize the planet """
    """ race is a dictionary of race parameters """
    def colonize(self, population, race):
        self.on_surface.people = int(population)
        self.player = race

    """ Grow the current population """
    def grow_population(self):
        # all population calculations are done using people but stored using kT (1000/kT)
        if self.player == None:
            return
        try:
            pop = max(0, int(self.on_surface.people) * 1000)
        except ValueError:
            pop = 0
        try:
            rate = float(self.player.get('growth_rate', 10) / 100)
        except ValueError:
            rate = 0.0
        try:
            maxpop = int(self.player.get('maximum_population', 10000000))
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


    """ Return the planet temperature (-260C to 260C) """
    def display_temp(self):
        return str(self.temperature * 4 - 200) + 'C'

    """ Return the planet gravity (0.20g to 5.00g) """
    def display_grav(self):
        return str(grav_values[self.gravity]) + 'g'
    
    """ todo """
    """ if inside habitable range return (0..1) """
    """ if outside habitable range return (1..2) bounding at 2 """
    def __calc_range_from_center(self, planet, race_start, race_stop):
        race_radius = float(race_stop - race_start) / 2.0
        return min([2.0, abs(race_start + race_radius - planet) / race_radius])

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
        g = self.__calc_range_from_center(self.gravity, self.player.get('gravity_start', 0), self.player.get('gravity_stop', 100))
        t = self.__calc_range_from_center(self.temperature, self.player.get('temperature_start', 0), self.player.get('temperature_stop', 100))
        r = self.__calc_range_from_center(self.radiation, self.player.get('radiation_start', 0), self.player.get('radiation_stop', 100))
        negative_offset = 0
        if t > 1.0 or r > 1.0 or g > 1.0:
            negative_offset = -100.0
            g = max(0.0, g - 1.0)
            t = max(0.0, t - 1.0)
            r = max(0.0, r - 1.0)
        x = max(0.0, g - 0.5)
        y = max(0.0, t - 0.5)
        z = max(0.0, r - 0.5)
        return 100 * (((1.0 - g)**2 + (1.0 - t)**2 + (1.0 - r)**2)**0.5) * (1.0 - x) * (1.0 - y) * (1.0 - z) / (3.0**0.5) + negative_offset

    #def transferpop(self, otherplanet, amount):
    #    for i in range(amount):
    #        if self.pop == 0:
    #            break
    #        self.pop -= 1
    #        otherplanet.pop += 1
    


""" Test the Planet class """
def _test():
    print('planet._test - begin')
    _test_grow_population()
    print('planet._test - end')

""" Test the Planet.grow_population method """
def _test_grow_population():
    print('planet._test_grow_population - begin')
    p = Planet('test planet', 50, 50, 50)
    p.colonize(25000, {'growth_rate': 0.15, 'maximum_population': 10000000, 'gravity_start': 20, 'gravity_stop': 80, 'temperature_start': 20, 'temperature_stop': 80, 'radiation_start': 20, 'radiation_stop': 80})
    p.grow_population()
    print('planet._test_grow_population - end')
