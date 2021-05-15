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
    elif location in __fleets:
        return __fleets[location].fleets
    return []

""" Add fleet a fleet """
def add(fleet):
    global __fleets
    location = fleet.location.reference_root
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
