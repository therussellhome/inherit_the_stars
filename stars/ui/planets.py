from .playerui import PlayerUI
from ..planet import Planet
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
        if self.planets_filter == '':
            self.planets_filter = self.options_planets_filter[0]

        # Fields for comparasion
        fields = ['Habitability', 'Capacity', 'Population', 'Max Population', 'Energy Generation', 'Production Capacity', 'Scanner Range', 'Shield Coverage', \
        'Silicon Output', 'Lithium Output', 'Titanium Output', 'Silicon Availability', 'Lithium Availability', 'Titanium Availability']
        for f in fields:
            self.options_planets_field.append(f)
        if self.planets_field == '':
            self.planets_field = self.options_planets_field[0]
        
        # Checks to see whether it has to calculate it 
        # It's using cache so it doesn't have to calculate the report over and over again
        if not hasattr(self.player, 'planet_report') or len(self.player.planet_report) == 0:
            planets = []
            for (reference, intel) in self.player.get_intel(by_type='Planet').items():
                planets.append(self.process_intel(reference, intel))
            for (reference, intel) in self.player.get_intel(by_type='Sun').items():
                planets.append(self.process_intel(reference, intel, 'Sun'))
            # Puts the report in the cache
            self.player.planet_report = planets
        else:
            planets = self.player.planet_report
        filtered_planets = self.planet_filter(planets, self.planets_filter)
        sorted_planets = self.planet_sort(filtered_planets, self.planets_field)
        for p in sorted_planets:
            p = self.get_details(p)
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
    def process_intel(self, reference, intel, world_type='Planet'):
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
        planet['Shield Genorators'] = -1.0
        planet['Factories'] = -1.0
        planet['Mines'] = -1.0
        if reference and intel.date != self.player.race.start_date:
            planet['Inhabitant'] = str(getattr(intel, 'Player', 'uninhabited')) 
            if hasattr(intel, 'Player'):
                planet['Inhabitant'] += '(' + str(self.player.get_relation(getattr(intel, 'Player'))) + ')'
            if ((world_type == 'Planet' and self.player.race.primary_race_trait != 'Pa\'anuri') or (world_type == 'Sun' and self.player.race.primary_race_trait == 'Pa\'anuri')):
                tmp = Planet()
                tmp.gravity = intel.gravity
                tmp.temperature = intel.temperature
                tmp.radiation = intel.radiation
                planet['Habitability'] = tmp.habitability(self.player.race)
                del tmp
                planet['Gravity'] = intel.gravity
                planet['Temperature'] = intel.temperature
                planet['Radiation'] = intel.radiation
            else:
                planet['Habitability'] = -101.0
                planet['Gravity'] = '?'
                planet['Temperature'] = '?'
                planet['Radiation'] = '?'
            pop = reference.on_surface.people
            planet['Population'] = str(pop)
            planet['Max Population'] = reference.maxpop(self.player.race)#store max_pop in intel? 
            planet['Capacity'] = pop / planet['Max Population']#getattr(intel, 'Population', '?')
            min_availability = reference.mineral_availability()
            planet['Silicon Availability'] = round(min_availability.silicon, 2)
            planet['Lithium Availability'] = round(min_availability.lithium, 2)
            planet['Titanium Availability'] = round(min_availability.titanium, 2)
            if hasattr(intel, 'Player'):
                relation = self.player.get_relation(getattr(intel, 'Player'))
                if relation == 'me':
                    facility_yj =  round(reference._operate('power_plants') * (1 + .05 * self.player.tech_level.propulsion))
                    pop_yj = reference.on_surface.people * self.player.race.pop_per_kt() * self.player.race.energy_per_10k_colonists / 10000 / 100
                    planet['Energy Generation'] = round((facility_yj + pop_yj) * 100)
                    planet['Production Capacity'] = reference.operate_factories() * 100
                    planet['Power Plants'] = reference.power_plants
                    planet['Shield Genorators'] = reference.defenses
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

    def get_details(self, planet={}):
        planet['details'] = ''
        # Habitability
        for attr in ['Habitability', 'Gravity', 'Temperature', 'Radiation']:
            self.set_detail(planet, attr)
        # People
        for attr in ['Population', 'Capacity', 'Max Population']:
            self.set_detail(planet, attr)
        # facilities and output
        for attr in ['Total Facilities', 'Power Plants', 'Shield Genorators', 'Factories', 'Mines', 'Scanner Range', 'Shield Coverage', 'Energy Generation', 'Production Capacity']:
            if planet[attr] != -1.0:
                self.set_detail(planet, attr)
        # Minerals
        for attr in ['Titanium Availability', 'Titanium Output', 'Titanium On Surface', 'Lithium Availability', 'Lithium Output', 'Lithium On Surface', 'Silicon Availability', 'Silicon Output', 'Silicon On Surface']:
            if planet[attr] != -1.0:
                self.set_detail(planet, attr)

        self.set_detail(planet, 'Inhabitant')
        return planet

    def set_color(self, attr, value=None):
        color = ''
        if attr == 'Inhabitant':
            if 'me' in value:
                color = 'springgreen'
            elif 'team' in value:
                color = 'deepskyblue'
            elif 'enemy' in value:
                color = 'crimson'
        elif attr == 'Habitability':
            if value > self.player.colonize_min_hab and value > 0:
                color = 'limegreen'
            elif value > 0:
                color = 'lime'
            elif value > -10:
                color = 'yellow'
            else:
                color = 'red'
        elif value and type(value) is int:
            if self.player.race['hab_' + attr.lower() + '_immune']:
                color = 'limegreen'
            elif value in range(self.player.race['hab_' + attr.lower()], self.player.race['hab_' + attr.lower() + '_stop']):
                color = 'lime'
            elif value in range(self.player.race['hab_' + attr.lower()] - 5, self.player.race['hab_' + attr.lower()]) or value in range(self.player.race['hab_' + attr.lower() + '_stop'], self.player.race['hab_' + attr.lower() + '_stop'] + 5):
                color = 'yellow'
            else:
                color = 'red'
        elif attr == 'Mines' or 'Ti' in attr or 'Li' in attr or 'Si' in attr:
            color = 'tan'
        elif 'Production' in attr or 'Factories' in attr:
            color = 'orchid'
        elif 'Shield' in attr:
            color = 'lightskyblue'
        elif 'Power' in attr or 'Energy' in attr:
            color = 'cyan'
        if 'Scan' in attr:
            color = 'pink'
        if color != '':
            color = '" style="color: ' + color
        return color

    def set_class(self, attr):
        iclass = ''
        if attr == 'Energy Generation':
            iclass = 'fa-bolt'
        elif 'Ti' in attr:
            iclass = 'ti'
        elif 'Li' in attr:
            iclass = 'li'
        elif 'Si' in attr:
            iclass = 'si'
        if 'Availability' in attr:
            iclass += ' col'
        return iclass

    def set_detail(self, planet, attr):
        value = planet[attr]
        if attr in ['Habitability', 'Gravity', 'Temperature', 'Radiation', 'Inhabitant']:
            color = self.set_color(attr, value)
        else:
            color = self.set_color(attr)
        iclass = self.set_class(attr)
        if 'i' in iclass:
            color1 = ''
        else:
            color1 = color
        planet['details'] += '<tr class="collapse"><td class="collapse' + color + '">' + str(attr) + '</td><td class="collapse"><i class="' + iclass + color1 + '">' + str(value) + '</i></td></tr>'


Planets.set_defaults(Planets, __defaults, sparse_json=False)
