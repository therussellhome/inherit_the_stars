from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Fleets(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


Fleets.set_defaults(Fleets, __defaults, sparse_json=False)
