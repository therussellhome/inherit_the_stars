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
        self.grow_population()
        self.calculate_effort()
        self.pay_effort_tax()
        self.generate_energy()
        self.pay_energy_tax()
        self.recv_stimulus()
        self.mine_minerals()
        self.build_stuff()
        self.donate_surplus()
    
    """  """
    def calculate_effort(self):
        self.effort = round((self.population + 1) * (self.player.effort_efficency/100) / 2)
    
    """  """
    def generate_energy(self):
        pass
    
    """  """
    def pay_effort_tax(self):
        if not self.is_tax_haven:
            tax_effort = round(self.__effort * (self.player.research_rate/100))
            self.player.__effort += tax_effort
            self.__effort -= tax_effort
    
    """  """
    def pay_energy_tax(self):
        if not self.is_tax_haven:
            tax_energy = round(self.__energy * (self.player.tax_rate/100))
            self.player.__energy += tax_energy
            self.__energy -= tax_energy
    
    """  """
    def recv_stimulus(self):
        stimulus_package = round(self.__population * self.player.stimulus_package / 1000)
        self.energy += stimulus_package
        self.player.energy -= stimulus_package
    
    """  """
    def mine_minerals(self):
        #self.minerals += round(10 * self.mines * self.mine_level * (self.player.mine_efficency/100))
        pass
    
    """  """
    def build_stuff(self):
        for item in self.build_queue:
            s_item = item.split(":")
            for i in range(int(s_item[1])):
                if s_item[0] == "uf" and self.player.research_level > self.factory_level:
                    factory_upgrade_cost_minerals = round(0.01 * self.factory_level * self.player.factory_cost.minerals * (self.factories))
                    factory_upgrade_cost_money = round(0.01 * self.factory_level * self.player.factory_cost.money * (self.factories))
                    factory_upgrade_cost_effort = round(0.01 * self.factory_level * self.player.factory_cost.effort * (self.factories))
                    if self.minerals >= factory_upgrade_cost_minerals and self.money >= factory_upgrade_cost_money and self.effort >= factory_upgrade_cost_effort:
                        self.minerals -= factory_upgrade_cost_minerals
                        self.money -= factory_upgrade_cost_money
                        self.effort -= factory_upgrade_cost_effort
                        self.factory_level += 1
                if s_item[0] == "um" and self.player.research_level > self.mine_level:
                    mine_upgrade_cost_minerals = round(0.01 * self.mine_level * self.player.mine_cost.minerals * (self.mines))
                    mine_upgrade_cost_money = round(0.01 * self.mine_level * self.player.mine_cost.money * (self.mines + 1))
                    mine_upgrade_cost_effort = round(0.01 * self.mine_level * self.player.mine_cost.effort * (self.mines + 1))
                    if self.minerals >= mine_upgrade_cost_minerals and self.money >= mine_upgrade_cost_money and self.effort >= mine_upgrade_cost_effort:
                        self.minerals -= mine_upgrade_cost_minerals
                        self.money -= mine_upgrade_cost_money
                        self.effort -= mine_upgrade_cost_effort
                        self.mine_level += 1
                if s_item[0] == "f" and self.minerals >= self.player.factory_cost.minerals and self.money >= self.player.factory_cost.money and self.effort >= self.player.factory_cost.effort:
                    self.minerals -= self.player.factory_cost.minerals
                    self.money -= self.player.factory_cost.money
                    self.effort -= self.player.factory_cost.effort
                    self.factories += 1
                if s_item[0] == "m" and self.minerals >= self.player.mine_cost.minerals and self.money >= self.player.mine_cost.money and self.effort >= self.player.mine_cost.effort:
                    self.minerals -= self.player.mine_cost.minerals
                    self.money -= self.player.mine_cost.money
                    self.effort -= self.player.mine_cost.effort
                    self.mines += 1
    
    """ give player extra and set energy and effort to 0 """
    def donate_surplus(self):
        self.player.__energy += self.__energy
        self.__energy = 0
        self.player.__effort += self.__effort
        self.__effort = 0


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
