from .playerui import PlayerUI
from ..planetary_minister import PlanetaryMinister
from ..reference import Reference

""" Default values (default, min, max)  """
__defaults = {
    'planetary_new_col_minister': '',
    'options_planetary_new_col_minister': [],
    'planetary_facility_types': [30.0, 60.0, 90.0],
    'planetary_power': '',
    'planetary_factory': '',
    'planetary_mine': '',
    'planetary_shield': '',
    'planetary_planets': [],
    'planetary_sidebar': [],
    'planetary_curent_minister': Reference('PlanetaryMinister'),
}

""" """
class PlanetaryMinisters(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        #print('1', action)
        self.planetary_curent_minister = Reference('PlanetaryMinister/' + self.planetary_ID)
        if not self.planetary_curent_minister:
            self.planetary_curent_minister = Reference(self.player.ministers[-1])
        if action.startswith('uuid='):
            self.planetary_curent_minister = Reference('PlanetaryMinister/' + action[5:])
            action = 'revert'
        if action == 'new':
            mini = PlanetaryMinister()
            self.player.ministers.append(mini)
            self.planetary_curent_minister = Reference(mini)
            action = 'revert'
        #for key in PlanetaryMinister.defaults:
        #    print('3', key, self.planetary_curent_minister[key])
        #print('2', self.planetary_curent_minister.__dict__)
        if action == 'revert':
            self.planetary_name = self.planetary_curent_minister.name
            for key in PlanetaryMinister.defaults:
                setattr(self, 'planetary_' + key, getattr(self.planetary_curent_minister, key))
            self.planetary_facility_types[0] = self.planetary_power_plants
            self.planetary_facility_types[1] = self.planetary_factories + self.planetary_facility_types[0]
            self.planetary_facility_types[2] = self.planetary_mineral_extractors + self.planetary_facility_types[1]
        #for minister in self.player.ministers:
        #    print('4 minister  = ', minister.__dict__)
        #print('self  = ', self.__dict__)
        """ set the new colony minister. """
        if self.planetary_new_col_minister == '':
            for minister in self.player.ministers:
                if hasattr(minister, 'new_colony_minister'):
        #            print(minister.__dict__)
                    if minister.new_colony_minister:
                        self.planetary_new_col_minister = minister.name
        #print('5', self.planetary_curent_minister.__dict__)
        for minister in self.player.ministers:
            if hasattr(minister, 'new_colony_minister'):
                minister.new_colony_minister = False
                if minister.name == self.planetary_new_col_minister:
                    minister.new_colony_minister = True
        #print('6', self.planetary_curent_minister.__dict__)
        """ save """
        self.planetary_power_plants = self.planetary_facility_types[0]
        self.planetary_factories = self.planetary_facility_types[1]-self.planetary_facility_types[0]
        self.planetary_mineral_extractors = self.planetary_facility_types[2]-self.planetary_facility_types[1]
        self.planetary_defenses = 100-self.planetary_facility_types[2]
        for key in PlanetaryMinister.defaults:
            if not key == 'ID':
                setattr(self.planetary_curent_minister, key, getattr(self, 'planetary_' + key))
        #        print('7', key, self.planetary_curent_minister[key])
        """ make minister selection """
        for planet in self.player.planets:
            planet = Reference(planet)
            if hasattr(self, 'planetary_' + planet.ID + '_minister'):
                self.player.planetary_minister_map[planet] = Reference('PlanetaryMinister/' + self['planetary_' + planet.ID + '_minister'])
            if planet in self.player.planetary_minister_map:
                self.player.planetary_minister_map[planet] = Reference(self.player.get_minister(planet))
        #print('8', self.planetary_curent_minister.__dict__)
        """ set display values """
        for minister in self.player.ministers:
            if hasattr(minister, 'new_colony_minister'):
                self.options_planetary_new_col_minister.append(minister.name)
        self.planetary_power = str(self.planetary_power_plants) + ' %'
        self.planetary_factory = str(self.planetary_factories) + ' %'
        self.planetary_mine = str(self.planetary_mineral_extractors) + ' %'
        self.planetary_shield = str(self.planetary_defenses) + ' %'
        m_list = ''
        for m in self.player.ministers:
            if hasattr(minister, 'new_colony_minister'):
                m_list += '<option value="' + m.ID + '">' + m.name + '</option>'
        for (p, m) in self.player.planetary_minister_map.items():
            p_tmp = '<select id="planetary_' + p.ID + '_minister" onchange="post(\'planetary_minister\')">' + m_list + '</select>'
            self['planetary_' + p.ID + '_minister'] = m.ID
            self.planetary_planets.append('<td>' + p.ID + '</td><td class="hfill">' + p_tmp.replace(m.ID + '"', m.ID + '" selected') + '</td>')
        #for planet in self.player.planetary_minister_map:
        #    setattr(self, 'options_planetary_' + planet.ID + '_minister', self.options_planetary_new_col_minister)
        #    self.planetary_planets.append('<td>' + planet.ID + '<select id="planetary_' + planet.ID + '_minister" style="width: 100%" /></td>')
        self.planetary_sidebar.append('<td><img class="button" title="ministers" src="/planetary_minister.png" onclick="show_screen(\'planetary_ministers\')"/></td>')
        for minister in self.player.ministers:
            if hasattr(minister, 'new_colony_minister'):
                self.planetary_sidebar.append('<td><img class="button" title="' + minister.name + '" style="background: ' + minister.color + '" src="/planetary_minister.png" onclick="show_minister(\'uuid=' + minister.ID + '\')"/></td>')
        self.planetary_sidebar.append('<td><i class="button fas fa-plus-circle" title="new minister" onclick="show_minister(\'new\')"></i></td>')
    

for key in PlanetaryMinister.defaults:
    __defaults['planetary_' + key] = PlanetaryMinister.defaults[key]

PlanetaryMinisters.set_defaults(PlanetaryMinisters, __defaults, sparse_json=False)
