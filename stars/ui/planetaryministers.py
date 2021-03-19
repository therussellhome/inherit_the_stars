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
            self.planetary___uuid__ = self.player.planetary_ministers[0].__uuid__
        if action.startswith('uuid='):
            self.planetary___uuid__ = action[5:]
            action = 'revert'
        if action == 'new':
            mini = PlanetaryMinister()
            self.player.planetary_ministers.append(mini)
            self.planetary___uuid__ = mini.__uuid__
            action = 'revert'
        if action == 'revert':
            self.planetary_name = self.player.get_planetary_minister(self.planetary___uuid__).name
            for key in PlanetaryMinister.defaults:
                setattr(self, 'planetary_' + key, getattr(self.player.get_planetary_minister(self.planetary___uuid__), key))
            self.planetary_facility_types[0] = self.planetary_power_plants
            self.planetary_facility_types[1] = self.planetary_factories + self.planetary_facility_types[0]
            self.planetary_facility_types[2] = self.planetary_mines + self.planetary_facility_types[1]
        #for minister in self.player.planetary_ministers:
        #    print('minister  = ', minister.__dict__)
        #print('self  = ', self.__dict__)
        """ set the new colony minister. """
        if self.planetary_new_col_minister == '':
            for minister in self.player.planetary_ministers:
                if minister.new_colony_minister:
                    self.planetary_new_col_minister = minister.name
        for minister in self.player.planetary_ministers:
            minister.new_colony_minister = False
            if minister.name == self.planetary_new_col_minister:
                minister.new_colony_minister = True
        """ save """
        self.planetary_power_plants = self.planetary_facility_types[0]
        self.planetary_factories = self.planetary_facility_types[1]-self.planetary_facility_types[0]
        self.planetary_mines = self.planetary_facility_types[2]-self.planetary_facility_types[1]
        self.planetary_defenses = 100-self.planetary_facility_types[2]
        for key in PlanetaryMinister.defaults:
            setattr(self.player.get_planetary_minister(self.planetary___uuid__), key, getattr(self, 'planetary_' + key))
        for planet in self.player.planetary_minister_map:
            self.player.planetary_minister_map[planet] = getattr(self, 'planetary_' + planet + '_minister')
        """ set display values """
        for minister in self.player.planetary_ministers:
            self.options_planetary_new_col_minister.append(minister.name)
        self.planetary_power = str(self.planetary_power_plants) + ' %'
        self.planetary_factory = str(self.planetary_factories) + ' %'
        self.planetary_mine = str(self.planetary_mines) + ' %'
        self.planetary_shield = str(self.planetary_defenses) + ' %'
        for planet in self.player.planetary_minister_map:
            setattr(self, 'options_planetary_' + planet + '_minister', self.option_planetary_new_col_minister)
            self.planetary_planets.append('<td>' + planet + '<select id="planetary_' + planet + '_minister" style="width: 100%" onchange="post(\'planetary_minister\')"/></td>')
        self.planetary_sidebar.append('<td><img class="button" title="ministers" src="/planetary_minister.png" onclick="show_screen(\'planetary_ministers\')"/></td>')
        for minister in self.player.planetary_ministers:
            self.planetary_sidebar.append('<td><img class="button" title="' + minister.name + '" style="background: ' + minister.color + '" src="/planetary_minister.png" onclick="show_minister(\'uuid=' + minister.__uuid__ + '\')"/></td>')
        self.planetary_sidebar.append('<td><i class="button fas fa-plus-circle" title="new minister" onclick="show_minister(\'new\')"></i></td>')
    

for key in PlanetaryMinister.defaults:
    __defaults['planetary_' + key] = PlanetaryMinister.defaults[key]

PlanetaryMinisters.set_defaults(PlanetaryMinisters, __defaults, sparse_json=False)