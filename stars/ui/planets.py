from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
<<<<<<< HEAD
    'planets_filters': [[]],
    'planets_filter': ['My Planets']
    'options_planets_filter': [[]],
    'planets_display': [[]],
    'planets_report': [[]],
    'options_planets_field': [[]],
    'planets_field': ['Habitability']
=======
    'planets_filters': [],
    'planets_filter': 'My Planets',
    'planets_report': [],
    'planets_field': 'Habitability',
>>>>>>> 73144c9d60dfb3d00495bc2d59ad7c961c30cf1a
}


""" """
class Planets(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return

        # Planets filter
        filters = ['My Planets', 'Team planets', 'Neutral Planets', 'Enemy Planets', 'Uninhabited Planets', 'All Planets', 'All Suns', 'All Planets &amp; Suns']
        for f in filters:
            self.options_planets_filter.append(f)
        self.planets_filters.append('<td class="hfill">Filter<select id="planets_filter" style="width: 100%" onchange="post(\'planets\')"></select>')

        # Fields for comparasion
        fields = ['Habitability', 'Capacity', 'Population', 'Max Population', 'Energy Generation', 'Production Capacity', 'Scanner Range', 'Shield Coverage', \
        'Mineral Output', 'Mineral Availability']
        for f in fields:
            self.options_planets_field.append(f)
        self.planets_report.append('<td class="hfill">Field<select id="planets_field" style="width: 100%" onchange="post(\'planets\')"/></td>')
        
        # Get planets
        suns = []
        planets = []
        ps = []
        for p in self.player.get_intel('Planet'):
            planets.append(p)

            ps.append(p)
        # Get suns
        for s in self.player.get_intel('Sun'):
            suns.append(s)
            ps.append(s)

        # Sort the planets and suns
        mine = []
        team = []
        neutral = []
        enemy = []
        uninhabited = []
        relation = self.player().get_relation(p.player)
        for p in ps:
            self.planets_report.append('<td>' + p.get('name') + '</td><td>100,000</td>')
            if not p.is_colonized:
                uninhabited.append(p)
            if p.is_colonized:
                if relation == 'me'
                    mine.append(p)
                if relation == 'team':
                    team.append(p)
                if relation == 'neutral':
                    neutral.append(p)
                if relation == 'enemy':
                    enemy.append(p)
        
        # Checks to see whether it has to calculate it 
        # It's using cache so it doesn't have to calculate the report over and over again
        if 'planet_report' not in self.player().__cache__:
            planets = []
            for (r, p) in self.player().get_intel(by_type='Planet').items():
                planet = {'name': p.name}
                relation = self.player().get_relation(p.player)
                if relation == 'me':
                    planet['My Planets'] = True
                elif relation == 'team':
                    planet['Team Planets'] = True
                elif relation == 'neutral':
                    planet['Neutral Planets'] = True
                elif relation == 'enemy':
                    planet['Enemy Planets'] = True
                elif not p.is_colonized:
                    planet['Uninhabited Planets'] = True
                planet['date'] = p.date
                planet['Habitability'] = p.habitability
                # Calculates all the things that the player only knows if it is their planet
                if r:
                    planet['Energy Generation'] = '<i class="YJ">' + str(r.generate_energy() * 100) + '</i>'
                    planet['Production Capacity'] = str(r.operate_factories() * 100)
                    planet['Scanner Range'] = str(r.scanning_penetrating()) + '/' + str(r.scanning_normal())
                    planet['Shield Coverage'] = str(r.raise_shields())
                    planet['Mineral Output'] = str(r.mine_minerals() * 100)
                else:
                    planet['Energy Generation'] = '?'
                    planet['Production Capacity'] = '?'
                    planet['Scanner Range'] = '?'
                    planet['Shield Coverage'] = '?'
                    planet['Mineral Output'] = '?'
                # Sets other fields
                planet['Population'] = p.population()
                planet['Capacity'] = p.capacity()
                planet['Max Population'] = p.max_pop 
                planet['Mineral Availability'] = p.mineral_availability
                planets.append(planet)
            # Puts the report in the cache
            self.player().__cache__['planet_report'] = planets
            else:
                planets = self.player().__cache__['planet_report']
            
        for p in planets:
            if p.get(self.planets_filter, False):
                self.planets_report.append('<td>' + p['name'] + '</td><td>' + p[self.planets_field] + '</td><td>' + p['date'] + '</td>')

Planets.set_defaults(Planets, __defaults, sparse_json=False)
# TODO get comparasion field working
# TODO click on the planet name and it shows everything else
