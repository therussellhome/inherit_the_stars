from .planet import Planet
from colorsys import hls_to_rgb

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
      
    """ Get the suns color """
    # return it in a hexdecimal string so the webpage can use it
    def get_color(self):
        t = (min(100, max(0, self.temperature)) / 100) * .7
        r = .5 + (min(100, max(0, self.radiation)) * .005)
        color = hls_to_rgb(t, .75, r)
        color_string = '#' + format(int(color[0] * 255), 'X') + format(int(color[1] * 255), 'X') + format(int(color[2] * 255), 'X') 
        return color_string

    """ Only Pa'anuri are allowed to colonize suns """
    def colonize(self, player, minister, population, factories):
        if player.race.primary_race_trait != 'Pa\'anuri':
            return
        super().colonize(player, minister, population, 0)

Sun.set_defaults(Sun, __defaults)
