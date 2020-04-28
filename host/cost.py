import game_engine

""" TODO """
class Cost:
    def __init__(self, energy, effort, silicon, lithium, titanium, production_capacity):
        self.production_capacity = int(production_capacity)
        self.titanium = int(titanium)
        self.lithium = int(lithium)
        self.silicon = int(silicon)
        self.energy = int(energy)
        self.effort = int(effort)

# Register the class with the game engine
game_engine.register_class(Cost)


def cost_test():
    test_cost = Cost(234, 249, 78, 27, 823, 100)
    if test_cost.energy != 234:
        print("energy Fail")
    if test_cost.effort != 249:
        print("effort Fail")
    if test_cost.silicon != 78:
        print("silicon Fail")
    if test_cost.lithium != 27:
        print("lithium Fail")
    if test_cost.titanium != 823:
        print("titanium Fail")
    if test_cost.production_capacity != 100:
        print("production_capacity Fail")
    print("tested Cost __init__()")
