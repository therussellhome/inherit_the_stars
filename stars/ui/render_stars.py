from .playerui import PlayerUI
import copy

""" Default values (default, min, max)  """
__defaults = {
    'systems': [],
    'deep_space': [],
    'wormholes': [],
    'asteroids': [],
    'details': {},
    'deep_space_color': '#FFFF00',
    'systems_color': '#FFFFFF',
    'wormholes_color': '#FF00FF',
    'asteroids_color': '#00FFFF',
}


""" Represent Open Game action """
class RenderStars(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        # Copy all suns
        for (s, i) in self.player().get_intel(by_type='StarSystem').items():
            system = self.set_details('StarSystem', self.systems_color, i)
            self.systems.append({'location': i.location, 'system_key': i.system_key})
            self.details[i.system_key] = [system]
        for (s, i) in self.player().get_intel(by_type='Suns').items():
            sun = self.set_details('Sun', i.color, i)
            self.details[i.system_key].append(sun)
        for (p, i) in self.player().get_intel(by_type='Planet').items():
            planet = self.set_details('Planet', i.color, i)
            self.details[i.system_key].append(planet)
        for (a, i) in self.player().get_intel(by_type='Asteroids').items():
            asteroid = self.set_details('Asteroid', self.asteroids_color, i)
            self.asteroids.append({'location': i.location, 'system_key': i.system_key})
            self.details[i.system_key] = [asteroid]
        for (w, i) in self.player().get_intel(by_type='Wormholes').items():
            wormhole = self.set_details('Wormhole', self.wormholes_color, i)
            self.wormholes.append({'location': i.location, 'system_key': i.system_key})
            self.details[i.system_key] = [wormhole]
        for (s, i) in self.player().get_intel(by_type='Ship').items():
            ship = self.set_details('Ship', self.deep_space_color, i)
            if i.system_key in self.details:
                self.details[i.system_key].append(ship)
            else:
                self.deep_space.append({'location': i.location, 'system_key': i.system_key})
                self.details[i.system_key] = [ship]

    def set_details(self, _type, _color, i):
        intel_obj = copy.copy(i)
        obj_dict = {'type': _type, 'color': _color}
        key_list = ['system_key', 'location_root', 'location', 'size']
        if hasattr(i, 'location_root_history'):
            key_list.append('location_root_history')
        if not hasattr(i, 'size'):
            intel_obj['size'] = 1
        for key in key_list:
            obj_dict[key] = intel_obj.__dict__[key]
        return obj_dict


RenderStars.set_defaults(RenderStars, __defaults, sparse_json=False)
