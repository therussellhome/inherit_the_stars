from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Settings(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


Settings.set_defaults(Settings, __defaults, sparse_json=False)
