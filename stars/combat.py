from .defaults import Defaults
from .stars_math import TERAMETER_2_LIGHTYEAR
from copy import copy

def distance(ship1, ship2):
    return (ship1.ship.location-ship2.ship.location)

class Combat(Defaults):
    def __init__(self, **kwargs):
        self.everybody = []
        self.players = []
        self.date = 0.0
        super().__init__(**kwargs)
    
    """ calculates where the ship should move to"""
    def calc_strategy_m(self, me):
        closest_p = 1021
        closest_s = 1021
        m_lat = 0
        m_lon = 0
        m_dis = 1021
        move_to = None
        move_two = None
        excape = False
        excape2 = False
        for ship in self.everybody:
            if ship is not me and not me.player in ship.hidden_from: # and me.player.relashons(ship.player) == 'enemy':
                if me.battle_plan.p_target == 'disengage' or len(me.ship.weapons) == 0:
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        move_to = ship.ship.location
                    excape = True
                elif me.battle_plan.p_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        move_to = ship.ship.location
                elif me.battle_plan.p_target == 'starbase':
                    if ship.ship.is_starbase:
                        dis = distance(me, ship)
                        if dis < closest_p:
                            closest_p = dis
                            move_to = ship.ship.location
                elif me.battle_plan.p_target == 'ship':
#                    print('okay...p')
                    if not ship.ship.is_starbase:
#                        print('realy...p')
                        dis = distance(me, ship)
#                        print(dis)
#                        print(closest_p)
                        if dis < closest_p:
#                            print('OK NOW!!!!!!!!')
                            closest_p = dis
                            move_to = ship.ship.location
                if me.battle_plan.s_target == 'disengage' or len(me.ship.weapons) == 0:
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        move_two = ship.ship.location
                    excape2 = True
                elif me.battle_plan.s_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        move_two = ship.ship.location
                elif me.battle_plan.s_target == 'starbase':
#                    print('okay...s')
                    if ship.ship.is_starbase:
#                        print('realy...s')
                        dis = distance(me, ship)
#                        print(dis)
#                        print(closest_s)
                        if dis < closest_s:
#                            print('OK NOW!!!!!!!!!!!')
                            closest_s = dis
                            move_two = ship.ship.location
                elif me.battle_plan.s_target == 'ship':
                    if not ship.ship.is_starbase:
                        dis = distance(me, ship)
                        if dis < closest_s:
                            closest_s = dis
                            move_two = ship.ship.location
#        print(move_to)
#        print(move_two)
        if move_to:
#            print('what:!')
            return (move_to, excape)
        elif move_two:
#            print('oooo goody goody')
            return (move_two, excape2)
        else:
#            print('noooo')
            return (me.ship.location, False)
    
    def move(self, ship):
        move = self.calc_strategy_m(ship)
        ship.ship.location = ship.ship.location.move(move[0], self.calc_speed(ship)*TERAMETER_2_LIGHTYEAR, ship.battle_plan.standoff*TERAMETER_2_LIGHTYEAR)
        self.save_to_combat_log()
        pass

    """ calculates the ship to fire at"""
    def calc_strategy_f(self, me):
        closest_p = 1021
        closest_s = 1021
        fire_at = None
        fire_att = None
        for ship in self.everybody:
            if not ship is me and not me.player in ship.hidden_from: # and me.player.relashons(ship.player) == 'enemy':
                if me.battle_plan.p_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        fire_at = ship
                elif me.battle_plan.p_target == 'starbase':
#                    print('okay...p')
                    if ship.ship.is_starbase:
#                        print('realy...p')
                        dis = distance(me, ship)
#                        print(dis)
#                        print(closest_p)
                        if dis < closest_p:
#                            print('OK NOW!!!!!!!!!')
                            closest_p = dis
                            fire_at = ship
                elif me.battle_plan.p_target == 'ship':
                    if not ship.ship.is_starbase:
                        dis = distance(me, ship)
                        if dis < closest_p:
                            closest_p = dis
                            fire_at = ship
                if me.battle_plan.s_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        fire_att = ship 
                elif me.battle_plan.s_target == 'starbase':
#                    print('okay...s')
                    if ship.ship.is_starbase:
#                        print('realy...s')
                        dis = distance(me, ship)
#                        print(dis)
#                        print(closest_s)
                        if dis < closest_s:
#                            print('OK NOW!!!!!!!!!')
                            closest_s = dis
                            fire_att = ship
                elif me.battle_plan.s_target == 'ship':
                    if not ship.ship.is_starbase:
                        dis = distance(me, ship)
                        if dis < closest_s:
                            closest_s = dis
                            fire_att = ship
#        print(me.battle_plan.standoff)
#        print(distance(me, ship))
#        print(me.battle_plan.wait_until_closed_to_fire)
#        print(fire_at)
#        print(fire_att)
        if me.battle_plan.wait_until_closed_to_fire and distance(me, ship) > me.battle_plan.standoff:
#            print('ding dong')
            return None
        elif fire_at:
            return fire_at
        elif fire_att:
            return fire_att
        else:
            return None

    def fire(self, ship):
        for weapon in ship.ship.weapons:
            ship_to_fire_at = self.calc_strategy_f(ship)
            if ship_to_fire_at:
                damage = weapon.get_damage(distance(ship, ship_to_fire_at), ship_to_fire_at.ship.shields, ship_to_fire_at.ship.armor, ship.ship.scanner.range_visible(ship_to_fire_at.ship.calc_apparent_mass()), ship_to_fire_at.ship.ecm)
                if damage == (0, 0):
                    ship_to_fire_at.ship.expirence.battle_expirence += 0.05
                else:
                    ship.ship.expirence.battle_expirence += 0.1
                ship_to_fire_at.ship.shields_damage += damage[0]
                ship_to_fire_at.ship.armor_damage += damage[1]
                if ship_to_fire_at.ship.armor <= ship_to_fire_at.ship.armor_damage:
                    ship.ship.blow_up()
                    for ship3 in self.everybody:
                        while True:
                            try:
                                ship3.to_fire_at.remove(ship_to_fire_at)
                            except:
                                break
                ship_to_fire_at.to_fire_at.append(ship)
                ship.hidden_from = []
            self.save_to_combat_log()
        pass


    def save_to_combat_log(self):
        pass

    #self.save_to_combat_log()
    def fight(self):
        for ship in self.everybody:
            for ship2 in self.everybody:
                if ship.player.treatys.realashon_with(ship2.player) == 'Enemy':
                    ship.to_fire_at.appen(ship2)
        no_anti_cloak = copy(self.players)
        for ship in self.everybody:
            if ship.ship.scanner.anti_cloak > 0:
                no_anti_cloak.remove(ship.player)
        for ship in self.everybody:
            if ship.ship.calc_apparent_mass() == 0:
                ship.hidden_from = no_anti_cloak
        while True:
            self.turn()
            csf = []
            for ship in evorybody:
                csf.append(len(ship.to_fire_at) == 0)
            if all(csf):
                break
                
    
    def turn(self):
        everybody.sort(key=lambda ship: ship.ship.expirence.calc(self.date))
        for ship in self.everybody:
            self.move(ship)
        everybody.sort(key=lambda ship: ship.ship.expirence.calc(self.date), reverse=True)
        for ship in self.everybody:
            self.fire(ship)

    
    def add_ship(self, ship, player, battle_plan):
        s = _ship(ship, player, battle_plan)
        self.everybody.append(s)
        if not s.player in self.players:
            self.players.append(s.player)
    
    def calc_speed(self, ship):
        speed = []
        for e in ship.ship.engines:
            speed.append(e.speed_at_tach_100(ship.ship.mass, 0)/20)
        if len(speed) == 0:
            speed.append(0.05)
        return min(speed)
    


class _ship():
    def __init__(self, ship, player, battle_plan):
        self.ship = ship
        self.player = player
        self.battle_plan = battle_plan
        self.hidden_from = []
        self.to_fire_at = []
    




