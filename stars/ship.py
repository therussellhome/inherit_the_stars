import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
}


class Ship(Defaults):
    def move(self, speed):
        distance = round((((self.x - self.waypoint_x) **2) + ((self.y - self.waypoint_y) **2) + ((self.z - self.waypoint_z) **2))**.5)    
        new_x = self.x + ((speed**2)/distance)
        new_y = self.y + ((speed**2)/distance)
        new_z = self.z + ((speed**2)/distance)
        return new_x, new_y, new_z
    def orbital_mining(self, planet):
        if planet.colonized == False:
            ti = planet.titanium - (self.rate * planet.titanium)
            si = planet.silicon - (self.rate * planet.silicon)
            li = planet.lithium - (self.rate * planet.lithium)
            planet.on_surface.titanium += round((planet.titanium - ti) + .1)
            planet.on_surface.silicon += round((planet.silicon - si) + .1)
            planet.on_surface.lithium += round((planet.lithium - li) + .1)
            planet.titanium = ti
            planet.silicon = si
            planet.lithium = li
        return planet
    def repair(self, ship):
        if ship.damage_points > 0:
            ship.damage_points -= self.repair_points
        return ship
    def bomb(self, p):
        if p.colonized == True:
            if self.bomb.percent_pop_kill * p.num_colonists < self.bomb.minimum_kill:
                p.num_colonist -= self.bomb.minimum_kill
            else:
                p.num_colonists *= self.bomb.percent_pop_kill
            p.num_facilities -= self.bomb.percent_facilities_kill
            if p.num_colonists < 0:
                p.num_colonists = 0
            if p.num_facilities < 0
                p.num_facilities = 0
        return p
                
