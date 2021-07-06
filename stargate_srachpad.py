
def move(self, moveto, speed, stats):
    start, end = self._stargate_find(moveto, False)
    if speed == -2 or (speed == -1 and self._stargate_find(moveto, True)):
        self.__cache__['moved'] = False
        # stargate use allows fleet actions this hundredth
        self.__cache__['move_in_system'] = moveto
        if start and end:
            self.location = Location(reference = moveto)
        multi_fleet.add(self)
    else:
        pass #move at speed

def _stargate_find(self, moveto, be_picky):
    # stargate format: [ship, cost(-1 means not alowed)]
    start_gates = []
    end_gates = []
    end_gate = None
    for fleet in multi_fleet.get(self.location):
        for ship in fleet.ships:
            if ship.stargate.strength > 0:
                start_gates.append(ship)
                #if self.player.get_treaty(ship.player).buy_gates:
                #    cost = self.player.get_treaty(ship.player).cost_buy_gates
                #else:
                #    cost = -1
                #start_gates.append([ship, cost])
    for fleet in multi_fleet.get(moveto):
        for ship in fleet.ships:
            if ship.stargate.strength > 0:
                #if self.player.get_treaty(ship.player).buy_gates:
                #    cost = self.player.get_treaty(ship.player).cost_buy_gates
                #else:
                #    cost = -1
                end_gate = ship
                break
    start_gates.stort(key=lambda x: x.stargate.strength, reverse=True)
    if len(start_gates) > 0:
        return (start_gates[0], end_gate)
    else:
        return (None, end_gate)
    if be_picky:
        pass #be picky

def gate_damage(self, ?):
    



