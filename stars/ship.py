import sys
from . import game_engine
from .defaults import Defaults
from random import randint


""" Default values (default, min, max)  """
__defaults = {
}


class Ship(Defaults):
    """ Moves on the ship level """
    """ If it has no engines it does an early exit with the empty return """
    def move(self, speed):
        if len(self.engines) == 0:
            return
        distance = round((((self.x - self.waypoint.x) **2) + ((self.y - self.waypoint.y) **2) + ((self.z - self.waypoint.z) **2))**.5)    
        self.x = self.x + ((speed**2)/distance)
        self.y = self.y + ((speed**2)/distance)
        self.z = self.z + ((speed**2)/distance)

    """ Calculates how much fuel it will take to move """
    """ Coded for use of the fleet """
    """ If there are no engines it returns 0 because it doesn't use any fuel """
    def fuel_check(self, speed, in_hyper_denial, distance):
        if len(self.engines) == 0:
            return 0
        fuel = 0
        mass_per_engine = self.mass/len(self.engines)
        mass_per_tachometer = mass_per_engine
        if in_hyper_denial:
            mass_per_tachometer = mass_per_engine * speed
        for engine in self.engines:
            fuel += engine.tachometer(speed, mass_per_tachometer) * mass_per_engine * distance
        return fuel

    """ Mines the planet if it is not colonized """
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

    """ Repairs the ship if it needs it """
    def repair(self, ship):
        if ship.damage_points > 0:
            ship.damage_points -= self.repair_points
        return ship

    """ Bombs the planet if the planet is colonized """
    def bomb(self, p):
        if p.colonized == True:
            if self.bomb.percent_pop_kill * p.num_colonists < self.bomb.minimum_kill:
                p.num_colonist -= self.bomb.minimum_kill
            else:
                p.num_colonists *= self.bomb.percent_pop_kill
            p.num_facilities -= self.bomb.percent_facilities_kill
            if p.num_colonists < 0:
                p.num_colonists = 0
            if p.num_facilities < 0:
                p.num_facilities = 0
        return p            
