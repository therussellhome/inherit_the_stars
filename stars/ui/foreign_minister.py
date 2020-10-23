from .treaties import Treaty
from .uiplayer import UiPlayer
from sys import maxsize


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
    'foreign_d1_p1_to_p2_safe_passage': [False],
    'foreign_d1_p2_to_p1_safe_passage': [False],
    "foreign_d1_p1_to_p2_intel_sharing": [False],
    "foreign_d1_p2_to_p1_intel_sharing": [False],
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
    'foreign_d2_p1_to_p2_safe_passage': [False],
    'foreign_d2_p2_to_p1_safe_passage': [False],
    "foreign_d2_p1_to_p2_intel_sharing": [False],
    "foreign_d2_p2_to_p1_intel_sharing": [False],
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
    'foreign_d3_p1_to_p2_safe_passage': [False],
    'foreign_d3_p2_to_p1_safe_passage': [False],
    "foreign_d3_p1_to_p2_intel_sharing": [False],
    "foreign_d3_p2_to_p1_intel_sharing": [False],
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
    'foreign_d4_p1_to_p2_safe_passage': [False],
    'foreign_d4_p2_to_p1_safe_passage': [False],
    "foreign_d4_p1_to_p2_intel_sharing": [False],
    "foreign_d4_p2_to_p1_intel_sharing": [False],
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
    'foreign_d5_p1_to_p2_safe_passage': [False],
    'foreign_d5_p2_to_p1_safe_passage': [False],
    "foreign_d5_p1_to_p2_intel_sharing": [False],
    "foreign_d5_p2_to_p1_intel_sharing": [False],
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
    'foreign_d6_p1_to_p2_safe_passage': [False],
    'foreign_d6_p2_to_p1_safe_passage': [False],
    "foreign_d6_p1_to_p2_intel_sharing": [False],
    "foreign_d6_p2_to_p1_intel_sharing": [False],
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
    'foreign_d7_p1_to_p2_safe_passage': [False],
    'foreign_d7_p2_to_p1_safe_passage': [False],
    "foreign_d7_p1_to_p2_intel_sharing": [False],
    "foreign_d7_p2_to_p1_intel_sharing": [False],
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
    'foreign_d8_p1_to_p2_safe_passage': [False],
    'foreign_d8_p2_to_p1_safe_passage': [False],
    "foreign_d8_p1_to_p2_intel_sharing": [False],
    "foreign_d8_p2_to_p1_intel_sharing": [False],
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
    'foreign_d9_p1_to_p2_safe_passage': [False],
    'foreign_d9_p2_to_p1_safe_passage': [False],
    "foreign_d9_p1_to_p2_intel_sharing": [False],
    "foreign_d9_p2_to_p1_intel_sharing": [False],
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
    'foreign_d10_p1_to_p2_safe_passage': [False],
    'foreign_d10_p2_to_p1_safe_passage': [False],
    "foreign_d10_p1_to_p2_intel_sharing": [False],
    "foreign_d10_p2_to_p1_intel_sharing": [False],
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
    'foreign_d11_p1_to_p2_safe_passage': [False],
    'foreign_d11_p2_to_p1_safe_passage': [False],
    "foreign_d11_p1_to_p2_intel_sharing": [False],
    "foreign_d11_p2_to_p1_intel_sharing": [False],
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
    'foreign_d12_p1_to_p2_safe_passage': [False],
    'foreign_d12_p2_to_p1_safe_passage': [False],
    "foreign_d12_p1_to_p2_intel_sharing": [False],
    "foreign_d12_p2_to_p1_intel_sharing": [False],
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
    'foreign_d13_p1_to_p2_safe_passage': [False],
    'foreign_d13_p2_to_p1_safe_passage': [False],
    "foreign_d13_p1_to_p2_intel_sharing": [False],
    "foreign_d13_p2_to_p1_intel_sharing": [False],
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
    'foreign_d14_p1_to_p2_safe_passage': [False],
    'foreign_d14_p2_to_p1_safe_passage': [False],
    "foreign_d14_p1_to_p2_intel_sharing": [False],
    "foreign_d14_p2_to_p1_intel_sharing": [False],
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
    'foreign_d15_p1_to_p2_safe_passage': [False],
    'foreign_d15_p2_to_p1_safe_passage': [False],
    "foreign_d15_p1_to_p2_intel_sharing": [False],
    "foreign_d15_p2_to_p1_intel_sharing": [False],
    "foreign_d15_negotiation": [''],
    'foreign_p1': [''],
    'foreign_p2': [''],
    'options_foreign_p2': [['', 'p2']],
    'foreign_relation': [['nutral']],
    'foreign_options_relation': [['team', 'nutral', 'enemy']],
    'foreign_cost_p1_to_p2_titanium': [100, 0, maxsize],
    'foreign_p1_is_selling_titanium': [False],
    'foreign_cost_p2_to_p1_titanium': [100, 0, maxsize],
    'foreign_p2_is_selling_titanium': [False],
    'foreign_cost_p1_to_p2_silicon': [100, 0, maxsize],
    'foreign_p1_is_selling_silicon': [False],
    'foreign_cost_p2_to_p1_silicon': [100, 0, maxsize],
    'foreign_p2_is_selling_silicon': [False],
    'foreign_cost_p1_to_p2_lithium': [100, 0, maxsize],
    'foreign_p1_is_selling_lithium': [False],
    'foreign_cost_p2_to_p1_lithium': [100, 0, maxsize],
    'foreign_p2_is_selling_lithium': [False],
    'foreign_cost_p1_to_p2_fuel': [5, 0, maxsize],
    'foreign_p1_is_selling_fuel': [False],
    'foreign_cost_p2_to_p1_fuel': [5, 0, maxsize],
    'foreign_p2_is_selling_fuel': [False],
    'foreign_cost_p1_to_p2_stargate': [5000, 0, maxsize],
    'foreign_p1_is_selling_stargate': [False],
    'foreign_cost_p2_to_p1_stargate': [5000, 0, maxsize],
    'foreign_p2_is_selling_stargate': [False],
    'foreign_p1_to_p2_safe_passage': [False],
    'foreign_p2_to_p1_safe_passage': [False],
    'foreign_shared_p1_general_intel': [False],
    'foreign_shared_p2_general_intel': [False],
}


""" """
class ForeignMinister(UiPlayer):
    
    def calc_ds(self, var, i, treaty, me):
        l = var.split('_')
        d = ''
        if not getattr(treaty, l[0]+'_is_selling_'+l[3]):
            d = '-'
        else:
            d = getattr(treaty, 'cost_'+var)
        setattr(self, 'foreign_d'+str(i)+'_cost_'+var, d)
    
    
    
    """ Interact with UI """
    def _post(self, action, me):
        print(self.foreign_cost_p1_to_p2_lithium)
        print(self.__dict__)
        try:
            me.treaties['p2'].p2
        except:
            me.treaties['p2']=Treaty(p1=me.name, p2='p2', p2_is_selling_titanium=True, p2_is_selling_silicon=True, p2_is_selling_lithium=True, p2_is_selling_fuel=True, p2_is_selling_stargate=True, p2_to_p1_safe_passage=True, shared_p2_general_intel=True)
            me.pending_treaties['p2']=me.treaties['p2']
        print('Hello everybody i\'m p2')
        self.options_foreign_p2 = []
        self.options_foreign_p2.append('p2')
        if action == 'revert':
            #self.reset_to_default()
            for key in me.treaties[foreign_p2].__dict__:
                setattr(self, 'foreign_'+key, me.treaties[foreign_p2].key)
        if action == 'propose':
            #print('propose')
            treety = Treaty()
            for key in treety.__dict__:
                setattr(treety, key, 'foreign_'+key)
            me.pending_treaties[foreign_p2] = treety
            if foreign_p2 == 'p2':
                me.treaties['p2']=me.pending_treaties['p2']
        """ set display values """
        i = 0
        treaties=me.treaties
        for z in me.treaties:
            i += 1
            setattr(self, 'foreign_player'+str(i)+'_name', treaties[z].p2)
            setattr(self, 'foreign_d'+str(i)+'_relation', treaties[z].relation)
            self.calc_ds('p1_to_p2_lithium', i, treaties[z], me)
            self.calc_ds('p2_to_p1_lithium', i, treaties[z], me)
            self.calc_ds('p1_to_p2_silicon', i, treaties[z], me)
            self.calc_ds('p2_to_p1_silicon', i, treaties[z], me)
            self.calc_ds('p1_to_p2_titanium', i, treaties[z], me)
            self.calc_ds('p2_to_p1_titanium', i, treaties[z], me)
            self.calc_ds('p1_to_p2_fuel', i, treaties[z], me)
            self.calc_ds('p2_to_p1_fuel', i, treaties[z], me)
            self.calc_ds('p1_to_p2_stargate', i, treaties[z], me)
            self.calc_ds('p2_to_p1_stargate', i, treaties[z], me)
            setattr(self, 'foreign_d'+str(i)+'_p1_to_p2_safe_passage', treaties[z].p1_to_p2_safe_passage)
            setattr(self, 'foreign_d'+str(i)+'_p2_to_p1_safe_passage', treaties[z].p2_to_p1_safe_passage)
            setattr(self, 'foreign_d'+str(i)+'_p1_to_p2_intel_sharing', treaties[z].shared_p1_general_intel)
            setattr(self, 'foreign_d'+str(i)+'_p2_to_p1_intel_sharing', treaties[z].shared_p2_general_intel)
            setattr(self, 'foreign_d'+str(i)+'_negotiation', me.pending_treaties[treaties[z].p2].stautus)


ForeignMinister.set_defaults(ForeignMinister, __defaults, no_reset=[])
