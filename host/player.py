import game_engine
from cost import Cost
from race import Race

""" the class to build the player """
class Player:
    """ the line is a string that contains all the player data """
    def __init__(self, **kwargs):
        """
        sets = line.strip().split(", ")
        self.name = sets[0]
        self._energy = int(sets[1])
        self._effort = int(sets[2])
        self.factory_efficency = int(sets[3])
        self.mine_efficency = int(sets[4])
        self.effort_efficency = int(sets[5])
        self.tax_rate = int(sets[6])
        self.research_rate = int(sets[7])
        self.stimulus_package = int(sets[8])
        self.research_level = int(sets[9])
        s_set = sets[10].split(",")
        self.factory_cost = Cost(int(s_set[0]), int(s_set[1]), int(s_set[2]), int(s_set[3]), int(s_set[4]), int(s_set[5]))
        s_set = sets[11].split(",")
        self.mine_cost = Cost(int(s_set[0]), int(s_set[1]), int(s_set[2]), int(s_set[3]), int(s_set[4]), int(s_set[5]))
        s_set = sets[12].split(",")
        self._research_cost = Cost(int(s_set[0]), int(s_set[1]), int(s_set[2]), int(s_set[3]), int(s_set[4]), int(s_set[5]))
        s_set = sets[13].split(",")
        self._origanal_research_cost = Cost(int(s_set[0]), int(s_set[1]), int(s_set[2]), int(s_set[3]), int(s_set[4]), int(s_set[5]))
        self._research_queue = [[self._research_cost.energy, self._research_cost.effort], [self._origanal_research_cost.energy * (2+self.research_level/2), self._origanal_research_cost.effort * (2+self.research_level/2)]]
        """
        self.race = Race()
        self.name = kwargs.get('name', 'Player_' + str(id(self)))
        game_engine.register(self)
    
    """ takes the turn """
    def take_turn(self):
        self.doResearch()
        self.__effort = 0
    
    """ research """
    def do_research(self):
        """ if research queue is empty fill it up """
        if len(self._research_queue) < 1:
            self._research_queue.append([int(self._origanal_research_cost.energy * (1+self.research_level/2)), int(self._origanal_research_cost.effort * (1+self.research_level/2)), 0])
        if len(self._research_queue) < 2:
            self._research_queue.append([int(self._origanal_research_cost.energy * (2+self.research_level/2)), int(self._origanal_research_cost.effort * (2+self.research_level/2)), 0])
        for i in range(100):
            """ do reasearch """
            if self._energy >= self._research_cost.energy:
                self._energy -= self._research_cost.energy
                self._research_cost.energy = 0
            else:
                self._research_cost.energy -= self._energy
                self._energy = 0
            
            if self._effort >= self._research_cost.effort:
                self._effort -= self._research_cost.effort
                self._research_cost.effort = 0
            else:
                self._research_cost.effort -= self._effort
                self._effort = 0
            
            if self._research_cost.energy == 0 and self._research_cost.effort == 0:
                self._research_level += 1
                self._research_queue.pop(0)
                self._research_cost.energy = int(self._research_queue[0][0])
                self._research_cost.effort = int(self._research_queue[0][1])
                self._research_queue.append([int(self._origanal_research_cost.energy * (2+self.research_level/2)), int(self._origanal_research_cost.effort * (2+self.research_level/2)), 0])
            else:
                self._research_queue[0] = [int(self._research_cost.energy), int(self._research_cost.effort)]
                break

# Register the class with the game engine
game_engine.register(Player)


""" testing """
def _test():
    _testPlayer__init__()
    
def _testPlayer__init__():
    """
    test_player = Player("Uma, 100000, 0, 100, 100, 100, 7, 7, 100, 1, 50,50,0,0,0,0, 50,50,0,0,0,0, 500,500,0,0,0,0, 500,500,0,0,0,0")
    if test_player.name != "Uma":
        print("name Fail")
    if test_player._energy != 100000:
        print("money Fail")
    if test_player._effort != 0:
        print("effort Fail")
    if test_player.factory_efficency != 100:
        print("factory_efficency Fail")
    if test_player.mine_efficency != 100:
        print("mine_efficency Fail")
    if test_player.effort_efficency != 100:
        print("effort_efficency Fail")
    if test_player.tax_rate != 7:
        print("tax_rate Fail")
    if test_player.research_rate != 7:
        print("research_rate Fail")
    if test_player.stimulus_package != 100:
        print("stimuls_package Fail")
    if test_player.research_level != 1:
        print("research_level Fail")
    if test_player.factory_cost.energy != 50 and test_player.factory_cost.effort != 50:
        print("factory_cost Fail")
    if test_player.mine_cost.energy != 50 and test_player.mine_cost.effort != 50:
        print("mine_cost Fail")
    if test_player._research_cost.energy != 500 and test_player._research_cost.effort != 500:
        print("research_cost Fail")
    if test_player._origanal_research_cost.energy != 500 and test_player._origanal_research_cost.effort != 500:
        print("origanal_research_cost Fail")
    """
    print("tested Player __init__()")
