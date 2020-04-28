import game_engine

_defaults = {
    'planets': [],
    'x': 0,
    'y': 0,
    'z': 0
}

class StarSystem:
    
    """ Initialize defaults """
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        for key in _defaults:
            if key not in kwargs:
                self.__dict__[key] = _defaults[key]
        self.name = kwargs.get('name', 'System_' + str(id(self)))
        self.name_planets()
        game_engine.register(self)

    """ Names the planet when it is handed one """
    def name_planets(self):
        counter = 0
        for planet in self.planets:
            if counter == 0:
                planet.name = str(self.name) + ' ' + 'Star'
            else:
                planet.name = str(self.name) + ' ' + ("I" * counter)
            counter += 1

# Register the class with the game engine
game_engine.register_class(StarSystem)


def _test():
    print('star_system._test - begin')
    _test_name_planet()
    print('star_system._test - end')

def _test_name_planet():
    print('star_system._test_name_planet - begin')
    test_system = StarSystem(name='Tribond', planets=[game_engine.Reference('Planet', 'system 1'), game_engine.Reference('Planet', 'system 2')])
    if test_system.name != 'Tribond':
        print('name fail', test_system.name)
    if test_system.planets[0].name != 'Tribond Star':
        print('planet name fail', test_system.planets[0].name)
    if test_system.planets[1].name != 'Tribond I':
        print('planet name fail', test_system.planets[1].name)
    print('star_system._test_name_planet - end')
    
