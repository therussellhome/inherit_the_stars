from .build_queue import BuildQueue


""" Default values (default, min, max)  """
__defaults = {
    'hab': '', # habitability type
}


""" Temporary class to indicate terraforming in progress """
class Terraform(BuildQueue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        base = 2500
        if self.planet.player.race.lrt_Bioengineer:
            base = 1800
        self.cost.energy = base * (1 + self.planet[self.hab + '_terraform']) ** 1.25

    """ Mark the item as completed """
    def finish(self):
        self.planet[self.hab + '_terraform'] += 1


Terraform.set_defaults(Terraform, __defaults)
