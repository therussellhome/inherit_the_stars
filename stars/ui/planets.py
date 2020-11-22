from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Planets(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


Planets.set_defaults(Planets, __defaults)
