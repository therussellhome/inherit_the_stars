from .planet import Planet


""" Default values (default, min, max)  """
__defaults = {
    'distance': [0, 0, 0]
}


""" TODO """
class Sun(Planet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Sun.set_defaults(Sun, __defaults)
