import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'energy': [0, 0, sys.maxsize],
    'weapons': [0, 0, sys.maxsize],
    'propulsion': [0, 0, sys.maxsize],
    'construction': [0, 0, sys.maxsize],
    'electronics': [0, 0, sys.maxsize],
    'biotechnology': [0, 0, sys.maxsize]
}

""" Represent 'tech level' """
class TechLevel(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Determine if the item is available for a player's tech level """
    def is_available(self, level):
        if level.energy >= self.energy and level.weapons >= self.weapons and level.propulsion >= self.propulsion and level.construction >= self.construction and level.electronics >= self.electronics and level.biotechnology >= self.biotechnology:
            return True
        return False

    def __add__(self, other):
        t = TechLevel()
        t.energy = max(self.energy, other.energy)
        t.weapons = max(self.weapons, other.weapons)
        t.propulsion = max(self.propulsion, other.propulsion)
        t.construction = max(self.construction, other.construction)
        t.electronics = max(self.electronics, other.electronics)
        t.biotechnology = max(self.biotechnology, other.biotechnology)
        return t

    """
    Cost in YJ to attain this level
    race (Race object) used for research modifiers
    level (TechLevel object) current levels for the player
    partial (TechLevel object) energy spent on next levels
    """
    def calc_cost(self, race, level, partial):
        cost = 0
        for field in ['energy', 'weapons', 'propulsion', 'construction', 'electronics', 'biotechnology']:
            cost_field = 0
            for i in range(getattr(level, field) + 1, getattr(self, field) + 1):
                cost_field += getattr(race, 'research_modifier_' + field) * (10 + i ** 3)
            cost += max(0, cost_field - getattr(partial, field))
        return cost

    """ Format the tech level for HTML """
    def to_html(self, show_zero=False):
        html = ''
        if self.energy > 0 or show_zero:
            html += '<i class="fa-react" title="Energy"> ' + str(self.energy) + '</i>'
        if self.weapons> 0 or show_zero:
            html += '<i class="fa-bomb" title="Weapons"> ' + str(self.weapons) + '</i>'
        if self.propulsion > 0 or show_zero:
            html += '<i class="fa-tachometer-alt" title="Propulsion"> ' + str(self.propulsion) + '</i>'
        if self.construction > 0 or show_zero:
            html += '<i class="fa-wrench" title="Construction"> ' + str(self.construction) + '</i>'
        if self.electronics > 0 or show_zero:
            html += '<i class="fa-plug" title="Electronics"> ' + str(self.electronics) + '</i>'
        if self.biotechnology > 0 or show_zero:
            html += '<i class="fa-seedling" title="Biotechnology"> ' + str(self.biotechnology) + '</i>'
        return html

TechLevel.set_defaults(TechLevel, __defaults)
