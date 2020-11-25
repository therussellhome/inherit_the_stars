from ..treaties import Treaty
from .playerui import PlayerUI
from sys import maxsize


""" Default values (default, min, max)  """
__defaults = {
    'foreign_treaties': [[]],
    'foreign_relation_is_neutral': [True],
    'foreign_relation_is_team': [False],
    'foreign_relation_is_enemy': [False],
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
        treaties=self.player.treaties
        p_treaties=self.player.pending_treaties
        for z in self.player.treaties:
            self.foreign_treaties.append('<td><i class="fas fa-pastafarianism"></i></td>\
                <td colspan="11" style="font-size: 75%">' + z + '</td>\
                ')
            self.foreign_treaties.append('<td></td><td rowspan="2" style="font-size: 150%">' + self.calcR(treaties[z]) + '</td>\
                <td style="font-size: 70%">sell</td><td style="font-size: 75%; text-align: center">' + self.calc_ds('p1_to_p2_lithium', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_silicon', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_titanium', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_fuel', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_stargate', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_passage', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_intel', treaties[z]) + '</td>\
                <td rowspan="2"><i class="button fas fa-pencil-alt button_s" title="edit" onclick="post(\'foreign_minister\', \'?edit=' + z + '\')"></i></td>\
                <td rowspan="2"><i class="button far fa-trash-alt button_s" title="revoke" onclick="post(\'foreign_minister\', \'?revoke=' + z + '\')"></i></td>\
                ')
            self.foreign_treaties.append('<td></td><td style="font-size: 75%">buy</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_lithium', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_silicon', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_titanium', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_fuel', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_stargate', treaties[z]) + '\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_passage', treaties[z]) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_intel', treaties[z]) + '</td>\
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
                self.foreign_treaties.append('<td></td><td rowspan="2" style="font-size: 150%">' + self.calcR(p_treaties[z]) + '</td>\
                    <td style="font-size: 70%">sell</td><td style="font-size: 75%; text-align: center">' + self.calc_ds('p1_to_p2_lithium', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_silicon', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_titanium', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_fuel', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_stargate', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_passage', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p1_to_p2_intel', p_treaties[z]) + '</td>\
                    <td rowspan="2"><i class="button far fa-check-circle button_s"' + self.calc_c(p_treaties[z], 'a') + 'title="accept" onclick="post(\'foreign_minister\', \'?accept=' + z + '\')"></i></td>\
                    <td rowspan="2"><i class="button far fa-times-circle button_s"' + self.calc_c(p_treaties[z], 'r') + 'title="reject" onclick="post(\'foreign_minister\', \'?reject=' + z + '\')"></i></td>\
                    ')
                self.foreign_treaties.append('<td></td><td style="font-size: 75%">buy</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_lithium', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_silicon', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_titanium', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_fuel', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_stargate', p_treaties[z]) + '\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_passage', p_treaties[z]) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('p2_to_p1_intel', p_treaties[z]) + '</td>\
                    ')
        self.calc_r()
        #print(self.player.treaties)
        #print(self.__dict__)
    
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

for key in Treaty.defaults:
    __defaults['foreign_' + key] = Treaty.defaults[key]

ForeignMinister.set_defaults(ForeignMinister, __defaults)
