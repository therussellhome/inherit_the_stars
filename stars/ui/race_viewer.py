from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class RaceViewer(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


RaceViewer.set_defaults(RaceViewer, __defaults)
