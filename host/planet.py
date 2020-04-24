""" Planet class """
class Planet(object):
    """ Restore class from a string """
    def __init__(self, from_string):
        pass

    """ Create an empty class """
    def __init__(self):
        pass

    """ Grow the current population """
    def grow_population(self):
        pass

    """ runs the  """
    def take_turn(self):
        self.growPopulation()
        self.calcEffort()
        self.generateMoney()
        self.payTaxes()
        self.recvStimulus()
        self.mineMinerals()
        self.buildStuff()
        self.donateSurplus()

""" Test the Planet class """
def _test():
    print('planet._test - begin')
    _test_grow_population()
    print('planet._test - end')

""" Test the Planet.grow_population method """
def _test_grow_population():
    print('planet._test_grow_population - begin')
    p = Planet()
    p.grow_population()
    print('planet._test_grow_population - end')
