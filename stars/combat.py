from random import random
from math import cos, sin, pi, atan2
from .stars_math import TERAMETER_2_LIGHTYEAR

def polar_to_cartesian(dis, lat, lon):
    x = round(cos(lat*pi/180)*dis*cos(lon*pi/180), 5)
    y = round(sin(lat*pi/180)*dis*cos(lon*pi/180), 5)
    z = round(sin(lon*pi/180)*dis, 5)
    return [x, y, z]

def distance(ship1, ship2):
    return (ship1.location-ship2.location)

class combat():
    def __init__(self, **kwargs):
        for key in **kwargs:
            self.__dict__[key] = **kwargs[key]
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
            if True #me.player.relashons(ship.player) == 'enemy' and me.can_see(ship):
                if me.battle_plan.p_target == 'disengage' or len(ship.wepons) == 0:
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
                if me.battle_plan.s_target == 'disengage' or len(ship.wepons) == 0:
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
        #    if not excape:
        #        m_dis = closest_p
        #    m_lat = atan2(move_to.y, move_to.x)
        #    m_lon = atan2(move_to.x, move_to.z)
        #    if excape:
        #        m_lon += pi
        elif move_two:
            return (move_two, excape2)
        #    if not excape2:
        #        m_dis = closest_s
        #    m_lat = atan2(move_two.y, move_two.x)
        #    m_lon = atan2(move_two.x, move_two.z)
        #    if excape2:
        #        m_lon += pi
        else:
            return (me.location, False)
        #    m_dis = 0
        #return [m_dis, m_lat*180/pi, m_lon*180/pi]
    """ calculates the ship to fire at"""
    def calc_strategy_f(self, me, wepon):
        closest_p = 1021
        closest_s = 1021
        fire_at = None
        fire_att = None
        for ship in self.everybody:
            if True #me.player.relashons(ship.player) == 'enemy' and me.can_see(ship):
                if me.battle_plan.p_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        fire_at = ship
                elif me.battle_plan.p_target == 'starbase':
                    if ship.__class__ == 'StarBace':
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
                    if ship.__class__ == 'StarBace':
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
        if fire_at and closest_p <= wepon.range*TERAMETER_2_LIGHTYEAR:
            return fire_at
        elif fire_att and closest_s <= wepon.range*TERAMETER_2_LIGHTYEAR:
            return fire_att
        else:
            return None
        pass

    def move(self, ship, ships):
        move = self.calc_strategy_m(ship)
        ship.location = ship.loction.move(move[0], ship.max_distance, move[1])
        self.save_to_cobat_log()
        pass

    def fire(self, ship):
        for wepon in ship.wepons:
            ship_to_fire_at = self.calc_strategy_f(ship, wepon)
            if ship_to_fire_at:
                damage = wepon.get_damage(ship.location-ship_to_fire_at.location, ship_to_fire_at.shealds, ship_to_fire_at.armor, ship.Scanner.range_visible(ship_to_fire_at.calc_aparent_mass()), ship_to_fire_at.ecm)
                ship_to_fire_at.shealds = damage[0]
                ship_to_fire_at.armor = damage[1]
            save_to_combat_log()
        pass


    def save_to_combat_log(self):
        pass

    save_to_combat_log()
    def take_turn(self):
        mi = 0
        for ship in self.everybody
            #ship.calc_initative()
            if ship.initative > mi:
                mi = int(ship.initative)
        for i in range(mi, -1, -1):
            for ship in ships:
                if ship.initative == i:
                    self.move(ship)
        for i in range(mi, -1, -1):
            for ship in self.everybody:
                if ship.initative == i:
                    self.fire(ship)



