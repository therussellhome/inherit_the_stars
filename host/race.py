import to_json

""" Storage class for race parameters """
""" growth_rate int(0..20) """
""" temperature_start int(0..100) """
""" temperature_stop int(0..100) """
""" temperature_immune bool """
""" radiation_start int(0..100) """
""" radiation_stop int(0..100) """
""" radiation_immune bool """
""" gravity_start int(0..100) """
""" gravity_stop int(0..100) """
""" gravity_immune bool """
class Race(to_json.Serializable):
    pass
#    def __init__(self:q, **kwargs):
#        self.
#        self.growth_rate = int(growth_rate)
#        self.temprature = (int(temperature.
#        self.people = people
#        self.titanium = titanium
#        self.lithium = lithium
#        self.silicon = silicon
#        self.cargo_max = cargo_max
