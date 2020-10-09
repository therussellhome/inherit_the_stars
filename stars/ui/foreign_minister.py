from .player import Player
from .game import Players


""" Default values (default, min, max)  """
__defaults = {
    "foreign_player1_name": [''],
    "foreign_d1_relation": [''],
    "foreign_d1_cost_p1_to_p2_lithium": [''],
    "foreign_d1_cost_p2_to_p1_lithium": [''],
    "foreign_d1_cost_p1_to_p2_silicon": [''],
    "foreign_d1_cost_p2_to_p1_silicon": [''],
    "foreign_d1_cost_p1_to_p2_titanium": [''],
    "foreign_d1_cost_p2_to_p1_titanium": [''],
    "foreign_d1_cost_p1_to_p2_fuel": [''],
    "foreign_d1_cost_p2_to_p1_fuel": [''],
    "foreign_d1_cost_p1_to_p2_stargate": [''],
    "foreign_d1_cost_p2_to_p1_stargate": [''],
    "foreign_d1_p1_to_p2_intel_sharing": [''],
    "foreign_d1_p2_to_p1_intel_sharing": [''],
    "foreign_d1_negotiation": [''],
    "foreign_player2_name": [''],
    "foreign_d2_relation": [''],
    "foreign_d2_cost_p1_to_p2_lithium": [''],
    "foreign_d2_cost_p2_to_p1_lithium": [''],
    "foreign_d2_cost_p1_to_p2_silicon": [''],
    "foreign_d2_cost_p2_to_p1_silicon": [''],
    "foreign_d2_cost_p1_to_p2_titanium": [''],
    "foreign_d2_cost_p2_to_p1_titanium": [''],
    "foreign_d2_cost_p1_to_p2_fuel": [''],
    "foreign_d2_cost_p2_to_p1_fuel": [''],
    "foreign_d2_cost_p1_to_p2_stargate": [''],
    "foreign_d2_cost_p2_to_p1_stargate": [''],
    "foreign_d2_p1_to_p2_intel_sharing": [''],
    "foreign_d2_p2_to_p1_intel_sharing": [''],
    "foreign_d2_negotiation": [''],
    "foreign_player3_name": [''],
    "foreign_d3_relation": [''],
    "foreign_d3_cost_p1_to_p2_lithium": [''],
    "foreign_d3_cost_p2_to_p1_lithium": [''],
    "foreign_d3_cost_p1_to_p2_silicon": [''],
    "foreign_d3_cost_p2_to_p1_silicon": [''],
    "foreign_d3_cost_p1_to_p2_titanium": [''],
    "foreign_d3_cost_p2_to_p1_titanium": [''],
    "foreign_d3_cost_p1_to_p2_fuel": [''],
    "foreign_d3_cost_p2_to_p1_fuel": [''],
    "foreign_d3_cost_p1_to_p2_stargate": [''],
    "foreign_d3_cost_p2_to_p1_stargate": [''],
    "foreign_d3_p1_to_p2_intel_sharing": [''],
    "foreign_d3_p2_to_p1_intel_sharing": [''],
    "foreign_d3_negotiation": [''],
    "foreign_player4_name": [''],
    "foreign_d4_relation": [''],
    "foreign_d4_cost_p1_to_p2_lithium": [''],
    "foreign_d4_cost_p2_to_p1_lithium": [''],
    "foreign_d4_cost_p1_to_p2_silicon": [''],
    "foreign_d4_cost_p2_to_p1_silicon": [''],
    "foreign_d4_cost_p1_to_p2_titanium": [''],
    "foreign_d4_cost_p2_to_p1_titanium": [''],
    "foreign_d4_cost_p1_to_p2_fuel": [''],
    "foreign_d4_cost_p2_to_p1_fuel": [''],
    "foreign_d4_cost_p1_to_p2_stargate": [''],
    "foreign_d4_cost_p2_to_p1_stargate": [''],
    "foreign_d4_p1_to_p2_intel_sharing": [''],
    "foreign_d4_p2_to_p1_intel_sharing": [''],
    "foreign_d4_negotiation": [''],
    "foreign_player5_name": [''],
    "foreign_d5_relation": [''],
    "foreign_d5_cost_p1_to_p2_lithium": [''],
    "foreign_d5_cost_p2_to_p1_lithium": [''],
    "foreign_d5_cost_p1_to_p2_silicon": [''],
    "foreign_d5_cost_p2_to_p1_silicon": [''],
    "foreign_d5_cost_p1_to_p2_titanium": [''],
    "foreign_d5_cost_p2_to_p1_titanium": [''],
    "foreign_d5_cost_p1_to_p2_fuel": [''],
    "foreign_d5_cost_p2_to_p1_fuel": [''],
    "foreign_d5_cost_p1_to_p2_stargate": [''],
    "foreign_d5_cost_p2_to_p1_stargate": [''],
    "foreign_d5_p1_to_p2_intel_sharing": [''],
    "foreign_d5_p2_to_p1_intel_sharing": [''],
    "foreign_d5_negotiation": [''],
    "foreign_player6_name": [''],
    "foreign_d6_relation": [''],
    "foreign_d6_cost_p1_to_p2_lithium": [''],
    "foreign_d6_cost_p2_to_p1_lithium": [''],
    "foreign_d6_cost_p1_to_p2_silicon": [''],
    "foreign_d6_cost_p2_to_p1_silicon": [''],
    "foreign_d6_cost_p1_to_p2_titanium": [''],
    "foreign_d6_cost_p2_to_p1_titanium": [''],
    "foreign_d6_cost_p1_to_p2_fuel": [''],
    "foreign_d6_cost_p2_to_p1_fuel": [''],
    "foreign_d6_cost_p1_to_p2_stargate": [''],
    "foreign_d6_cost_p2_to_p1_stargate": [''],
    "foreign_d6_p1_to_p2_intel_sharing": [''],
    "foreign_d6_p2_to_p1_intel_sharing": [''],
    "foreign_d6_negotiation": [''],
    "foreign_player7_name": [''],
    "foreign_d7_relation": [''],
    "foreign_d7_cost_p1_to_p2_lithium": [''],
    "foreign_d7_cost_p2_to_p1_lithium": [''],
    "foreign_d7_cost_p1_to_p2_silicon": [''],
    "foreign_d7_cost_p2_to_p1_silicon": [''],
    "foreign_d7_cost_p1_to_p2_titanium": [''],
    "foreign_d7_cost_p2_to_p1_titanium": [''],
    "foreign_d7_cost_p1_to_p2_fuel": [''],
    "foreign_d7_cost_p2_to_p1_fuel": [''],
    "foreign_d7_cost_p1_to_p2_stargate": [''],
    "foreign_d7_cost_p2_to_p1_stargate": [''],
    "foreign_d7_p1_to_p2_intel_sharing": [''],
    "foreign_d7_p2_to_p1_intel_sharing": [''],
    "foreign_d7_negotiation": [''],
    "foreign_player8_name": [''],
    "foreign_d8_relation": [''],
    "foreign_d8_cost_p1_to_p2_lithium": [''],
    "foreign_d8_cost_p2_to_p1_lithium": [''],
    "foreign_d8_cost_p1_to_p2_silicon": [''],
    "foreign_d8_cost_p2_to_p1_silicon": [''],
    "foreign_d8_cost_p1_to_p2_titanium": [''],
    "foreign_d8_cost_p2_to_p1_titanium": [''],
    "foreign_d8_cost_p1_to_p2_fuel": [''],
    "foreign_d8_cost_p2_to_p1_fuel": [''],
    "foreign_d8_cost_p1_to_p2_stargate": [''],
    "foreign_d8_cost_p2_to_p1_stargate": [''],
    "foreign_d8_p1_to_p2_intel_sharing": [''],
    "foreign_d8_p2_to_p1_intel_sharing": [''],
    "foreign_d8_negotiation": [''],
    "foreign_player9_name": [''],
    "foreign_d9_relation": [''],
    "foreign_d9_cost_p1_to_p2_lithium": [''],
    "foreign_d9_cost_p2_to_p1_lithium": [''],
    "foreign_d9_cost_p1_to_p2_silicon": [''],
    "foreign_d9_cost_p2_to_p1_silicon": [''],
    "foreign_d9_cost_p1_to_p2_titanium": [''],
    "foreign_d9_cost_p2_to_p1_titanium": [''],
    "foreign_d9_cost_p1_to_p2_fuel": [''],
    "foreign_d9_cost_p2_to_p1_fuel": [''],
    "foreign_d9_cost_p1_to_p2_stargate": [''],
    "foreign_d9_cost_p2_to_p1_stargate": [''],
    "foreign_d9_p1_to_p2_intel_sharing": [''],
    "foreign_d9_p2_to_p1_intel_sharing": [''],
    "foreign_d9_negotiation": [''],
    "foreign_player10_name": [''],
    "foreign_d10_relation": [''],
    "foreign_d10_cost_p1_to_p2_lithium": [''],
    "foreign_d10_cost_p2_to_p1_lithium": [''],
    "foreign_d10_cost_p1_to_p2_silicon": [''],
    "foreign_d10_cost_p2_to_p1_silicon": [''],
    "foreign_d10_cost_p1_to_p2_titanium": [''],
    "foreign_d10_cost_p2_to_p1_titanium": [''],
    "foreign_d10_cost_p1_to_p2_fuel": [''],
    "foreign_d10_cost_p2_to_p1_fuel": [''],
    "foreign_d10_cost_p1_to_p2_stargate": [''],
    "foreign_d10_cost_p2_to_p1_stargate": [''],
    "foreign_d10_p1_to_p2_intel_sharing": [''],
    "foreign_d10_p2_to_p1_intel_sharing": [''],
    "foreign_d10_negotiation": [''],
    "foreign_player11_name": [''],
    "foreign_d11_relation": [''],
    "foreign_d11_cost_p1_to_p2_lithium": [''],
    "foreign_d11_cost_p2_to_p1_lithium": [''],
    "foreign_d11_cost_p1_to_p2_silicon": [''],
    "foreign_d11_cost_p2_to_p1_silicon": [''],
    "foreign_d11_cost_p1_to_p2_titanium": [''],
    "foreign_d11_cost_p2_to_p1_titanium": [''],
    "foreign_d11_cost_p1_to_p2_fuel": [''],
    "foreign_d11_cost_p2_to_p1_fuel": [''],
    "foreign_d11_cost_p1_to_p2_stargate": [''],
    "foreign_d11_cost_p2_to_p1_stargate": [''],
    "foreign_d11_p1_to_p2_intel_sharing": [''],
    "foreign_d11_p2_to_p1_intel_sharing": [''],
    "foreign_d11_negotiation": [''],
    "foreign_player12_name": [''],
    "foreign_d12_relation": [''],
    "foreign_d12_cost_p1_to_p2_lithium": [''],
    "foreign_d12_cost_p2_to_p1_lithium": [''],
    "foreign_d12_cost_p1_to_p2_silicon": [''],
    "foreign_d12_cost_p2_to_p1_silicon": [''],
    "foreign_d12_cost_p1_to_p2_titanium": [''],
    "foreign_d12_cost_p2_to_p1_titanium": [''],
    "foreign_d12_cost_p1_to_p2_fuel": [''],
    "foreign_d12_cost_p2_to_p1_fuel": [''],
    "foreign_d12_cost_p1_to_p2_stargate": [''],
    "foreign_d12_cost_p2_to_p1_stargate": [''],
    "foreign_d12_p1_to_p2_intel_sharing": [''],
    "foreign_d12_p2_to_p1_intel_sharing": [''],
    "foreign_d12_negotiation": [''],
    "foreign_player13_name": [''],
    "foreign_d13_relation": [''],
    "foreign_d13_cost_p1_to_p2_lithium": [''],
    "foreign_d13_cost_p2_to_p1_lithium": [''],
    "foreign_d13_cost_p1_to_p2_silicon": [''],
    "foreign_d13_cost_p2_to_p1_silicon": [''],
    "foreign_d13_cost_p1_to_p2_titanium": [''],
    "foreign_d13_cost_p2_to_p1_titanium": [''],
    "foreign_d13_cost_p1_to_p2_fuel": [''],
    "foreign_d13_cost_p2_to_p1_fuel": [''],
    "foreign_d13_cost_p1_to_p2_stargate": [''],
    "foreign_d13_cost_p2_to_p1_stargate": [''],
    "foreign_d13_p1_to_p2_intel_sharing": [''],
    "foreign_d13_p2_to_p1_intel_sharing": [''],
    "foreign_d13_negotiation": [''],
    "foreign_player14_name": [''],
    "foreign_d14_relation": [''],
    "foreign_d14_cost_p1_to_p2_lithium": [''],
    "foreign_d14_cost_p2_to_p1_lithium": [''],
    "foreign_d14_cost_p1_to_p2_silicon": [''],
    "foreign_d14_cost_p2_to_p1_silicon": [''],
    "foreign_d14_cost_p1_to_p2_titanium": [''],
    "foreign_d14_cost_p2_to_p1_titanium": [''],
    "foreign_d14_cost_p1_to_p2_fuel": [''],
    "foreign_d14_cost_p2_to_p1_fuel": [''],
    "foreign_d14_cost_p1_to_p2_stargate": [''],
    "foreign_d14_cost_p2_to_p1_stargate": [''],
    "foreign_d14_p1_to_p2_intel_sharing": [''],
    "foreign_d14_p2_to_p1_intel_sharing": [''],
    "foreign_d14_negotiation": [''],
    "foreign_player15_name": [''],
    "foreign_d15_relation": [''],
    "foreign_d15_cost_p1_to_p2_lithium": [''],
    "foreign_d15_cost_p2_to_p1_lithium": [''],
    "foreign_d15_cost_p1_to_p2_silicon": [''],
    "foreign_d15_cost_p2_to_p1_silicon": [''],
    "foreign_d15_cost_p1_to_p2_titanium": [''],
    "foreign_d15_cost_p2_to_p1_titanium": [''],
    "foreign_d15_cost_p1_to_p2_fuel": [''],
    "foreign_d15_cost_p2_to_p1_fuel": [''],
    "foreign_d15_cost_p1_to_p2_stargate": [''],
    "foreign_d15_cost_p2_to_p1_stargate": [''],
    "foreign_d15_p1_to_p2_intel_sharing": [''],
    "foreign_d15_p2_to_p1_intel_sharing": [''],
    "foreign_d15_negotiation": [''],
}


""" """
class ForeignMinister(Player):
    
    def calc_ds(self, var, i, offset, player, me):
        l = var.split('_')
        d = ''
        if not getattr(me.treaties[player.name], l[0]+'_is_selling_'+l[3]):
            d = '-'
        else:
            d = getattr(me.treaties[player.name], 'cost_'+var)
        setattr(self, 'foreign_d'+str(i+offset)+'_cost_'+var, d)
    
    def calc_di(self, var, i, offset, player, me):
        lisp = ['planet_report', 'scanner_report_of_enemies', 'scanner_report_of_nutals', 'scanner_report_of_teammates', 'scanner_report_of_intersteler_objects', 'fleet_reports', 'knowlage_of_hiper_dinile_and_system_defence', 'passcode_for_hiper_dinile', 'passcode_for_system_defence']
        l = var.split('_')
        d = []
        for t in lisp:
            d.append(getattr(player.treaties[player], 'shared_'+l[0]+t))
        v = all(d)+any(d)
        setattr(self, 'foreign_d'+str(i+offset)+'_'+var, v)
    
    
    """ Interact with UI """
    def _post(self, action, me):
        """ set display values """
        p = 1
        for i in range(len(game_engine.players)):
            if me == game_engine.players[i]:
                p -= 1
            else:
                setattr(me, 'foreign_player'+str(i+p)+'_name', players[i].name)
                setattr(me, 'foreign_d'+str(i+p)+'_relation', me.treaties[players[i].name].relation)
                self.calc_ds('p1_to_p2_lithium', i, p, players[i], me)
                self.calc_ds('p2_to_p1_lithium', i, p, players[i], me)
                self.calc_ds('p1_to_p2_silicon', i, p, players[i], me)
                self.calc_ds('p2_to_p1_silicon', i, p, players[i], me)
                self.calc_ds('p1_to_p2_titanium', i, p, players[i], me)
                self.calc_ds('p2_to_p1_titanium', i, p, players[i], me)
                self.calc_ds('p1_to_p2_fuel', i, p, players[i], me)
                self.calc_ds('p2_to_p1_fuel', i, p, players[i], me)
                self.calc_ds('p1_to_p2_stargate', i, p, players[i], me)
                self.calc_ds('p2_to_p1_stargate', i, p, players[i], me)
                self.calc_di('p1_to_p2_intel_sharing', i, p, players[i], me)
                self.calc_di('p2_to_p1_intel_sharing', i, p, players[i], me)
                setattr(me, 'foreign_d'+str(i+p)+'_negotiation', 'how to calculate this? hmmm')
        pass


ForeignMinister.set_defaults(ForeignMinister, __defaults, no_reset=[])
