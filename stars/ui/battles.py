from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Battles(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


Battles.set_defaults(Battles, __defaults)
