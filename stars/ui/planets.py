from .playerui import PlayerUI
import math


""" Default values (default, min, max)  """
__defaults = {
    'options_planets_filter': [],
    'planets_filter': 'My Planets',
    'planets_report': [],
    'options_planets_field': [],
    'planets_field': 'Habitability',
}


""" """
class Planets(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return

        # Planets filter
        filters = ['My Planets', 'Team planets', 'Neutral Planets', 'Enemy Planets', 'Uninhabited Planets', 'All Planets', 'All Suns']
        for f in filters:
            self.options_planets_filter.append(f)

        # Fields for comparasion
        fields = ['Habitability', 'Capacity', 'Population', 'Max Population', 'Energy Generation', 'Production Capacity', 'Scanner Range', 'Shield Coverage', \
        'Silicon Output', 'Lithium Output', 'Titanium Output', 'Silicon Availability', 'Lithium Availability', 'Titanium Availability']
        for f in fields:
            self.options_planets_field.append(f)
        
        # Checks to see whether it has to calculate it 
        # It's using cache so it doesn't have to calculate the report over and over again
        if True or not hasattr(self.player, 'planet_report') or len(self.player.planet_report) == 0:
            print('no preprepared planet reports')
            planets = []
            print('race.g_start', self.player.race.hab_gravity)
            print('race.g_stop', self.player.race.hab_gravity_stop)
            print('race.t_start', self.player.race.hab_temperature)
            print('race.t_stop', self.player.race.hab_temperature_stop)
            print('race.r_start', self.player.race.hab_radiation)
            print('race.r_stop', self.player.race.hab_radiation_stop)
            for (reference, intel) in self.player.get_intel(by_type='Planet').items():
                planets.append(self.process_intel(reference, intel))
            for (reference, intel) in self.player.get_intel(by_type='Sun').items():
                planets.append(self.process_intel(reference, intel, 'sun'))
            # Puts the report in the cache
            self.player.planet_report = planets
        else:
            print('you previously prepared planets reports')
            planets = self.player.planet_report
        filtered_planets = self.planet_filter(planets, self.planets_filter)
        sorted_planets = self.planet_sort(filtered_planets, self.planets_field)
        for p in sorted_planets:
            self.planets_report.append('<td colspan="3"><table class="hfill"><caption><div class="fa-angle-double-down" onclick="toggle(this.parentElement.parentElement, \'collapse\')">' + str(p['name']) + '</div></caption><tr><td>' + str(p['name']) + '</td><td>' + str(p[self.planets_field]) +'</td><td>' + p['date'] + '</td></tr>')
            self.planets_report[-1] += '<tr><td colspan="3"><table class="hfill">' + str(p['details']) + '</table></td></tr>'
            self.planets_report[-1] += '</table></td>'
            
    def planet_filter(self, planets, planet_type):
        #filters = ['My Planets', 'Team planets', 'Neutral Planets', 'Enemy Planets', 'Uninhabited Planets', 'All Planets', 'All Suns']
        filtered_planets = []
        for planet in planets:
            if planet_type in planet and planet[planet_type]:
                filtered_planets.append(planet)
        print(len(filtered_planets))
        return filtered_planets

    def planet_sort(self, planets, planet_field):
        #fields = ['Habitability', 'Capacity', 'Population', 'Max Population', 'Energy Generation', 'Production Capacity', 'Scanner Range', 'Shield Coverage', \
        #'Mineral Output', 'Mineral Availability']
        sorted_planets = sorted(planets, key=lambda planet: planet[planet_field], reverse=True)
        return sorted_planets

    """ Common intel processing planet and sun """
    def process_intel(self, reference, intel, world_type='planet'):
        planet = {'name': intel.name, 'details': ''}
        planet['date'] = intel.date
        planet['World Type'] = str(world_type)
        if reference:
            planet['Inhabitant'] = str(getattr(intel, 'Player', 'uninhabited')) 
            if hasattr(intel, 'Player'):
                planet['Inhabitant'] += '(' + str(self.player.get_relation(getattr(intel, 'Player'))) + ')'
            planet['Habitability'] = reference.habitability(self.player.race)
            planet['Gravity'] = intel.gravity
            planet['Temperature'] = intel.temperature
            planet['Radiation'] = intel.radiation
            num_people = getattr(intel, 'Population', '?')
            pop = reference.on_surface.people
            planet['Population'] = pop
            planet['Max Population'] = reference.maxpop(self.player.race)#store max_pop in intel? 
            planet['Capacity'] = pop / planet['Max Population']#getattr(intel, 'Population', '?')
            planet['Energy Generation'] = '<i class="YJ">' + str(reference.generate_energy() * 100) + '</i>'
            planet['Production Capacity'] = str(reference.operate_factories() * 100)
            planet['Scanner Range'] = str((self.player.race.pop_per_kt() * pop * 3.0 / 4.0 / math.pi * (self.player.tech_level.electronics + 1.0) / 3000.0) ** (1.0 / 3.0)) + '/' + str((reference.player.race.pop_per_kt() * pop * 3.0 / 4.0 / math.pi * (self.player.tech_level.electronics + 1.0) / 3000.0) ** (1.0 / 3.0) * 10.0)
            planet['Shield Coverage'] = str(reference.raise_shields())
            min_availability = reference.mineral_availability()
            planet['Silicon Availability'] = min_availability.silicon
            planet['Lithium Availability'] = min_availability.lithium
            planet['Titanium Availability'] = min_availability.titanium
            operate = reference._operate('mineral_extractors')
            planet['Silicon Output'] = operate * min_availability.silicon
            planet['Lithium Output'] = operate * min_availability.lithium
            planet['Titanium Output'] = operate * min_availability.titanium
        else:
            planet['Inhabitant'] = str(getattr(intel, 'Player', 'uninhabited')) 
            if hasattr(intel, 'Player'):
                planet['Inhabitant'] += '(' + str(self.player.get_relation(getattr(intel, 'Player'))) + ')'
            planet['Energy Generation'] = '?'
            planet['Production Capacity'] = '?'
            planet['Scanner Range'] = '?'
            planet['Shield Coverage'] = '?'
            planet['Silicon Output'] = -1.0
            planet['Lithium Output'] = -1.0
            planet['Titanium Output'] = -1.0
            planet['Habitability'] = -101.0
            planet['Gravity'] = '?'
            planet['Temperature'] = '?'
            planet['Radiation'] = '?'
            planet['Population'] = getattr(intel, 'Population', -1.0)
            planet['Capacity'] = getattr(intel, 'capacity', -1.0)
            planet['Max Population'] = getattr(intel, 'max_pop', -1.0)
            planet['Lithium Availability'] = getattr(intel, 'Lithium availability', -1.0)
            planet['Silicon Availability'] = getattr(intel, 'Silicon availability', -1.0)
            planet['Titanium Availability'] = getattr(intel, 'Titanium availability', -1.0)
        planet['details'] += '<tr><td>Habitability</td><td>' + str(planet['Habitability']) + '</td></tr>'
        planet['details'] += '<tr><td>    Gravity</td><td>' + str(planet['Gravity']) + '</td></tr>'
        planet['details'] += '<tr><td>    Temperature</td><td>' + str(planet['Temperature']) + '</td></tr>'
        planet['details'] += '<tr><td>    Radiation</td><td>' + str(planet['Radiation']) + '</td></tr>'
        planet['details'] += '<tr><td>Population</td><td>' + str(planet['Population']) + '</td></tr>'
        planet['details'] += '<tr><td>Capacity</td><td>' + str(planet['Capacity']) + '</td></tr>'
        planet['details'] += '<tr><td>Max Population</td><td>' + str(planet['Max Population']) + '</td></tr>'
        planet['details'] += '<tr><td>Energy Generation</td><td>' + str(planet['Energy Generation']) + '</td></tr>'
        planet['details'] += '<tr><td>Production Capacity</td><td>' + str(planet['Production Capacity']) + '</td></tr>'
        planet['details'] += '<tr><td>Scanner Range</td><td>' + str(planet['Scanner Range']) + '</td></tr>'
        planet['details'] += '<tr><td>Shield Coverage</td><td>' + str(planet['Shield Coverage']) + '</td></tr>'
        planet['details'] += '<tr><td>Lithium Output</td><td>' + str(planet['Lithium Output']) + '</td></tr>'
        planet['details'] += '<tr><td>Silicon Output</td><td>' + str(planet['Silicon Output']) + '</td></tr>'
        planet['details'] += '<tr><td>Titanium Output</td><td>' + str(planet['Titanium Output']) + '</td></tr>'
        planet['details'] += '<tr><td>Lithium Availability</td><td>' + str(planet['Lithium Availability']) + '</td></tr>'
        planet['details'] += '<tr><td>Silicon Availability</td><td>' + str(planet['Silicon Availability']) + '</td></tr>'
        planet['details'] += '<tr><td>Titanium Availability</td><td>' + str(planet['Titanium Availability']) + '</td></tr>'
        planet['details'] += '<tr><td>Inhabitant</td><td>' + str(planet['Inhabitant']) + '</td></tr>'
        if reference ^ 'Planet':
            planet['All Planets'] = True
            print('planet:', reference.__reference__)
            print('  *  gravity:',  reference.gravity)
            print('  *  temperature:',  reference.temperature)
            print('  *  radiation:',  reference.radiation)
            print('  *  habitability:',  reference.habitability(self.player.race))
        else:
            planet['All Suns'] = True
        if not hasattr(intel, 'Player'):
            planet['Uninhabited Planets'] = True
        else:
            relation = self.player.get_relation(getattr(intel, 'Player'))
            if relation == 'me':
                planet['My Planets'] = True
            elif relation == 'team':
                planet['Team Planets'] = True
            elif relation == 'neutral':
                planet['Neutral Planets'] = True
            elif relation == 'enemy':
                planet['Enemy Planets'] = True
        return planet

Planets.set_defaults(Planets, __defaults, sparse_json=False)
