from .build_queue import BuildQueue


""" Default values (default, min, max)  """
__defaults = {
    'hab': '', # habitability type
}


""" Temporary class to indicate terraforming in process """
class Terraform(BuildQueue):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        base = 5000
        if self.planet.player.race.lrt_Bioengineer:
            base = 3500
        self.cost.energy = base * (1 + self.planet[hab + '_terraform']) ** 1.5 #TODO Pam, please balance this

    """ Mark the item as completed """
    def finish(self):
        self.planet[self.hab + '_terraform'] += 1


Terraform.set_defaults(Terraform, __defaults)
