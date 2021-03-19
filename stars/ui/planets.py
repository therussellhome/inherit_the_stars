from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'options_planets_filter': [],
    'planets_filter': 'My Planets',
    'planets_report': [],
    'options_planets_field': [],
    'planets_field': 'Habitability',
}


""" """
class Planets(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return

        # Planets filter
        filters = ['My Planets', 'Team planets', 'Neutral Planets', 'Enemy Planets', 'Uninhabited Planets', 'All Planets', 'All Suns', 'All Planets & Suns']
        for f in filters:
            self.options_planets_filter.append(f)

        # Fields for comparasion
        fields = ['Habitability', 'Capacity', 'Population', 'Max Population', 'Energy Generation', 'Production Capacity', 'Scanner Range', 'Shield Coverage', \
        'Mineral Output', 'Mineral Availability']
        for f in fields:
            self.options_planets_field.append(f)
        
        # Checks to see whether it has to calculate it 
        # It's using cache so it doesn't have to calculate the report over and over again
        if 'planet_report' not in self.player().__cache__:
            planets = []
            for (r, p) in self.player().get_intel(by_type='Planet').items():
                # Gets and sorts planets
                planet = {'name': p.name}
                if not hasattr(p, 'player'):
                    planet['Uninhabited Planets'] = True
                else:
                    relation = self.player().get_relation(hasattr(p, player))
                    if relation == 'me':
                        planet['My Planets'] = True
                    elif relation == 'team':
                        planet['Team Planets'] = True
                    elif relation == 'neutral':
                        planet['Neutral Planets'] = True
                    elif relation == 'enemy':
                        planet['Enemy Planets'] = True
                planet['date'] = p.date
                if r: 
                    planet['Habitability'] = r.habitability
                    planet['Population'] = r.population()
                    planet['Capacity'] = r.capacity
                    planet['Max Population'] = r.max_pop 
                    planet['Energy Generation'] = '<i class="YJ">' + str(r.generate_energy() * 100) + '</i>'
                    planet['Production Capacity'] = str(r.operate_factories() * 100)
                    planet['Scanner Range'] = str(r.scanning_penetrating()) + '/' + str(r.scanning_normal())
                    planet['Shield Coverage'] = str(r.raise_shields())
                    planet['Mineral Output'] = str(r.mine_minerals() * 100)
                    planet['Mineral Availability'] = r.mineral_availability
                else:
                    planet['Energy Generation'] = '?'
                    planet['Production Capacity'] = '?'
                    planet['Scanner Range'] = '?'
                    planet['Shield Coverage'] = '?'
                    planet['Mineral Output'] = '?'
                    planet['Habitability'] = getattr(p, 'habitability', '?')
                    planet['Population'] = getattr(p, 'population', '?')
                    planet['Capacity'] = getattr(p, 'capacity', '?')
                    planet['Max Population'] = getattr(p, 'max_pop', '?')
                    planet['Mineral Availability'] = getattr(p, 'mineral_availability', '?')
                planets.append(planet)
            # Puts the report in the cache
            self.player().__cache__['planet_report'] = planets
        else:
            planets = self.player().__cache__['planet_report']
            
        for p in planets:
            if p.get(self.planets_filter, False):
                self.planets_report.append('<td>' + p['name'] + '</td><td>' + p[self.planets_field] + '</td><td>' + p['date'] + '</td>')
        print(planets)
        print(self.planets_report)

Planets.set_defaults(Planets, __defaults, sparse_json=False)
# TODO get comparasion field working
# TODO click on the planet name and it shows everything else
