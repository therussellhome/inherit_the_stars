from ..treaties import Treaty
from .playerui import PlayerUI
from ..player import Player #for p2 only
from ..reference import Reference #for p2 only


""" Default values (default, min, max)  """
__defaults = {
    'foreign_treaties': [[]],
    'foreign_p2': [''],
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
        team_true = ['gate', 'passage', 'intel']
        enemy_false = ['ti', 'si', 'li', 'fuel', 'gate', 'passage', 'intel']
        p = ['foreign_sell_', 'foreign_buy_']
        if self.foreign_relation_is_team:
            for m in p:
                for v in team_true:
                    setattr(self, m+v, True)
        if self.foreign_relation_is_enemy:
            for m in p:
                for x in enemy_false:
                    setattr(self, m+x, False)
        #print(self.foreign_sell_li_at)
        #print(self.__dict__)
        #print(self.player.__dict__)
        #print(self.player.treaties)
        #for key in self.player.treaties:
            #print(key, self.player.treaties[key].__dict__)
        p2 = Reference(Player(name='not_to_lazy_to_name_my_race P2'))
        try:
            s = self.player.seen_players[0]
            #print(s)
        except:
            t = Treaty(accepted_by=['not_to_lazy_to_name_my_race P2'], me=Reference(self.player), other_player=p2, buy_ti=True, buy_si=True, buy_li=True, buy_fuel=True, buy_gate=True, buy_passage=True, buy_intel=True)
            self.player.treaties[t.name] = t
            self.player.seen_players.append(p2)
        #print('Hello everybody i\'m p2')
        if action.startswith('edit='):
            for p in self.player.seen_players:
        #        print(p.name, action, p.name == action[5:])
                if p.name == action[5:]:
                    op = p
            self.foreign_other_player = op
            action = 'revert'
        if action.startswith('reject='):
            t = self.player.treaties[action[7:]]
            try:
                t.rejected_by.remove(self.player.name)
            except:
                try:
                    t.accepted_by.remove(self.player.name)
                except:
                    pass
            t.rejected_by.append(self.player.name)
        if action == 'propose':
            t = self.player.calc_p_treaty(self.foreign_other_player)
            if t:
                try:
                    t.rejected_by.remove(self.player.name)
                except:
                    try:
                        t.accepted_by.remove(self.player.name)
                    except:
                        pass
                t.rejected_by.append(self.player.name)
            treety = Treaty()
            if treety.relation == 'enemy':
                treety.relation = 'enemy'
                treety.accepted_by = [self.player.name, self.player.name]
                self.player.treaties[treety.name] = treety
            else:
                for key in Treaty.defaults:
                    setattr(treety, key, getattr(self, 'foreign_'+key))
            self.player.treaties[treety.name] = treety
            action = 'accept='+treety.name
        if action.startswith('accept='):
            print(action)
            t = self.player.treaties[action[7:]]
            try:
                t.accepted_by.remove(self.player.name)
            except:
                try:
                    t.rejected_by.remove(self.player.name)
                except:
                    pass
            t.accepted_by.append(self.player.name)
        #    if action[7:] == 'p2': #TODO
        #        self.player.treaties['p2']=self.player.pending_treaties['p2']
        #print(self.player.treaties)
        if action == 'revert':
            t = self.player.calc_p_treaty(self.foreign_other_player)
            if not t:
                t = self.player.calc_treaty(self.foreign_other_player)
            for key in t.__dict__:
                setattr(self, 'foreign_'+key, t.__dict__[key])
            self.foreign_relation_is_neutral = False
            self.foreign_relation_is_team = False
            self.foreign_relation_is_enemy = False
            setattr(self, 'foreign_relation_is_'+self.foreign_relation, True)
        """ set display values """
        try:
            self.foreing_p2 = self.foreign_other_player.name
        except:
            pass
        self.foreign_treaties.append('<th></th><th></th><th></th>\
            <th><i style="font-size: 85%" class="li" title="Lithium">1</i></th>\
            <th><i style="font-size: 85%" class="si" title="Silicon">1</i></th>\
            <th><i style="font-size: 85%" class="ti" title="Titanium">1</i></th>\
            <th><i style="font-size: 85%" class="fa-free-code-camp" title="fuel">10k</i></th>\
            <th><i style="font-size: 150%" class="fab fa-galactic-republic" title="stargate"></i></th>\
            <th><i style="font-size: 150%" class="fas fa-virus-slash" title="safe passage"></i></th>\
            <th><i style="font-size: 150%" class="fas fa-user-secret" title="intel sharing"></i></th>')
        for z in self.player.seen_players:
            treaty = self.player.calc_treaty(z)
            p_treaty = self.player.calc_p_treaty(z)
            self.foreign_treaties.append('<td><i class="fas fa-pastafarianism"></i></td>\
                <td colspan="11" style="font-size: 75%">' + z.name + '</td>\
                ')
            self.foreign_treaties.append('<td></td><td rowspan="2" style="font-size: 150%">' + self.calcR(treaty) + '</td>\
                <td style="font-size: 70%">sell</td><td style="font-size: 75%; text-align: center">' + self.calc_ds('sell_li', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_si', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_ti', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_fuel', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_gate', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_passage', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_intel', treaty) + '</td>\
                <td rowspan="2"><i class="button fas fa-pencil-alt button_s" title="edit" onclick="post(\'foreign_minister\', \'?edit=' + z.name + '\')"></i></td>\
                <td rowspan="2"><i class="button far fa-trash-alt button_s" title="revoke" onclick="post(\'foreign_minister\', \'?reject=' + treaty.name + '\')"></i></td>\
                ')
            self.foreign_treaties.append('<td></td><td style="font-size: 75%">buy</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_li', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_si', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_ti', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_fuel', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_gate', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_passage', treaty) + '</td>\
                <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_intel', treaty) + '</td>\
                ')
            if p_treaty:
                self.foreign_treaties.append('<td></td><td rowspan="2" style="font-size: 150%">' + self.calcR(p_treaty) + '</td>\
                    <td style="font-size: 70%">sell</td><td style="font-size: 75%; text-align: center">' + self.calc_ds('sell_li', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_si', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_ti', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_fuel', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_gate', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_passage', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('sell_intel', p_treaty) + '</td>\
                    <td rowspan="2"><i class="button far fa-check-circle button_s"' + self.calc_c(p_treaty, 'a') + 'title="accept" onclick="post(\'foreign_minister\', \'?accept=' + p_treaty.name + '\')"></i></td>\
                    <td rowspan="2"><i class="button far fa-times-circle button_s"' + self.calc_c(p_treaty, 'r') + 'title="reject" onclick="post(\'foreign_minister\', \'?reject=' + p_treaty.name + '\')"></i></td>\
                    ')
                self.foreign_treaties.append('<td></td><td style="font-size: 75%">buy</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_li', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_si', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_ti', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_fuel', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_gate', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_passage', p_treaty) + '</td>\
                    <td style="font-size: 70%; text-align: center">' + self.calc_ds('buy_intel', p_treaty) + '</td>\
                    ')
        self.calc_r()
        #print(self.player.treaties)
        #print(self.__dict__)
        #print(self.player.__dict__)
    
    def calc_c(self, t, c):
        if c == 'a' and self.player.name in t.accepted_by:
            return ' style="color: green"'
        if c == 'r' and self.player.name in t.rejected_by:
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
        if not getattr(treaty, var):
            d = '-'
        else:
            d = '<i class="fa-bolt" title="Energy">' + str(getattr(treaty, var+'_at')) + '</i>'
        return d

for key in Treaty.defaults:
    __defaults['foreign_' + key] = Treaty.defaults[key]

ForeignMinister.set_defaults(ForeignMinister, __defaults, sparse_json=False)
