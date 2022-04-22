from .defaults import Defaults
from .stars_math import TERAMETER_2_LIGHTYEAR
from copy import copy

def distance(ship1, ship2):
    return (ship1.ship.location-ship2.ship.location)

# battle plan; two dropdowns:
# how to engage; run away, max damage(get in close), longrange
# what to engage; most massive, most thretening, closest
# ships cloaked to zero do not fire until at destonation or fired apoun

__defaults = {
    'date': 0.0
}

class Combat(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #everyone = []
        #self.players = []
    
    def get_most_thretening(self, everyone):
        return everyone[0]
    
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
        everyone.sort(key=lambda ship: distance(ship, me))
        if me.method == 'runaway' or len(me.ship.weapons) == 0:
            return (everyone[0].location, True)
        if me.priority == 'closest':
            return (everyone[0].location, False)
        if me.priority == 'most massive':
            everyone.sort(key=lambda ship: ship.mass, reverce=True)
            return (everyone[0].location, False)
        if me.priority == 'most thretening':
            get_most_thretening(self, everyone)
        for ship in everyone:
            if not (ship is me) and not (me.player in ship.hidden_from): # and me.player.relashons(ship.player) == 'enemy':
                if me.battle_plan.p_target == 'disengage' or len(me.ship.weapons) == 0:
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        move_to = ship.ship.location
                    excape = True
    
    def move(self, ship):
        move = self.calc_strategy_m(ship)
        standoff = 0
        ship.ship.location = ship.ship.location.move(move[0], self.calc_speed(ship)*TERAMETER_2_LIGHTYEAR, move[1], standoff)
        self.save_to_combat_log()
        pass
    
    """ calculates the ship to fire at"""
    def calc_strategy_f(self, me):
        closest_p = 1021
        closest_s = 1021
        fire_at = None
        fire_att = None
        for ship in everyone:
            if not ship is me and not me.player in ship.hidden_from: # and me.player.relashons(ship.player) == 'enemy':
                if me.battle_plan.p_target == 'any':
                    dis = distance(me, ship)
                    if dis < closest_p:
                        closest_p = dis
                        fire_at = ship
                elif me.battle_plan.p_target == 'starbase':
                    if ship.ship.is_starbase:
                        dis = distance(me, ship)
                        if dis < closest_p:
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
                    if ship.ship.is_starbase:
                        dis = distance(me, ship)
                        if dis < closest_s:
                            closest_s = dis
                            fire_att = ship
                elif me.battle_plan.s_target == 'ship':
                    if not ship.ship.is_starbase:
                        dis = distance(me, ship)
                        if dis < closest_s:
                            closest_s = dis
                            fire_att = ship
        if me.battle_plan.wait_until_closed_to_fire and distance(me, ship) > me.battle_plan.standoff:
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
                if damage == (0, 0) and ship.ship.location-ship_to_fire_at.ship.location <= weapon.range_tm*TERAMETER_2_LIGHTYEAR:
                    ship_to_fire_at.ship.expirence.battle_expirence += 0.05
                else:
                    ship.ship.expirence.battle_expirence += 0.1
                ship_to_fire_at.ship.shields_damage += damage[0]
                ship_to_fire_at.ship.armor_damage += damage[1]
                if ship_to_fire_at.ship.armor <= ship_to_fire_at.ship.armor_damage:
                    ship.ship.blow_up()
                    for ship3 in everyone:
                        while True:
                            try:
                                ship3.to_fire_at.remove(ship_to_fire_at)
                            except:
                                break
                    everyone.remove(ship_to_fire_at)
                ship_to_fire_at.to_fire_at.append(ship)
                ship.hidden_from = []
            self.save_to_combat_log()
        pass
    
    def fight(self, ships):
        everyone, players = self.get_ships(ships)
        for ship in everyone:
            for ship2 in everyone:
                if not ship.player is ship2.player:
                    if ship.player.treaties[ship2.player.name].relation == 'Enemy':
                        ship.to_fire_at.append(ship2)
        no_anti_cloak = copy(self.players)
        for ship in everyone:
            if ship.ship.scanner.anti_cloak > 0:
                no_anti_cloak.remove(ship.player)
        for ship in everyone:
            if ship.ship.calc_apparent_mass() == 0:
                ship.hidden_from = no_anti_cloak
        i=0
        while 2048:
            self.turn()
            csf = []
            for ship in everyone:
                csf.append(len(ship.to_fire_at) == 0)
            if all(csf):
                for ship in everyone:
                    ship.shields_damage = 0
                break
            i+=1
                
    def turn(self):
        everyone.sort(key=lambda ship: ship.ship['expirence'])
        for ship in everyone:
            self.move(ship)
        everyone.sort(key=lambda ship: ship.ship['expirence'], reverse=True)
        for ship in everyone:
            self.fire(ship)
    
    def get_ships(self, ships):
        everyone = []
        players = []
        for ship in ships:
            battle_plan = ship['fleet']['orders']
            s = _ship(ship, player, battle_plan)
            everyone.append(s)
            if not s.player in players:
                players.append(s.player)
        return everyone, players
    
    def calc_speed(self, ship):
        speed = []
        for e in ship.ship.engines:
            speed.append(e.speed_at_tach_100(ship.ship.mass, 0)/20)
        if len(speed) == 0:
            speed.append(0.05)
        return min(speed)
    


class _ship():
    def __init__(self, ship, battle_plan):
        self.ship = ship
        self.player = ship['player']
        self.method = battle_plan.how_to_engage
        self.priority = battle_plan.what_to_engage
        self.has_stot = False
        self.hidden_from = []
        self.to_fire_at = []
    

Combat.set_defaults(Combat, __defaults)
