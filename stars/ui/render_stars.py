from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'suns': [[]],
    'planets': [[]],
    'ships': [[]],
}


""" Represent Open Game action """
class RenderStars(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        # Copy all suns
        self.suns = []
        self.plants = []
        for s in self.player().get_intel('Sun'):
            self.suns.append({
                'name': s.get('name'), 
                'x': s.get('location').x,
                'y': s.get('location').y,
                'z': s.get('location').z,
                'color': s.get('color'),
                'size': s.get('size'),
            })
        for s in self.player().get_intel('Planets'):
            self.planets.append({
                'name': s.get('name'), 
                'x': s.get('location').x,
                'y': s.get('location').y,
                'z': s.get('location').z,
                'color': s.get('color'),
                'size': s.get('size'),
            })
        print(len(self.suns))
        print(len(self.planets))

RenderStars.set_defaults(RenderStars, __defaults, sparse_json=False)
