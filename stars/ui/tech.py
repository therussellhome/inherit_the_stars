import sys
from .playerui import PlayerUI
from .. import game_engine
from .. import stars_math
from ..race import Race
from ..scanner import Scanner
from ..tech import Tech as StarsTech
from ..tech_level import TechLevel

__defaults = {
    'overview': {},
    'combat': {}, # power over range (computed for 0..99)
    'sensor': {}, # visability over range (standard, penetrating, anti-cloak, self-cloak)
    'engine': {}, # tacometer over hyper (computed for 1..10)
    'guts': {},

#    'apparent_mass': [0, 0, sys.maxsize],
}

""" Display information about a tech item or ship design """
class Tech(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        tech_tree = game_engine.get('Tech')
        if self.player:
            player_race = self.player.race
            player_level = self.player.tech_level
            player_partial = self.player.research_partial
            tech_tree = self.player.tech
        else:
            if len(tech_tree) < 10:
                tech_tree = game_engine.load('Tech', 'Inherit the Stars!')
            player_race = Race()
            player_level = TechLevel()
            player_partial = TechLevel()
        for tech in tech_tree:
            self.overview[tech.ID] = tech.html_overview(player_race, player_level, player_partial)
            combat = tech.html_combat()
            if combat:
                self.combat[tech.ID] = combat
            sensor = tech.html_sensor()
            if sensor:
                self.sensor[tech.ID] = sensor
            engine = tech.html_engine()
            if engine:
                self.engine[tech.ID] = engine
            self.guts[tech.ID] = tech.html_guts()


Tech.set_defaults(Tech, __defaults, sparse_json=False)
