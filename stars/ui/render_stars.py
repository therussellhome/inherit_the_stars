from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'systems': [[]],
    'planets': [[]],
    'ships': [[]],
}


""" Represent Open Game action """
class RenderStars(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            print('no player')
            return
        # Copy all systems
        self.systems = []
        for s in self.player.get_intel('Sun'):
            self.systems.append({
                'name': s.get('name'), 
                'x': s.get('location').x,
                'y': s.get('location').y,
                'z': s.get('location').z,
                'color': s.get('color'),
                'size': s.get('size'),
            })
            

RenderStars.set_defaults(RenderStars, __defaults)
