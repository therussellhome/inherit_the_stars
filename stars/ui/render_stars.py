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
    'home_system': '',
    'homeworld': (1, 0, 10),
    
}


""" Represent Open Game action """
class RenderStars(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        # Copy all suns
        for (s, i) in self.player.get_intel(by_type='StarSystem').items():
            system = self.set_details('StarSystem', self.systems_color, i, s.ID)
            self.systems.append({'location': i.xyz, 'system_key': i.system_key})
            self.details[i.system_key] = [system]
        for (s, i) in self.player.get_intel(by_type='Sun').items():
            sun = self.set_details('Sun', i.color, i, s.ID)
            self.details[i.system_key].append(sun)
        for (p, i) in self.player.get_intel(by_type='Planet').items():
            if p.ID == self.player.planets[0].ID:
                self.home_system = i.system_key
                self.homeworld = len(self.details[i.system_key]) -1
            planet = self.set_details('Planet', i.color, i, p.ID)
            self.details[i.system_key].append(planet)
        for (a, i) in self.player.get_intel(by_type='Asteroid').items():
            asteroid = self.set_details('Asteroid', self.asteroids_color, i, a.ID)
            self.asteroids.append({'location': i.xyz, 'system_key': i.system_key})
            if i.system_key not in self.details:
                self.details[i.system_key] = []
            self.details[i.system_key].append(asteroid)
        for (w, i) in self.player.get_intel(by_type='Wormhole').items():
            wormhole = self.set_details('Wormhole', self.wormholes_color, i, w.ID)
            self.wormholes.append({'location': i.xyz, 'system_key': i.system_key})
            if i.system_key not in self.details:
                self.details[i.system_key] = []
            self.details[i.system_key].append(wormhole)
        for (s, i) in self.player.get_intel(by_type='Ship').items():
            team = 'other'
            ship = self.set_details('Ship', self.deep_space_color, i, s.ID)
            for s1 in self.player.ships:
                if s == s1:
                    team = 'me'
            if i.system_key not in self.details:
                self.deep_space.append({'location': i.xyz, 'system_key': i.system_key})
                self.details[i.system_key] = []
            self.details[i.system_key].append(ship)
            self.details[i.system_key][-1]['team'] = team
            if team == 'me':
                for f in self.player.fleets:
                    for s1 in f.ships:
                        if s == s1:
                            self.details[i.system_key][-1]['fleet'] = 'Fleet/' + f.ID
                            break
                    for s1 in f.under_construction:
                        if s == s1:
                            self.details[i.system_key][-1]['fleet'] = 'Fleet/' + f.ID
                            break

    def set_details(self, _type, _color, i, ID):
        intel_obj = copy.copy(i)
        obj_dict = {'type': _type, 'color': _color, 'ID': ID}
        key_list = ['system_key', 'location_root', 'location', 'size']
        if hasattr(i, 'location_root_history'):
            key_list.append('location_root_history')
        if not hasattr(i, 'size'):
            intel_obj['size'] = 1
        for key in key_list:
            key1 = key
            if key == 'location':
                key1 = 'xyz'
            obj_dict[key] = intel_obj.__dict__[key1]
        return obj_dict


RenderStars.set_defaults(RenderStars, __defaults, sparse_json=False)
