import game_engine
from serializable import Serializable

_defaults = {
    'planets': [],
    'x': 0,
    'y': 0,
    'z': 0
}

class System(Serializable):
    
    """ Initialize defaults """
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        for key in _defaults:
            if key not in kwargs:
                self.__dict__[key] = _defaults[key]
        self.name = kwargs.get('name', 'System_' + str(id(self)))
        if self.planets != []:
            plen = self.planets
            self.planets = []
            for i in range(len(plen)):
                self.planets.append(self.name_planet(plen[i]))
        game_engine.register('System/' + self.name, self)

    """ Names the planet when it is handed one """
    def name_planet(self, planet_name):
        planet = game_engine.get(planet_name)
        if len(self.planets) == 0:
            planet.name = str(self.name) + ' ' + 'Star'
        if len(self.planets) > 0:
            planet.name = str(self.name) + ' ' + ("I" * (len(self.planets)))
        game_engine.register('Planet/' + planet.name, planet)
        return 'Planet/' + planet.name
    

def test():
    print('star_system._test - begin')
    _test_name_planet()
    print('star_system._test - end')

def _test_name_planet():
    print('star_system._test_name_planet - begin')
    test_system = System(name='Tribond', planets=['Planet/trip', 'Planet/Trip'])
    if test_system.name != 'Tribond':
        print('name fail', test_system.name)
    if test_system.planets[0] != 'Planet/Tribond Star':
        print('planet name fail', test_system.planets[0])
    if test_system.planets[1] != 'Planet/Tribond I':
        print('planet name fail', test_system.planets[1])
    print('star_system._test_name_planet - end')
    
