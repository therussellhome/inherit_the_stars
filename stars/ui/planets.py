from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'planets_filters': [[]],
    'planets_filter': ['My Planets']
    'planets_report': [[]],
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
        b = ''
        for f in filters:
            s = '<option>' + f + '</option>'
            if f == planets_filter:
                s = '<option selected="true">' + f + '</option>'
            b += s
        self.planets_filters.append('<td class="hfill">Filter<select id="planets_filter" style="width: 100%" onchange="post(\'planets\')"/>' + b + '</td>')

        # Fields for comparasion
        fields = ['Habitability', 'Capacity', 'Population', 'Max Population', 'Energy Generation', 'Production Capacity', 'Scanner Range', 'Shield Coverage', 'Mineral Output', 'Mineral Availability']
        b = ''
        for f in fields:
            s = '<option>' + f + '</option>'
            if f == planets_field:
                s = '<option selected="true">' + f + '</option>'
            b += s
        self.planets_report.append('<td class="hfill">Field<select id="planets_field" style="width: 100%" onchange="post(\'planets\')"/>' + b + '</td>')
        
        # Get planets
        planets = []
        for p in self.player.get_intel('Planet'):
            planets.append(p)
        for s in self.player.get_intel('Sun')
            planet.append(s)
        for p in planets:
            # TODO Sort planets
            self.planets_report.append('<td>' + p.get('name') + '</td><td>100,000</td>') 

Planets.set_defaults(Planets, __defaults, sparse_json=False)

# TODO get comparasion field working, TODO sort planets, TODO click on the planet name and it shows everything else
