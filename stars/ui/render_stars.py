from .playerui import PlayerUI
#''' Test code
from .. import location
from .. import game_engine
#'''Ende test code

""" Default values (default, min, max)  """
__defaults = {
    'systems': [],
    'deep_space': [],
    'wormholes': [],
    'asteroids': [],
    'details': {},
    'deep_space_color': '#999900',
    'systems_color': '#FFFFFF',
    'wormholes_color': '#990099',
    'asteroids_color': '#999999',
}


""" Represent Open Game action """
class RenderStars(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        # Copy all suns
        index = 1 #comment this out with test code
        for (s, i) in self.player().get_intel(by_type='StarSystem').items():
            self.systems.append(i)
            self.details[str(i.location[0]) + ', ' + str(i.location[1]) + ', ' + str(i.location[2])] = []
            '''test code
            if index == 1:
                index = 0
                print(s.__reference__)
                print(game_engine.get(s.__reference__))
                print(game_engine.get('StarSystem/'))
                ' ''test code
                print(s)
                location.Location(0.00001057, 0, 0, reference = s.location)
                self.details[str(i.location[0]) + ', ' + str(i.location[1]) + ', ' + str(i.location[2])].append(
                    self.player().create_fleet(
                        location = location.Location(0.00001057, 0, 0, reference = s.location),
                        name = 'Fleet 1', 
                        ships = [
                            Ship(
                                ID = 'Test Ship1', 
                                fuel = 100, 
                                fuel_max = 400, 
                                cargo = Cargo(
                                    people = 100, 
                                    titanium = 900, 
                                    cargo_max = 1000
                                )), 
                            Ship(
                                ID = 'Test Ship2', 
                                fuel = 100, 
                                fuel_max = 400, 
                                cargo = Cargo(
                                    people = 100, 
                                    titanium = 100, 
                                    cargo_max = 1000
                                ))],
                        orders = [
                            Order(),
                            Order(
                                description = 'We are going to crash!!',
                                location = Reference(self.fleets[0]),
                                load_si = 200,
                                load_li = 200,
                                load_people = 200,
                                load_ti = 200,
                                merge = True
                            )]))
            #end test code'''
        for (s, i) in self.player().get_intel(by_type='Suns').items():
            print('suns')
            print(i.__dict__)
            self.details[i.location_root].append(i)
        for (p, i) in self.player().get_intel(by_type='Planet').items():
            print(i.__dict__)
            self.details[i.location_root].append(i)
        for (a, i) in self.player().get_intel(by_type='Asteroids').items():
            print(i.__dict__)
            self.asteroids.append({'location': i.location, 'location_root': i.location_root})
            self.details[i.location_root].append(i)
        for (w, i) in self.player().get_intel(by_type='Wormholes').items():
            self.wormholes.append({'location': i.location, 'location_root': i.location_root})
            self.details[i.location_root].append(i)
        for (s, i) in self.player().get_intel(by_type='Ship').items():
            print('there is a ship')
            if hasattr(i, 'location_root'):
                if i.location_root in self.details:
                    self.details[i.location_root].append(i)
                else:
                    self.deep_space.append({'location': i.location, 'location_root': i.location_root})
                    self.details[i.location_root] = [i]
            else:
                self.deep_space.append({'location': i.location, 'location_root': 'location_root does not exist'})
                self.details[i.location_root] = [i]


RenderStars.set_defaults(RenderStars, __defaults, sparse_json=False)
