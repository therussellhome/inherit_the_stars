from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class PlanetaryMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


PlanetaryMinister.set_defaults(PlanetaryMinister, __defaults)
