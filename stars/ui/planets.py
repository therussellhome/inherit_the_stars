from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Planets(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        planets = []
        for p in self.player.get_intel('Planet'):
            planets.append(p)
        for s in self.player.get_intel('Sun')
            planet.append(s)
        for p in planets:
            self.planets_report.append('<td>' + p.get('name') + '</td><td>100,000</td>')

Planets.set_defaults(Planets, __defaults, sparse_json=False)
