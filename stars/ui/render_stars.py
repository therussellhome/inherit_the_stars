from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'systems': [],
    'planets': [],
    'ships': [],
}


""" Represent Open Game action """
class RenderStars(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        # Copy all suns
        self.systems = []
        self.plants = []
        self.ships = []
        for (s, i) in self.player().get_intel(by_type='StarSystem').items():
            self.systems.append(i)
        for (p, i) in self.player().get_intel(by_type='Planet').items():
            self.planets.append(i)
        for (s, i) in self.player().get_intel(by_type='Ship').items():
            self.ships.append(i)


RenderStars.set_defaults(RenderStars, __defaults, sparse_json=False)
