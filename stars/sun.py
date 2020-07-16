from .planet import Planet


""" Default values (default, min, max)  """
__defaults = {
    'distance': [0, 0, 0],
    'power_plants': [0, 0, 0],
    'factories': [0, 0, 0],
    'mines': [0, 0, 0],
    'defense': [0, 0, 0],
}


""" The sun at the center of the system """
class Sun(Planet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Only Pa'anuri are allowed to colonize suns """
    def colonize(self, player, minister, population, factories):
        if player.race.primary_race_trait != 'Pa\'anuri':
            return
        super().colonize(player, minister, population, 0)

Sun.set_defaults(Sun, __defaults)
