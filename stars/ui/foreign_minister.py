from ..treaties import Treaty
from .playerui import PlayerUI
from sys import maxsize


""" Default values (default, min, max)  """
__defaults = {
    'foreign_treaties': [[]],
    'foreign_relation_is_neutral': [True],
    'foreign_relation_is_team': [False],
    'foreign_relation_is_enemy': [False],
    'foreign_p2': ['']
#    'cost_p1_to_p2_titanium': [33, 0, 120],
#    'p1_is_selling_titanium': [False],
#    'cost_p2_to_p1_titanium': [33, 0, 120],
#    'p2_is_selling_titanium': [False],
#    'cost_p1_to_p2_silicon': [33, 0, 120],
#    'p1_is_selling_silicon': [False],
#    'cost_p2_to_p1_silicon': [33, 0, 120],
#    'p2_is_selling_silicon': [False],
#    'cost_p1_to_p2_lithium': [33, 0, 120],
#    'p1_is_selling_lithium': [False],
#    'cost_p2_to_p1_lithium': [33, 0, 120],
#    'p2_is_selling_lithium': [False],
#    'cost_p1_to_p2_fuel': [10, 0, 999],
#    'p1_is_selling_fuel': [False],
#    'cost_p2_to_p1_fuel': [10, 0, 999],
#    'p2_is_selling_fuel': [False],
#    'cost_p1_to_p2_stargate': [5000, 0, 99999],
#    'p1_is_selling_stargate': [False],
#    'cost_p2_to_p1_stargate': [5000, 0, 99999],
#    'p2_is_selling_stargate': [False],
#    'p1_is_selling_intel': [False],
#    'cost_p2_to_p1_intel': [100, 0, 999],
#    'p2_is_selling_intel': [False],
#    'cost_p1_to_p2_intel': [100, 0, 999],
#    'p1_is_selling_passage': [False],
#    'cost_p2_to_p1_passage': [50, 0, 999],
#    'p2_is_selling_passage': [False],
#    'cost_p1_to_p2_passage': [50, 0, 999],

}


""" """
class ForeignMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        self.calc_r()
        team_true = ['stargate', 'passage', 'intel']
        enemy_false = ['titanium', 'silicon', 'lithium', 'fuel', 'stargate', 'passage', 'intel']
        p = ['foreign_p1_is_selling_', 'foreign_p2_is_selling_']
        if self.foreign_relation_is_team:
            for m in p:
                for v in team_true:
                    setattr(self, m+v, True)
        if self.foreign_relation_is_enemy:
            for m in p:
                for x in enemy_false:
                    setattr(self, m+x, False)
        #print(self.foreign_cost_p1_to_p2_lithium)
        #print(self.__dict__)
        #print(self.player.treaties)
        try:
            self.player.treaties['p2'].p2
        except:
            self.player.treaties['p2']=Treaty(p1=self.player.name, p2='p2', p2_is_selling_titanium=True, p2_is_selling_silicon=True, p2_is_selling_lithium=True, p2_is_selling_fuel=True, p2_is_selling_stargate=True, p2_is_selling_passage=True, p2_is_selling_intel=True)
            self.player.pending_treaties['p2']=self.player.treaties['p2']
        #print('Hello everybody i\'m p2')
        if action.startswith('edit='):
            self.foreign_p2 = action[5:]
            action = 'revert'
        if action.startswith('revoke='):
            t = action[7:]
            self.player.treaties[t].reset_to_default()
        if action.startswith('reject='):
            self.player.pending_treaties[action[7:]].status = 'rejected'
        if action.startswith('accept='):
            self.player.pending_treaties[action[7:]].status = 'accepted'
            if action[7:] == 'p2':
                self.player.treaties['p2']=self.player.pending_treaties['p2']
        if action == 'propose':
            self.foreign_stautus = 'sent'
            treety = Treaty()
            for key in treety.__dict__:
                setattr(treety, key, getattr(self, 'foreign_'+key))
            if treety.relation == 'enemy':
                treety.reset_to_default()
                treety.relation = 'enemy'
                self.player.treaties[self.foreign_p2] = treety
            self.player.pending_treaties[self.foreign_p2] = treety
        #print(self.player.treaties)
        if action == 'revert':
            t = self.player.pending_treaties[self.foreign_p2]
            if t.status == 'rejected':
                t = self.player.treaties[self.foreign_p2]
            for key in t.__dict__:
                setattr(self, 'foreign_'+key, t.__dict__[key])
                self.foreign_relation_is_neutral = False
                self.foreign_relation_is_team = False
                self.foreign_relation_is_enemy = False
                setattr(self, 'foreign_relation_is_'+self.foreign_relation, True)
        """ set display values """
        i = 0
        self.foreign_treaties.append('<th></th><th></th><th></th>\
            <th><i style="font-size: 85%" class="li" title="Lithium">1</i></th>\
            <th><i style="font-size: 85%" class="si" title="Silicon">1</i></th>\
            <th><i style="font-size: 85%" class="ti" title="Titanium">1</i></th>\
            <th><i style="font-size: 85%" class="fa-free-code-camp" title="fuel">10k</i></th>\
            <th><i style="font-size: 150%" class="fab fa-galactic-republic" title="stargate"></i></th>\
            <th><i style="font-size: 150%" class="fas fa-virus-slash" title="safe passage"></i></th>\
            <th><i style="font-size: 150%" class="fas fa-user-secret" title="intel sharing"></i></th>')
        for z in self.player.seen_players:
            treaty = self.calc_treaty(z)
            p_treaty = self.calc_p_treaty(z)
            self.foreign_treaties.append('<td><i class="fas fa-pastafarianism"></i></td>\
                <td colspan="11" style="font-size: 75%">' + self.find_name(treaty) + '</td>\
                ')
            self.foreign_treaties.append('<td></td><td rowspan="2" style="font-size: 150%">' + self.calcR(treaty) + '</td>\
                <td style="font-size: 70%">sell</td><td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_lithium', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_silicon', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_titanium', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_fuel', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_stargate', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_passage', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_intel', treaty) + '</td>\
                <td rowspan="2"><i class="button fas fa-pencil-alt button_s" title="edit" onclick="post(\'foreign_minister\', \'?edit=' + z + '\')"></i></td>\
                <td rowspan="2"><i class="button far fa-trash-alt button_s" title="revoke" onclick="post(\'foreign_minister\', \'?revoke=' + z + '\')"></i></td>\
                ')
            self.foreign_treaties.append('<td></td><td style="font-size: 70%">buy</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_lithium', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_silicon', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_titanium', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_fuel', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_stargate', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_passage', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_intel', treaty) + '</td>\
                ')
            if p_treaties[z]:
                #print(self.calcR(p_treaties[z]))
                #print(self.calc_ds('p1_to_p2_lithium', p_treaties[z]), self.calc_ds('p2_to_p1_lithium', p_treaties[z]))
                #print(self.calc_ds('p1_to_p2_silicon', p_treaties[z]), self.calc_ds('p2_to_p1_silicon', p_treaties[z]))
                #print(self.calc_ds('p1_to_p2_titanium', p_treaties[z]), self.calc_ds('p2_to_p1_titanium', p_treaties[z]))
                #print(self.calc_ds('p1_to_p2_fuel', p_treaties[z]), self.calc_ds('p2_to_p1_fuel', p_treaties[z]))
                #print(self.calc_ds('p1_to_p2_stargate', p_treaties[z]), self.calc_ds('p2_to_p1_stargate', p_treaties[z]))
                #print(self.check(p_treaties[z].p1_to_p2_safe_passage))
                #print(self.check(p_treaties[z].p2_to_p1_safe_passage))
                #print(self.check(p_treaties[z].p1_shared_intel))
                #print(self.check(p_treaties[z].p2_shared_intel))
                #print(self.calc_c(p_treaties[z], 'a'))
                #print(self.calc_c(p_treaties[z], 'r'))
                self.foreign_treaties.append('<td></td><td rowspan="2" style="font-size: 150%">' + self.calcR(p_treaty) + '</td>\
                    <td style="font-size: 70%">sell</td><td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_lithium', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_silicon', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_titanium', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_fuel', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_stargate', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_passage', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_intel', p_treaty) + '</td>\
                    <td rowspan="2"><i class="button far fa-check-circle button_s"' + self.calc_c(p_treaty, 'a') + 'title="accept" onclick="post(\'foreign_minister\', \'?accept=' + z + '\')"></i></td>\
                    <td rowspan="2"><i class="button far fa-times-circle button_s"' + self.calc_c(p_treaty, 'r') + 'title="reject" onclick="post(\'foreign_minister\', \'?reject=' + z + '\')"></i></td>\
                    ')
                self.foreign_treaties.append('<td></td><td style="font-size: 70%">buy</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_lithium', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_silicon', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_titanium', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_fuel', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_stargate', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_passage', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_intel', p_treaty) + '</td>\
                    ')
        self.calc_r()
        #print(self.player.treaties)
        #print(self.__dict__)
    
    def calc_treaty(self, whith):
        for key in self.player.treaties:
            t = self.player.treaties[key]
            if whith in t.prices:
                if len(accepted_by) == 2:
                    if not replaced_by == '':
                        return self.palyoer.treaties[replaced_by]
                    return t
        t = treaties.Treaty()
        return t
    
    def calc_p_treaty(self, whith):
        for key in self.player.treaties:
            t = self.player.treaties[key]
            if whith in t.prices:
                if len(accepted_by) == 1:
                    return t
        return None
    
    def find_name(self, treaty):
        for n in treaty.prices:
            if not n == self.player.name:
                return n
    
    def check(self, boo):
        r = ''
        if boo:
            r = 'checked'
        return r
    
    def calc_c(self, t, c):
        if c == 'a' and t.status == 'accepted':
            return ' style="color: green"'
        if c == 'r' and t.status == 'rejected':
            return ' style="color: red"'
        return ''
    
    def calcR(self, treaty):
        t = '<i class="fas fa-meh"></i>'
        if treaty.relation == 'neutral':
            t = '<i class="fas fa-meh"></i>'
        elif treaty.relation == 'team':
            t = '<i class="fas fa-handshake"></i>'
        elif treaty.relation == 'enemy':
            t = '<i class="fas fa-skull-crossbones"></i>'
        return t
    
    def calc_r(self):
        if self.foreign_relation_is_neutral:
            setattr(self, 'foreign_relation', 'neutral')
        elif self.foreign_relation_is_team:
            setattr(self, 'foreign_relation', 'team')
        elif self.foreign_relation_is_enemy:
            setattr(self, 'foreign_relation', 'enemy')
        self.foreign_relation_is_neutral = False
        self.foreign_relation_is_team = False
        self.foreign_relation_is_enemy = False
        setattr(self, 'foreign_relation_is_'+self.foreign_relation, True)
    
    def calc_ds(self, var, treaty):
        l = var.split('_')
        d = ''
        if not getattr(treaty, l[0]+'_is_selling_'+l[3]):
            d = '-'
        else:
            d = '<i class="fa-bolt" title="Energy">' + str(getattr(treaty, 'cost_'+var)) + '</i>'
        return d

#for key in Treaty.defaults:
#    __defaults['foreign_' + key] = Treaty.defaults[key]

ForeignMinister.set_defaults(ForeignMinister, __defaults)
