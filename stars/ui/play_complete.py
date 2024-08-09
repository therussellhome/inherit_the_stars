import sys
from .playerui import PlayerUI
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'player_ready': False,
}


""" """
class PlayComplete(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        if action == 'refresh':
            self.player_ready = not self.player.ready_to_generate
        elif action == 'save':
            self.player.save()
        elif action != 'reset':
            self.player.ready_to_generate = True
            self.player.save()
            filename = self.player.filename()
            game_engine.unregister()
            game = game_engine.load('Game', self.player.game_ID)
            game.update_players()
            if game.is_ready_to_generate():
                game.new_turn()
            # Reload the player file
            game_engine.unregister()
            p = game_engine.load('Player', filename)
            # Set the player object to autosave
            game_engine.set_root_obj(p)
            self.player_token = str(id(p))
            self.player_ready = True


PlayComplete.set_defaults(PlayComplete, __defaults, sparse_json=False)
