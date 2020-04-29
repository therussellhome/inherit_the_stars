import game_engine
from random import randint

_defaults = {
    'planets': [[]],
    'x': [0, -1000, 1000],
    'y': [0, -1000, 1000],
    'z': [0, -1000, 1000],
    'num_planets': [2, 0, 5]
}

_roman = ["I", "II", "III", "IV", "V"]

class StarSystem(game_engine.Defaults):
    
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)
        if 'name' not in kwargs:
            self.name = 'System_' + str(id(self))
        if len(self.planets) == 0:
            self._create_system()
        game_engine.register(self)

    """ create planets """
    def _create_system(self):
        self.planets = []
        planet_args = {
            'reference': 'Planet/' + str(self.name) + "'s " + 'Star',
            'star_system': game_engine.Reference(self)
            }
        sun = game_engine.Reference(**planet_args)
        self.planets.append(sun)
        
        segment = 100.0 / self.num_planets
        for i in range(self.num_planets):
            planet_args['reference'] = 'Planet/' + str(self.name) + ' ' + _roman[i]
            planet_args['sun'] = self.planets[0]
            planet_args['distance'] = round(segment * i + randint(5, segment))
            self.planets.append(game_engine.Reference(**planet_args))
    
        

# Register the class with the game engine
game_engine.register(StarSystem, defaults=_defaults)


def _test():
    print('star_system._test - begin')
    _test_name_planet()
    print('star_system._test - end')

def _test_name_planet():
    print('star_system._test_name_planet - begin')
    test_system = StarSystem(name='Tribond', num_planets=6)
    if test_system.name != 'Tribond':
        print('name fail', test_system.name)
    if test_system.planets[0].name != "Tribond's Star":
        print('planet name fail', test_system.planets[0].name)
    if test_system.planets[1].name != 'Tribond I':
        print('planet name fail', test_system.planets[1].name)
    if test_system.planets[2].name != 'Tribond II':
        print('planet name fail', test_system.planets[2].name)
    print('star_system._test_name_planet - end')
    
