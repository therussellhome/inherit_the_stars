from .. import game_engine
from ..defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    'systems': [[]],
    'planets': [[]],
    'ships': [[]],
    # Shared with other forms and used to identify player
    'player_token': [''],
}


""" Represent Open Game action """
class RenderStars(Defaults):
    """ Interact with UI """
    def post(self, action):
        # Always reset to default
        self.reset_to_default()
        # Copy all systems
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
        # Get the player's intel
        games = game_engine.get('Game')
        if len(games) > 0:
            for p in games[0].players:
                if self.player_token == str(id(p)):
                    print('TODO')
                    # do stuff
            

RenderStars.set_defaults(RenderStars, __defaults)
