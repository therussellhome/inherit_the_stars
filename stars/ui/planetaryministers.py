from .playerui import PlayerUI
from ..planetary_minister import PlanetaryMinister

""" Default values (default, min, max)  """
__defaults = {
    'planetary_new_col_minister': [''],
    'options_planetary_new_col_minister': [[]],
    'planetary_facility_types': [[30.0, 60.0, 90.0]],
    'planetary_power': [''],
    'planetary_factory': [''],
    'planetary_mine': [''],
    'planetary_shield': [''],
    'planetary_planets': [[]],
    'planetary_sidebar': [[]],
    'planetary___uuid__': [''],
}

""" """
class PlanetaryMinisters(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        if self.planetary___uuid__ == '':
            for key in self.player.planetary_ministers:
                self.planetary___uuid__ = key
                break
        if action.startswith('uuid='):
            self.planetary___uuid__ = action[5:]
            action = 'revert'
        if action == 'new':
            mini = PlanetaryMinister()
            self.player.planetary_ministers[mini.__uuid__] = mini
            self.planetary___uuid__ = mini.__uuid__
            action = 'revert'
        if action == 'revert':
            self.planetary_name = self.player.planetary_ministers[self.planetary___uuid__].name
            for key in self.player.planetary_ministers[self.planetary___uuid__].__dict__:
                setattr(self, 'planetary_' + key, getattr(self.player.planetary_ministers[self.planetary___uuid__], key))
            self.planetary_facility_types[0] = getattr(self, 'planetary_Power Plant')
            self.planetary_facility_types[1] = getattr(self, 'planetary_Power Plant') + getattr(self, 'planetary_Factory')
            self.planetary_facility_types[2] = getattr(self, 'planetary_Mineral Extractor') + self.planetary_facility_types[1]
        #for key in self.player.planetary_ministers:
        #    print(self.player.planetary_ministers[key].__dict__)
        """ set the new colony minister. """
        for key in self.player.planetary_ministers:
            minister = self.player.planetary_ministers[key]
            minister.new_colony_minister = False
            if minister.name == self.planetary_new_col_minister:
                minister.new_colony_minister = True
        """ save """
        setattr(self, 'planetary_Power Plant', self.planetary_facility_types[0])
        setattr(self, 'planetary_Factory', self.planetary_facility_types[1]-self.planetary_facility_types[0])
        setattr(self, 'planetary_Mineral Extractor', self.planetary_facility_types[2]-self.planetary_facility_types[1])
        setattr(self, 'planetary_Planetary Shield', 100-self.planetary_facility_types[2])
        for key in self.player.planetary_ministers[self.planetary___uuid__].__dict__:
            setattr(self.player.planetary_ministers[self.planetary___uuid__], key, getattr(self, 'planetary_' + key))
        for planet in self.player.planets:
            self.player.planets[planet] = getattr(self, 'planetary_' + planet.name + '_minister')
        """ set display values """
        for key in self.player.planetary_ministers:
            self.options_planetary_new_col_minister.append(self.player.planetary_ministers[key].name)
        self.planetary_power = str(getattr(self, 'planetary_Power Plant')) + ' %'
        self.planetary_factory = str(getattr(self, 'planetary_Factory')) + ' %'
        self.planetary_mine = str(getattr(self, 'planetary_Mineral Extractor')) + ' %'
        self.planetary_shield = str(getattr(self, 'planetary_Planetary Shield')) + ' %'
        for planet in self.player.planets:
            setattr(self, 'options_planetary_' + planet.name + '_minister', self.option_planteary_new_col_minister)
            self.planetary_planets.append('<td>' + planet.name + '<select id="planetary_' + planet.name + '_minister" style="width: 100%" onchange="post(\'planetary_minister\')"/></td>')
        self.planetary_sidebar.append('<td><img class="button" id="ministers_all" title="ministers" src="/planetary_minister.png" onclick="show_screen(\'planetary_ministers\')"/></td>')
        for key in self.player.planetary_ministers:
            minister = self.player.planetary_ministers[key]
            self.planetary_sidebar.append('<td><img class="button" id="planetary_' + minister.name + '" title="' + minister.name + '" style="background: ' + minister.color + '" src="/planetary_minister.png" onclick="show_minister(\'uuid=' + minister.__uuid__ + '\')"/></td>')
        self.planetary_sidebar.append('<td><i class="button far fa-plus-circle" title="new minister" onclick="show_minister(\'new\')"></i></td>')
    

for key in PlanetaryMinister.defaults:
    __defaults['planetary_' + key] = PlanetaryMinister.defaults[key]

PlanetaryMinisters.set_defaults(PlanetaryMinisters, __defaults, sparse_json=False)
