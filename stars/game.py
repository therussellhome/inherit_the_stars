import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'name': [''],
    'players': [[]],
    'autogen_turn': [True],
    'date': [3000, 0, sys.maxsize]
}


""" Class defining a game and everything in it """
class Game(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)

    """ Generate a turn """
    def generate_turn(self):
        fleets = game_engine.get('Fleet/')
        fleets.sort(key=lambda x: x.initiative, reverse=True)
        game_engine.hyper_denials = []
        # Execute fleet preactions
        for preaction in Fleet.preactions:
            for fleet in fleets:
                fleet.execute(preaction)
        # TODO anomolies & mystery trader
        # Movment and scaning in hundredths of a turn
        for time_in in range(100):
            # Fleet movement in initiative order
            for fleet in reversed(fleets):
                fleet.move(time_in/100)
            # Mineral packet movement
            for packet in game_engine.get('MineralPacket/'):
                packet.move()
            # Update scanning
            for planet in game_engine.get('Planet/'):
                planet.calculate_scanning()
            for station in game_engine.get('SpaceStation/'):
                station.calculate_scanning()
            for fleet in fleets:
                fleet.calculate_scanning()
            for packet in game_engine.get('MineralPackets/'):
                packet.calculate_scanning()
        # Player build/research/other economic funcitions
        for player in game_engine.get('Player/'):
            player.manage_economy()
        # Execute combat
        for system in game_engine.get('StarSystem/'):
            system.combat()
        # Execute fleet actions in action order and reverse initiativve
        for action in Fleet.actions:
            for fleet in fleets:
                fleet.execute(action)


Game.set_defaults(Game, __defaults)
