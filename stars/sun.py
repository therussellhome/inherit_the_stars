from colorsys import hls_to_rgb
from .minerals import Minerals
from .planet import Planet


""" Default values (default, min, max)  """
__defaults = {
    'distance': (0, 0, 0),
}


""" The sun at the center of the system """
class Sun(Planet):
    """ Get the suns color """
    # return it in a hexdecimal string so the webpage can use it
    def get_color(self):
        t = (min(100, max(0, self.temperature)) / 100) * .7
        r = .5 + (min(100, max(0, self.radiation)) * .005)
        color = hls_to_rgb(t, .75, r)
        color_string = '#' + format(round(color[0] * 255), '02X') + format(round(color[1] * 255), '02X') + format(round(color[2] * 255), '02X') 
        return color_string

    """ Cannot mine a sun """
    def extract_minerals(self, orbital=False):
        return Minerals()

Sun.set_defaults(Sun, __defaults)
