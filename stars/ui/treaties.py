from ..defaults import Defaults
from .. import game_engine
from sys import maxsize

__defaults = {
    'p1': [[]],
    'p2': [[]],
    'relation': [['nutral']],
    'options_relation': [['team', 'nutral', 'enemy']],
    'cost_p1_to_p2_titanium': [100, 0, maxsize],
    'p1_is_selling_titanium': [False],
    'cost_p2_to_p1_titanium': [100, 0, maxsize],
    'p2_is_selling_titanium': [False],
    'cost_p1_to_p2_silicon': [100, 0, maxsize],
    'p1_is_selling_silicon': [False],
    'cost_p2_to_p1_silicon': [100, 0, maxsize],
    'p2_is_selling_silicon': [False],
    'cost_p1_to_p2_lithium': [100, 0, maxsize],
    'p1_is_selling_lithium': [False],
    'cost_p2_to_p1_lithium': [100, 0, maxsize],
    'p2_is_selling_lithium': [False],
    'cost_p1_to_p2_fuel': [100, 0, maxsize],
    'p1_is_selling_fuel': [False],
    'cost_p2_to_p1_fuel': [100, 0, maxsize],
    'p2_is_selling_fuel': [False],
    'cost_p1_to_p2_stargate': [5000, 0, maxsize],
    'p1_is_selling_stargate': [False],
    'cost_p2_to_p1_stargate': [5000, 0, maxsize],
    'p2_is_selling_stargate': [False],
    'shared_p1_planet_report': [False],
    'shared_p1_scanner_report_of_enemies': [False],
    'shared_p1_scanner_report_of_nutals': [False],
    'shared_p1_scanner_report_of_teammates': [False],
    'shared_p1_scanner_report_of_intersteler_objects': [False],
    'shared_p1_fleet_reports': [False],
    'shared_p1_knowlage_of_hiper_dinile_and_system_defence': [False],
    'shared_p1_passcode_for_hiper_dinile': [False],
    'shared_p1_passcode_for_system_defence': [False],
    'shared_p2_planet_report': [False],
    'shared_p2_scanner_report_of_enemies': [False],
    'shared_p2_scanner_report_of_nutals': [False],
    'shared_p2_scanner_report_of_teammates': [False],
    'shared_p2_scanner_report_of_unowned_things': [False],
    'shared_p2_fleet_reports': [False],
    'shared_p2_knowlage_of_hiper_dinile_and_system_defence': [False],
    'shared_p2_passcode_for_hiper_dinile': [False],
    'shared_p2_passcode_for_system_defence': [False],
}

class Treaty(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def post(self, action):
        if action == 'revoc':
            self.relation = 'enemy'
        if action == 'propose':
            game_engine.send_message(self.p1, self.p2, 'do you except ' + p1.name + '\'s treaty proposal?')
        if self.relation == 'enemy':
            for key in self.__dict__:
                self.__dict__[key] = False
        pass

Treaty.set_defaults(Treaty, __defaults)
