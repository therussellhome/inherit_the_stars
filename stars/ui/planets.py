from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'planets_filters': [[]],
    'planets_filter': ['My Planets']
    'options_planets_filter': [[]],
    'planets_report': [[]],
    'options_planets_field': [[]],
    'planets_field': ['Habitability']
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
        fields = ['Habitability', 'Capacity', 'Population', 'Max Population', 'Energy Generation', 'Production Capacity', 'Scanner Range', 'Shield Coverage', 'Mineral Output', 'Mineral Availability']
        b = ''
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
                

Planets.set_defaults(Planets, __defaults, sparse_json=False)
# TODO get comparasion field working
# TODO click on the planet name and it shows everything else
