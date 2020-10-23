from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'systems': [[]],
    'planets': [[]],
    'ships': [[]],
    # Shared with other forms and used to identify player
    'player_token': [''],
}


""" Represent Open Game action """
class RenderStars(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        # Copy all systems
        self.systems = []
        return #TODO get from player object
        for s in game_engine.get('StarSystem'):
            self.systems.append({
                'name': s.name, 
                'x': s.location.x,
                'y': s.location.y,
                'z': s.location.z,
                'color': s.planets[0].get_color(),
                'size': s.planets[0].gravity,
            })
            print(s.name, s.planets[0].temperature, s.planets[0].get_color())
            

RenderStars.set_defaults(RenderStars, __defaults)
