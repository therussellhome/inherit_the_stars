from defaults import Defaults

__defaults = {
    'p1': [[]]
    'p2': [[]]
    'relation': [['enemy']]
    'options_relation': [['team', 'nutal', 'enemy']]
    'coust_p1_to_p2_titanium': [100, 0, maxsize],
    'p1_is_selling_titanium': [False],
    'coust_p2_to_p1_titanium': [100, 0, maxsize],
    'p2_is_selling_titanium': [False],
    'coust_p1_to_p2_silicon': [100, 0, maxsize],
    'p1_is_selling_silicon': [False],
    'coust_p2_to_p1_silicon': [100, 0, maxsize],
    'p2_is_selling_silicon': [False],
    'coust_p1_to_p2_lithium': [100, 0, maxsize],
    'p1_is_selling_lithium': [False],
    'coust_p2_to_p1_lithium': [100, 0, maxsize],
    'p2_is_selling_lithium': [False],
    'coust_p1_to_p2_fuel': [100, 0, maxsize],
    'p1_is_selling_fuel': [False],
    'coust_p2_to_p1_fuel': [100, 0, maxsize],
    'p2_is_selling_fuel': [False],
    'charge_p1_to_p2_for_stargating': [5000, 0, maxsize],
    'p2_can_use_p1\'s_stargates': [False],
    'charge_p2_to_p1_for_stargating': [5000, 0, maxsize],
    'p1_can_use_p2\'s_stargates': [False],
    'shared_p1_planet_report': [False],
    'shared_p1_scanner_report_of_enemies': [False],
    'shared_p1_scanner_report_of_nutals': [False],
    'shared_p1_scanner_report_of_teammates': [False],
    'shared_p1_scanner_report_of_unowned_things': [False],
    'shared_p1_fleet_reports': [False],
    'shared_p1_knowage_of_hiper_dinile_and_system_defence': [False],
    'shared_p1_passcode_for_hiper_dinile': [True],
    'shared_p1_passcode_for_system_defence': [True],
    'shared_p2_planet_report': [False],
    'shared_p2_scanner_report_of_enemies': [False],
    'shared_p2_scanner_report_of_nutals': [False],
    'shared_p2_scanner_report_of_teammates': [False],
    'shared_p2_scanner_report_of_unowned_things': [False],
    'shared_p2_fleet_reports': [False],
    'shared_p2_knowage_of_hiper_dinile_and_system_defence': [False],
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
            game_engin.send_message(self.p1, self.p2, 'do you except ' + p1.name + '\'s treaty proposal?')
        if self.relation == 'enemy':
            for key in self.__dict__:
                self.__dict__[key] = False
        pass

Treaty.set_defaults(Treaty, __defaults)
