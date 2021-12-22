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
        if not self.player:
            return

        # Planets filter
        filters = ['My Planets', 'Team planets', 'Neutral Planets', 'Enemy Planets', 'Uninhabited Planets', 'All Planets', 'All Suns']
        for f in filters:
            self.options_planets_filter.append(f)

        # Fields for comparasion
        fields = ['Habitability', 'Capacity', 'Population', 'Max Population', 'Energy Generation', 'Production Capacity', 'Scanner Range', 'Shield Coverage', \
        'Mineral Output', 'Mineral Availability']
        for f in fields:
            self.options_planets_field.append(f)
        
        # Checks to see whether it has to calculate it 
        # It's using cache so it doesn't have to calculate the report over and over again
        if len(self.player.planet_report) == 0:
            planets = [] 
            for (r, p) in self.player.get_intel(by_type='Planet').items():
                planet = {'name': p.name, 'details': ''}
                planet['date'] = p.date
                if r: 
                    planet['Habitability'] = r.habitability
                    planet['Population'] = r.population
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
                planet['details'] += '<tr><td>Habitability</td><td>' + planet['Habitability'] + '</td></tr>'
                planet['details'] += '<tr><td>Population</td><td>' + planet['Population'] + '</td></tr>'
                planet['details'] += '<tr><td>Capacity</td><td>' + planet['Capacity'] + '</td></tr>'
                planet['details'] += '<tr><td>Max Population</td><td>' + planet['Max Population'] + '</td></tr>'
                planet['details'] += '<tr><td>Energy Generation</td><td>' + planet['Energy Generation'] + '</td></tr>'
                planet['details'] += '<tr><td>Production Capacity</td><td>' + planet['Production Capacity'] + '</td></tr>'
                planet['details'] += '<tr><td>Scanner Range</td><td>' + planet['Scanner Range'] + '</td></tr>'
                planet['details'] += '<tr><td>Shield Coverage</td><td>' + planet['Shield Coverage'] + '</td></tr>'
                planet['details'] += '<tr><td>Mineral Output</td><td>' + planet['Mineral Output'] + '</td></tr>'
                planet['details'] += '<tr><td>Mineral Availability</td><td>' + planet['Mineral Availability'] + '</td></tr>'
                planets.append(planet)
            # Puts the report in the cache
            self.player.planet_report = planets
        else:
            planets = self.player.planet_report
            
        for p in planets:
            if p.get(self.planets_filter, False):
                self.planets_report.append('<td>' + p['name'] + '</td><td>' + p[self.planets_field] + '</td><td>' + p['date'] + \
                '</td><td><div class="fa-angle-double-up" onclick="toggle(this.parentElement, \'collapse\')"></div>')
                self.planets_report.append('<td colspan="4"><table class="hfill">' + p['details'] + '</table></td>')
        print(planets)
        print(self.planets_report)

    def sort_planets(self, planet):
        for (r, p) in self.player.get_intel(by_type='Planet').items():
            # Gets and sorts planets
            planet['All Planets'] = True
            if not hasattr(p, 'player'):
                planet['Uninhabited Planets'] = True
            else:
                relation = self.player.get_relation(hasattr(p, player))
                if relation == 'me':
                    planet['My Planets'] = True
                elif relation == 'team':
                    planet['Team Planets'] = True
                elif relation == 'neutral':
                    planet['Neutral Planets'] = True
                elif relation == 'enemy':
                    planet['Enemy Planets'] = True
        for (r, p) in self.player.get_intel(by_type='Sun').items():
            # Gets and sorts planets
            planet = {'name': p.name, 'details': ''}
            planet['All Suns'] = True
            if not hasattr(p, 'player'):
                planet['Uninhabited Planets'] = True
            else:
                relation = self.player.get_relation(hasattr(p, player))
                if relation == 'me':
                    planet['My Planets'] = True
                elif relation == 'team':
                    planet['Team Planets'] = True
                elif relation == 'neutral':
                    planet['Neutral Planets'] = True
                elif relation == 'enemy':
                    planet['Enemy Planets'] = True

Planets.set_defaults(Planets, __defaults, sparse_json=False)
