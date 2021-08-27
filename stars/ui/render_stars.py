from .playerui import PlayerUI

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
        t = 1
        for (s, i) in self.player().get_intel(by_type='StarSystem').items():
            system = set_details('StarSystem', i)
            self.details[i.system_key] = [system]
        for (s, i) in self.player().get_intel(by_type='Suns').items():
            sun = set_details('Sun', i)
            self.details[i.system_key].append(sun)
        for (p, i) in self.player().get_intel(by_type='Planet').items():
            planet = set_details('Planet', i)
            self.details[i.system_key].append(planet)
        for (a, i) in self.player().get_intel(by_type='Asteroids').items():
            asteroid = set_details('Asteroid', i)
            self.asteroids.append({'location': i.location, 'system_key': i.system_key})
            self.details[i.system_key] = [asteroid]
        for (w, i) in self.player().get_intel(by_type='Wormholes').items():
            wormhole = set_details('Wormhole', i)
            self.wormholes.append({'location': i.location, 'system_key': i.system_key})
            self.details[i.system_key] = [wormhole]
        for (s, i) in self.player().get_intel(by_type='Ship').items():
            ship = set_details('Ship', i)
            if i.system_key in self.details:
                self.details[i.system_key].append(ship)
            else:
                self.deep_space.append({'location': i.location, 'system_key': i.system_key})
                self.details[i.system_key] = [ship]

    def set_details(self, _type, i):
        intel_obj = copy.copy(i)
        obj_dict = {'type': _type}
        key_list = ['system_key', 'location_root', 'location', 'size']
        if hasattr(i, 'location_root_history'):
            key_list.append('location_root_history')
        if not hasattr(i, 'size'):
            intel_obj['size'] = 1
        for key in key_list:
            obj_dict[key] = intel_obj[key]
        return obj_dict


RenderStars.set_defaults(RenderStars, __defaults, sparse_json=False)
