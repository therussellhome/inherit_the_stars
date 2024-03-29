""" Indexed by location """
__fleets = {}


""" Reset fleet here tracking """
def reset():
    global __fleets
    __fleets = {}

""" Get the multi-fleets for game to call actions on """
def get(location=None):
    global __fleets
    if not location:
        return __fleets.values()
    elif location.root_location in __fleets:
        return __fleets[location.root_location].fleets
    return []

""" Add fleet a fleet """
def add(fleet):
    global __fleets
    location = fleet.location.root_location
    if location not in __fleets:
        __fleets[location] = MultiFleet()
    __fleets[location].fleets.append(fleet)


""" Handle multi-fleet actions """
class MultiFleet:
    """ Initialize the multi fleet """
    def __init__(self):
        self.fleets = []

    """ TODO """
    def round1_fight(self):
        pass #TODO

    """ TODO """
    def share_fuel(self):
        # also orbital fuel generation
        # apply fuel caps after sharing
        pass #TODO

    """ TODO """
    def share_repair(self):
        share_groups = []
        for f in self.fleets:
            if f.is_stationary:
                pass #TODO
            # Moving ships can only repair themselves
            else:
                for s in f.ships:
                    s.armor_damage -= s.hull().repair
        for g in share_groups:
            pass #TODO
#            for i in range(repair_points):
#                ships.sort(key=lambda x: x.armor_damage / x.armor, reverse=True)
#                ships[0].armor_damage -= 1
