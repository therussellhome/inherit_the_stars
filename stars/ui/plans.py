from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Plans(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


Plans.set_defaults(Plans, __defaults, sparse_json=False)
