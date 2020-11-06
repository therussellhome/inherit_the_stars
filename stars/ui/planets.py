from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Planets(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass
    def p(self)
        planets = []
        for p in self.player.get_intel('Planet'):
            planets.append(p)
        for s in self.player.get_intel('Sun')
            planet.append(s)
        for p in planets:
            self.planets_report.append('<td>' + p.get('name') + '</td><td>100,000</td>')

Planets.set_defaults(Planets, __defaults, no_reset=[])
