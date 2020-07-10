from random import random
from math import cos, sin, pi, atan2

def calc_strategy_m(me, everybody):
    closest_p = 1021
    closest_s = 1021
    m_lat = 0
    m_lon = 0
    m_dis = 1021
    move_to = None
    move_two = None
    excape = False
    excape2 = False
    for ship in everybody:
        if me.player.relashons(ship.player) == 'enemy' and me.can_see(ship):
            if me.BattlePlan.1st_target == 'any':
                dis = distance(me, ship)
                if dis < closest_p:
                    closest_p = dis
                    move_to = ship.location
            elif me.BattlePlan.1st_target == 'disengage':
                dis = distance(me, ship)
                if dis < closest_p:
                    closest_p = dis
                    move_to = ship.location
                excape = True
            elif me.BattlePlan.1st_target == 'starbase':
                if ship.__class__ == 'StarBace':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        move_to = ship.location
            elif me.BattlePlan.1st_target == 'ship':
                if not ship.__class__ == 'StarBase':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        move_to = ship.location
            if me.BattlePlan.2nd_target == 'any':
                dis = distance(me, ship)
                if dis < closest_s:
                    closest_s = dis
                    move_two = ship.location
            elif me.BattlePlan.2nd_target == 'disengage':
                dis = distance(me, ship)
                if dis < closest_s:
                    closest_s = dis
                    move_two = ship.location
                excape2 = True
            elif me.BattlePlan.2nd_target == 'starbase':
                if ship.__class__ == 'StarBace':
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        move_two = ship.location
            elif me.BattlePlan.2nd_target == 'ship':
                if not ship.__class__ == 'StarBase':
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        move_two = ship.location
    if move_to:
        if not excape:
            m_dis = closest_p
        m_lat = atan2(move_to.y, move_to.x)
        m_lon = atan2(move_to.x, move_to.z)
        if excape:
            m_lon += pi
    elif move_two:
        if not excape2:
            m_dis = closest_s
        m_lat = atan2(move_two.y, move_two.x)
        m_lon = atan2(move_two.x, move_two.z)
        if excape2:
            m_lon += pi
    else:
        m_dis = 0
    return [m_dis, m_lat*180/pi, m_lon*180/pi]

def calc_strategy_f(me, everybody, wepon):
    closest_p = 1021
    closest_s = 1021
    fire_at = None
    fire_att = None
    for ship in everybody:
        if me.player.relashons(ship.player) == 'enemy' and me.can_see(ship):
            if me.BattlePlan.1st_target == 'any':
                dis = distance(me, ship)
                if dis < closest_p:
                    closest_p = dis
                    fire_at = ship
            elif me.BattlePlan.1st_target == 'starbase':
                if ship.__class__ == 'StarBace':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        fire_at = ship
            elif me.BattlePlan.1st_target == 'ship':
                if not ship.__class__ == 'StarBase':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        fire_at = ship
            if me.BattlePlan.2nd_target == 'any':
                dis = distance(me, ship)
                if dis < closest_s:
                    closest_s = dis
                    fire_att = ship 
            elif me.BattlePlan.2nd_target == 'starbase':
                if ship.__class__ == 'StarBace':
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        fire_att = ship
            elif me.BattlePlan.2nd_target == 'ship':
                if not ship.__class__ == 'StarBase':
                    dis = distance(me, ship)
                    if dis < closest_s:
                        closest_s = dis
                        fire_att = ship
    if fire_at and closest_p <= wepon.range:
        return fire_at
    elif fire_att and closest_s <= wepon.range:
        return fire_att
    else:
        return None
    pass

def move(ship, ships):
    move = calc_strategy_m(ship, ships)
    moved = polar_to_cartesion(min(ship.movement, move[0]), move[1], move[2])
    ship.location.x += moved[0]
    ship.location.y += moved[1]
    ship.location.z += moved[2]
    save_to_cobat_log()
    pass

def distance(ship1, ship2):
    return ((ship1.location.x-ship2.location.x)**2 + (ship1.location.y-ship2.location.y)**2 + (ship1.location.z-ship2.location.z)**2)**0.5

def fire(ship, ships):
    for wepon in ship.wepons:
        ship_to_fire_at = calc_strategy_f(ship, ships, wepon)
        if ship_to_fire_at:
            accuracy = calc_accuacy(ship, wepon)
            if random <= accuracy:
                damage = calc_net_damage(ship, wepon)
                Adamage = 0
                if wepon.type == 'misile':
                    Adamage = damage/4
                    damage *= 3/4
                while ship_to_fire_at.shealds > 0 and damage > 0:
                    ship.ship_to_fire_at.shealds -= 1
                    damage -= 1:
                while ship_to_fire_at.armor > 0 and (damage > 0 or Adamage > 0):
                    if damage > 0:
                        damage -= 1
                    elif Adamage > 0:
                        Adamage -= 1
                    else:
                        break
                    ship.ship_to_fire_at.armor -= 1
        save_to_combat_log()
    pass

def polar_to_cartesian(dis, lat, lon):
    x = round(cos(lat*pi/180)*dis*cos(lon*pi/180), 5)
    y = round(sin(lat*pi/180)*dis*cos(lon*pi/180), 5)
    z = round(sin(lon*pi/180)*dis, 5)
    return [x, y, z]

def save_to_combat_log():
    pass

class combat():
    save_to_combat_log()
    def take_turn():
        mi = 0
        for ship in ships:
            calc_initative(ship)
            if ship.initative > mi:
                mi = int(ship.initative)
        for i in range(mi, -1, -1):
            for ship in ships:
                if ship.initative = i:
                    move(ship, ships)
        for i in range(mi, -1, -1):
            for ship in ships:
                if ship.initative = i:
                    fire(ship, ships)



