import sys
from math import ceil
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'energy': (0, 0, sys.maxsize),
    'weapons': (0, 0, sys.maxsize),
    'propulsion': (0, 0, sys.maxsize),
    'construction': (0, 0, sys.maxsize),
    'electronics': (0, 0, sys.maxsize),
    'biotechnology': (0, 0, sys.maxsize),
}


""" List of tech fields """
TECH_FIELDS = ['energy', 'weapons', 'propulsion', 'construction', 'electronics', 'biotechnology']


""" Represent 'tech level' """
class TechLevel(Defaults):
    """ Determine if the item is available for a player's tech level """
    def is_available(self, level):
        for field in TECH_FIELDS:
            if self[field] > level[field]:
                return False
        return True

    """ Add uses the greater of the inputs by field """
    def __add__(self, other):
        t = TechLevel()
        for field in TECH_FIELDS:
            t[field] = max(self[field], other[field])
        return t

    """ Greater than in any field """
    def __gt__(self, other):
        for field in TECH_FIELDS:
            if self[field] > other[field]:
                return True
        return False

    """ Calculate cost for an increase in a given field """
    def cost_for_next_level(self, field, race, increase=1):
        cost = 0
        for i in range(self[field] + 1, self[field] + 1 + increase):
            cost += race['research_modifier_' + field] * (10 + i ** 3)
        return cost

    """
    Calculate the most expesive field in YJ to attain this level and the Tech with which it is associated
    race (Race object) used for research modifiers
    level (TechLevel object) current levels for the player
    partial (TechLevel object) energy spent on next levels
    " ""
    def most_expensive_field(self, race, level, partial):
        cost = {}
        max_field = 'energy'
        max_cost = -1
        for field in TECH_FIELDS:
            increase = max(0, self[field] - level[field])
            cost = max(0, level.cost_for_next_level(field, race, increase) - partial[field])
            if cost > max_cost:
                max_field = field
                max_cost = cost
        return max_field
        #"""
    
    """
    Cost in YJ to attain this level
    race (Race object) used for research modifiers
    level (TechLevel object) current levels for the player
    partial (TechLevel object) energy spent on next levels
    """
    def calc_cost(self, race, level, partial):
        cost = 0
        for field in TECH_FIELDS:
            increase = max(0, self[field] - level[field])
            cost += max(0, level.cost_for_next_level(field, race, increase) - partial[field])
        return cost

    """ Sum of levels """
    def total_levels(self):
        levels = 0
        for field in TECH_FIELDS:
            levels += self[field]
        return levels

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
