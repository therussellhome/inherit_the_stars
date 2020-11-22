from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Generate(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


Generate.set_defaults(Generate, __defaults)
