from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class EnergyMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        


EnergyMinister.set_defaults(EnergyMinister, __defaults, sparse_json=False)
