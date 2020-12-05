from .buildable import Buildable


""" Default values (default, min, max)  """
__defaults = {
    'hab': [''],
}


""" Temporary class to indicate terraforming in process """
class Terraform(Buildable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Return the cost to build """
    def add_to_build_queue(self, planet, upgrade_to=None):
        super().add_to_build_queue(planet, upgrade_to)
        base = 5000
        if planet.player.race.lrt_Bioengineer:
            base = 3500
        return Cost(energy=base * (1 + planet[hab + '_terraform']) ** 1.5) #TODO Pam, please balance this

    """ Mark the item as completed """
    def build_complete(self, planet, upgrade_to=None):
        super().build_complete(planet, upgrade_to)
        planet[self.hab + '_terraform'] += 1


Terraform.set_defaults(Terraform, __defaults)
