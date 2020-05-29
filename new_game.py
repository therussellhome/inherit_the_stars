#!/usr/bin/python

from . import game_engine
from . import star_system
from random import randint
from random import random
from math import pi


""" Put the system names in a list """
with open('host/star_system.names') as file:
    names = []
    for name in file:
        names.append(name.strip())
game_engine.save_game('games/new_game.zip')

""" Set the game name and the density x"""
game_name = str(input('game name:'))

while True:
    density = input('density (1..100):')
    try:
        density = int(density)
    except:
        pass
    if density in range(1, 101):
        break
    print('invalid input')

""" Set the dimensions x"""
x = -1
y = -1
z = -1
while True:
    x = input('x diameter (0...100):')
    y = input('y diameter (0...100):')
    z = input('z diameter (0...100):')
    try:
        x = int(x)
        y = int(y)
        z = int(z)
    except:
        pass
    if x in range(0, 101) and y in range(0, 101) and z in range(0, 101) and x + y + z in range(1, 301):
       break
    print('invalid input')

""" Calculate the volume in cubic light centuries """
dimension = 3
if x == 0 or x == 1:
    dimension -= 1
    x = 2
if y == 0 or y == 1:
    dimension -= 1
    y = 2
if z == 0 or z == 1:
    dimension -= 1
    z = 2
volume = ((4/3)*pi)*(x/2)*(y/2)*(z/2)/(100**dimension)

""" Calculate the number of systems x"""
num_systems = round(volume * density)
min_systems = 3
default_systems = 100
if num_systems not in range(min_systems, len(names)):
    print('invalid input:', num_systems, 'is not between', min_systems, 'and', len(names))
    num_systems = default_systems

""" Print the universe information """
if dimension == 3:
    if x == y and y == z:
        shape = 'sphere'
    else:
        shape = 'elipsoid'
elif dimension == 2:
    if x == y:
        shape = 'circle'
    else:
        shape = 'elipse'
if dimension == 1:
    print('this universe is a 1-dimensional', x, 'lightyear long line with', num_systems, 'systems')
elif dimension == 2:
    print('this universe is a 2-dimensional', x, 'by', y, shape, 'with', num_systems, 'systems and an area of', round(volume * (100**dimension)), 'square lightyears')
elif dimension == 3:
    print('this universe is a 3-dimensional', x, 'by', y, 'by', z, shape, 'with', num_systems, 'systems and a volume of', round(volume * (100**dimension)), 'cubic lightyears')

"""Create the systems x"""
""" rx = x coordinate """
""" ry = y coordinate """
""" rz = z coordinate """
systems = []
while len(systems) < num_systems:
    rx = (random() * 2) -1
    ry = (random() * 2) -1
    rz = (random() * 2) -1
    distance = ((rx**2) + (ry**2) + (rz**2))**.5 
    if distance <= 1 and distance >= -1:
        rx = round(rx * (x/2))
        ry = round(ry * (y/2))
        rz = round(rz * (z/2))
        for s in systems:
            counter = 0
            if s.x == rx and s.y == ry and s.z == rz:
                counter += 1
                break
            if counter == 100:
                print('too many systems')
                break
        else:
            counter = 0
            system_name = names.pop(randint(0, len(names) - 1))
            s = star_system.StarSystem(name=system_name, x=rx, y=ry, z=rz)
            systems.append(s)
game_engine.save_game('games/new_game.zip')

""" Set the number of players x"""
while True:
    num_players = input('number of players (1...16):')
    try:
        num_players = int(num_players)
    except:
        pass
    if num_players in range(1, 17):
        break
    print('invalid input')

""" Set the distance between players x """
while True:
    if num_players == 1:
        break
    player_distance = input('distance between players:')
    try:
        player_distance = int(player_distance)
    except:
        pass
    if player_distance in range(1, 51):
        break
    print('invalid input')

""" Generate the home systems x"""
home_systems = []
home_systems.append(systems[0])
if num_players == 1:
    pass 

"""    else:
        for i in systems:
            p = ''
            for k in home_systems:
                    if round((((i.x - k.x)**2) + ((i.y - k.y)**2) + ((i.z - k.z)**2))**.5) < player_distance:    
                        p += 'fail'
                    elif round((((i.x - k.x)**2) + ((i.y - k.y)**2) + ((i.z - k.z)**2))**.5) >= player_distance:
                        p += 'pass'
            if 'fail' not in p:
                home_systems.append(i)
            if len(home_systems) == num_players:
                break
            if i == systems[len(systems) - 1] and len(home_systems) < num_players:
                player_distance *= .9
        # Output:
        #if dimension == 3:
            #if x == y and y == z:
                #shape = 'sphere'
            #else:
                #shape = 'elipsoid'
        #elif dimension == 2:
            #if x == y:
                #shape = 'circle'
            #else:
                #shape = 'elipse'
        #if dimension == 1:
            #print('this universe is a 1-dimensional', x, 'lightyear long line with', num_systems, 'systems')
        #elif dimension == 2:
            #print('this universe is a 2-dimensional', x, 'by', y, shape, 'with', num_systems, 'systems and an area of', round(volume * (100**dimension)), 'square lightyears')
        #elif dimension == 3:
            #print('this universe is a 3-dimensional', x, 'by', y, 'by', z, shape, 'with', num_systems, 'systems and a volume of', round(volume * (100**dimension)), 'cubic lightyears')
"""
