from random import random
from .defaults import Defaults
from math import cos, sin, pi, atan2
from .stars_math import TERAMETER_2_LIGHTYEAR

def distance(ship1, ship2):
    return (ship1.location-ship2.location)

class Combat(Defaults):
    def __init__(self, **kwargs):
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
            if not ship is me: #me.player.relashons(ship.player) == 'enemy' and me.can_see(ship):
                if me.battle_plan.p_target == 'disengage' or len(ship.weapons) == 0:
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        move_to = ship.location
                    excape = True
                elif me.battle_plan.p_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        move_to = ship.location
                elif me.battle_plan._target == 'starbase':
                    if ship.__class__ == 'StarBace':
                        dis = distance(me, ship)
                        if dis < closest_p:
                            closest_p = dis
                            move_to = ship.location
                elif me.battle_plan.p_target == 'ship':
                    if ship.__class__ == 'Ship':
                        dis = distance(me, ship)
                        if dis < closest_p:
                            closest_p = dis
                            move_to = ship.location
                if me.battle_plan.s_target == 'disengage' or len(ship.weapons) == 0:
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        move_two = ship.location
                    excape2 = True
                elif me.battle_plan.s_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        move_two = ship.location
                elif me.battle_plan.s_target == 'starbase':
                    if ship.__class__ == 'StarBace':
                        dis = distance(me, ship)
                        if dis < closest_s:
                            closest_s = dis
                            move_two = ship.location
                elif me.battle_plan.s_target == 'ship':
                    if ship.__class__ == 'Ship':
                        dis = distance(me, ship)
                        if dis < closest_s:
                            closest_s = dis
                            move_two = ship.location
        if move_to:
            return (move_to, excape)
        elif move_two:
            return (move_two, excape2)
        else:
            return (me.location, False)
    
    """ calculates the ship to fire at"""
    def calc_strategy_f(self, me):
        closest_p = 1021
        closest_s = 1021
        fire_at = None
        fire_att = None
        for ship in self.everybody:
            if not ship is me: #me.player.relashons(ship.player) == 'enemy' and me.can_see(ship):
                if me.battle_plan.p_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        fire_at = ship
                elif me.battle_plan.p_target == 'starbase':
                    if ship.__class__ == 'StarBase':
                        dis = distance(me, ship)
                        if dis < closest_p:
                            closest_p = dis
                            fire_at = ship
                elif me.battle_plan.p_target == 'ship':
                    if not ship.__class__ == 'StarBase':
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
                    if ship.__class__ == 'StarBase':
                        dis = distance(me, ship)
                        if dis < closest_s:
                            closest_s = dis
                            fire_att = ship
                elif me.battle_plan.s_target == 'ship':
                    if not ship.__class__ == 'StarBase':
                        dis = distance(me, ship)
                        if dis < closest_s:
                            closest_s = dis
                            fire_att = ship
        if fire_at:
            return fire_at
        elif fire_att:
            return fire_att
        else:
            return None
        pass

    def move(self, ship):
        move = self.calc_strategy_m(ship)
        ship.location = ship.location.move(move[0], ship.max_distance, move[1])
        self.save_to_combat_log()
        pass

    def fire(self, ship):
        for weapon in ship.weapons:
            ship_to_fire_at = self.calc_strategy_f(ship)
            if ship_to_fire_at:
                damage = weapon.get_damage(ship.location-ship_to_fire_at.location, ship_to_fire_at.shields, ship_to_fire_at.armor, ship.scanner.range_visible(ship_to_fire_at.calc_aparent_mass()), ship_to_fire_at.ecm)
                ship_to_fire_at.shields = damage[0]
                ship_to_fire_at.armor = damage[1]
                if ship.armor==0:
                    ship.blow_up()
            self.save_to_combat_log()
        pass


    def save_to_combat_log(self):
        pass

    #self.save_to_combat_log()
    def take_turn(self):
        mi = 0
        for ship in self.everybody:
            ship.calc_initative()
            if ship.initative > mi:
                mi = int(ship.initative)
        for i in range(mi, -1, -1):
            for ship in self.everybody:
                if ship.initative == i:
                    self.move(ship)
        for i in range(mi, -1, -1):
            for ship in self.everybody:
                if ship.initative == i:
                    self.fire(ship)



