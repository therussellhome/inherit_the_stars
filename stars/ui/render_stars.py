from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'systems': [],
    'deep_space': [],
    'wormholes': [],
    'asteroids': [],
    'details': {},
    'deep_space_color': '0x999900'
    'systems_color': '0xffffff'
    'wormholes_color': '0x990099'
    'asteroids_color': '0x999999'
}


""" Represent Open Game action """
class RenderStars(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        # Copy all suns
        for (s, i) in self.player().get_intel(by_type='StarSystem').items():
            self.systems.append(i)
            self.details[i.location] = []
        for (s, i) in self.player().get_intel(by_type='Suns').items():
            self.details[i.location_root].append(i)
        for (p, i) in self.player().get_intel(by_type='Planet').items():
            self.details[i.location_root].append(i)
        for (p, i) in self.player().get_intel(by_type='Asteroids').items():
            self.asteroids.append({'location': i.location, 'location_root': i.location_root})
            self.details[i.location_root].append(i)
        for (p, i) in self.player().get_intel(by_type='Wormholes').items():
            self.wormholes.append({'location': i.location, 'location_root': i.location_root})
            self.details[i.location_root].append(i)
        for (s, i) in self.player().get_intel(by_type='Ship').items():
            if i.location_root in self.details:
                self.details[i.location_root].append(i)
            else:
                self.deep_space.append({'location': i.location, 'location_root': i.location_root})
                self.details[i.location_root] = [i]


RenderStars.set_defaults(RenderStars, __defaults, sparse_json=False)
