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
        if not hasattr(self.player, 'planet_report') or len(self.player.planet_report) == 0:
            planets = []
            for (reference, intel) in self.player.get_intel(by_type='Planet').items():
                planets.append(self.process_intel(reference, intel))
            for (reference, intel) in self.player.get_intel(by_type='Sun').items():
                planets.append(self.process_intel(reference, intel, 'sun'))
            # Puts the report in the cache
            self.player.planet_report = planets
        else:
            planets = self.player.planet_report
        filtered_planets = self.planet_filter(planets, self.planets_filter)
        sorted_planets = self.planet_sort(filtered_planets, self.planets_field)
        for p in sorted_planets:
            self.planets_report.append('<td colspan="3"><table class="hfill collapse"><caption class="collapse"><div class="fa-angle-double-down collapse" onclick="toggle(this.parentElement.parentElement, \'collapse\')">' + str(p['name']) + '  $  ' + str(p[self.planets_field]) + '  $  ' + str(p['date']) + '</div></caption>')#'<tr class="collapse"><td class="collapse">' + str(p['name']) + '</td><td class="collapse">' + str(p[self.planets_field]) +'</td><td class="collapse">' + str(p['date']) + '</td></tr>')
            self.planets_report[-1] += '<tr class="collapse"><td class="collapse" colspan="3"><table class="hfill collapse">' + str(p['details']) + '</table></td></tr>'
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
        planet['Energy Generation'] = -1.0
        planet['Production Capacity'] = -1.0
        planet['Silicon Output'] = -1.0
        planet['Lithium Output'] = -1.0
        planet['Titanium Output'] = -1.0
        planet['Silicon On Surface'] = -1.0
        planet['Lithium On Surface'] = -1.0
        planet['Titanium On Surface'] = -1.0
        planet['Scanner Range'] = -1.0
        planet['Shield Coverage'] = -1.0
        planet['Total Facilities'] = -1.0
        planet['Power Plants'] = -1.0
        planet['Shild Genorators'] = -1.0
        planet['Factories'] = -1.0
        planet['Mines'] = -1.0
        if reference:
            planet['Inhabitant'] = str(getattr(intel, 'Player', 'uninhabited')) 
            if hasattr(intel, 'Player'):
                planet['Inhabitant'] += '(' + str(self.player.get_relation(getattr(intel, 'Player'))) + ')'
            reference.gravity = intel.gravity
            reference.temperature = intel.temperature
            reference.radiation = intel.radiation
            planet['Habitability'] = reference.habitability(self.player.race)
            planet['Gravity'] = intel.gravity
            planet['Temperature'] = intel.temperature
            planet['Radiation'] = intel.radiation
            pop = reference.on_surface.people
            planet['Population'] = str(pop)
            planet['Max Population'] = reference.maxpop(self.player.race)#store max_pop in intel? 
            planet['Capacity'] = pop / planet['Max Population']#getattr(intel, 'Population', '?')
            min_availability = reference.mineral_availability()
            planet['Silicon Availability'] = round(min_availability.silicon)
            planet['Lithium Availability'] = round(min_availability.lithium)
            planet['Titanium Availability'] = round(min_availability.titanium)
            if hasattr(intel, 'Player'):
                relation = self.player.get_relation(getattr(intel, 'Player'))
                if relation == 'me':
                    facility_yj =  round(reference._operate('power_plants') * (1 + .05 * self.player.tech_level.propulsion))
                    pop_yj = reference.on_surface.people * self.player.race.pop_per_kt() * self.player.race.energy_per_10k_colonists / 10000 / 100
                    planet['Energy Generation'] = '<i class="YJ">' + str(round((facility_yj + pop_yj) * 100)) + '</i>'
                    planet['Production Capacity'] = str(reference.operate_factories() * 100)
                    planet['Power Plants'] = reference.power_plants
                    planet['Shild Genorators'] = reference.defenses
                    planet['Factories'] = reference.factories
                    planet['Mines'] = reference.mineral_extractors
                    num_people = reference.on_surface.people * self.player.race.pop_per_kt()
                    planet['Population'] += ' / ' +str(round(num_people))
                    operate = reference._operate('mineral_extractors')
                    planet['Silicon Output'] = round(operate * min_availability.silicon)
                    planet['Lithium Output'] = round(operate * min_availability.lithium)
                    planet['Titanium Output'] = round(operate * min_availability.titanium)
                    planet['Silicon On Surface'] = round(reference.on_surface.silicon)
                    planet['Lithium On Surface'] = round(reference.on_surface.lithium)
                    planet['Titanium On Surface'] = round(reference.on_surface.titanium)
                    planet['Shield Coverage'] = str(reference.raise_shields())
                    planet['Scanner Range'] = str(round((self.player.race.pop_per_kt() * pop * 3.0 / 4.0 / math.pi * (self.player.tech_level.electronics + 1.0) / 3000.0) ** (1.0 / 3.0))) + ' / ' + str(round((reference.player.race.pop_per_kt() * pop * 3.0 / 4.0 / math.pi * (self.player.tech_level.electronics + 1.0) / 3000.0) ** (1.0 / 3.0) * 10.0))
                else:
                    planet['Total Facilities'] = reference.power_plants + reference.defenses + reference.factories + reference.mineral_extractors

        else:
            planet['Inhabitant'] = str(getattr(intel, 'Player', 'uninhabited')) 
            if hasattr(intel, 'Player'):
                planet['Inhabitant'] += '(' + str(self.player.get_relation(getattr(intel, 'Player'))) + ')'
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
        planet['details'] += '<tr class="collapse"><td class="collapse">Habitability</td><td class="collapse">' + str(planet['Habitability']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">    Gravity</td><td class="collapse">' + str(planet['Gravity']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">    Temperature</td><td class="collapse">' + str(planet['Temperature']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">    Radiation</td><td class="collapse">' + str(planet['Radiation']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">Population</td><td class="collapse">' + str(planet['Population']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">Capacity</td><td class="collapse">' + str(planet['Capacity']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">Max Population</td><td class="collapse">' + str(planet['Max Population']) + '</td></tr>'
        #planet['details'] += '<tr class="collapse"><td class="collapse">Energy Generation</td><td class="collapse">' + str(planet['Energy Generation']) + '</td></tr>'
        #planet['details'] += '<tr class="collapse"><td class="collapse">Production Capacity</td><td class="collapse">' + str(planet['Production Capacity']) + '</td></tr>'
        #planet['details'] += '<tr class="collapse"><td class="collapse">Scanner Range</td><td class="collapse">' + str(planet['Scanner Range']) + '</td></tr>'
        #planet['details'] += '<tr class="collapse"><td class="collapse">Shield Coverage</td><td class="collapse">' + str(planet['Shield Coverage']) + '</td></tr>'
        for attr in ['Total Facilities', 'Power Plants', 'Shild Genorators', 'Factories', 'Mines', 'Scanner Range', 'Shield Coverage', 'Energy Generation', 'Production Capacity', 'Silicon Output', 'Lithium Output', 'Titanium Output', 'Silicon On Surface', 'Lithium On Surface', 'Titanium On Surface']:
            if planet[attr] != -1.0:
                planet['details'] += '<tr class="collapse"><td class="collapse">' + str(attr) + '</td><td class="collapse">' + str(planet[attr]) + '</td></tr>'
            #planet['details'] += '<tr class="collapse"><td class="collapse">Silicon Output</td><td class="collapse">' + str(planet['Silicon Output']) + '</td></tr>'
            #planet['details'] += '<tr class="collapse"><td class="collapse">Titanium Output</td><td class="collapse">' + str(planet['Titanium Output']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">Lithium Availability</td><td class="collapse">' + str(planet['Lithium Availability']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">Silicon Availability</td><td class="collapse">' + str(planet['Silicon Availability']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">Titanium Availability</td><td class="collapse">' + str(planet['Titanium Availability']) + '</td></tr>'
        planet['details'] += '<tr class="collapse"><td class="collapse">Inhabitant</td><td class="collapse">' + str(planet['Inhabitant']) + '</td></tr>'
        if reference ^ 'Planet':
            planet['All Planets'] = True
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
