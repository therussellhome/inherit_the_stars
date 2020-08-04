""" outline """
Game for action in actions: for Player in players: Player.ship_action(action)
Player.ship_action(action): for Fleet in fleets: Fleet.exceute(action, player)
Fleet.excute(action, player): Fleet do_action(?player?): for Ship in ships: Ship.action(?player?)
Ship.action(?player?): Ship do stuff
""" involving transfer of Cargo """
Fleet.compile()
Fleet.returnn()
#Fleet hadles cargo not ship
""" load """ #written
    Fleet.excute('load', player): Fleet.load(player): Fleet do stuff
""" unload """ #written
    Fleet.excute('unload', player): Fleet.unload(player): Fleet do stuff
""" buy """ #working #written
    Fleet.excute('buy', player): Fleet.buy(player): Fleet do stuff
""" sell """ #working #written
    Fleet.excute('sell', player): Fleet.sell(player): Fleet do stuff
""" piracy """
    Fleet.excute('piracy', player): Fleet.piracy(player): Fleet do stuff
""" colonize """ #written
    Fleet.excute('colonize', player): Fleet.colonize(player): for Ship in ships: Ship.colonize(player, planet)
    Ship.colonize(player, planet):
        Planet.colonize(player, copy.copy(player.colonize_minister), cargo, num_col_modules, num_col_modules, num_col_modules)
""" involving transfer and editing fleets """ #DONE
""" scrap """ #written
    Fleet.excute('scrap', player): Fleet.scrap(): for Ship in ships: Ship.scrap(fleet.location)
    Ship.scrap(location): Cargo=Cargo(t, l, s, cm = (t + l + s)); if location != referance(Planet): create_salvage(location, Cargo);
        else: planet.on_surface += cargo + Cargo
""" merge """ #written
    Fleet.excute('merge', player): Fleet.merge(player)
    Fleet.merge(player): o_fleet = waypoint.recipiants['merge'] if type(o_fleet) != type(Fleet) or o_fleet not in player.fleets: return;
        for Ship in ships: o_fleet.ships.append(ship); o_fleet.compile() o_fleet.returnn()
""" split """ #written
    Fleet.excute('split', player): Fleet.split(player)
    Fleet.split(player): for split in waypoint.splits: Player.create_fleet(ships=split.ships, waypoints=copy.copy(fleet.waypoints))
        for ship in split.ships: fleet.ships.remove(ship);; if len(fleet.ships) == 0: Player.remove_fleet(self)
""" transfer """ #written
    Fleet.excute('transfer', player): Fleet.transfer(player)
    Fleet.transfer(player): Player2 = waypoint.recipiants['transfer'] Player2.create_fleet(self.__dict__) Player.remove_fleet(self)
""" other? """ #-patrol
""" orbital_mining """ #written
    Fleet.excute('orbital_mining', player): Fleet.orbital_mining(): check planet for Ship in ships: Ship.orbital_mining(planet)
""" deploy_hyper_denial (how to store hyper_denials?) """ #written
    Fleet.excute('deploy_hyper_denial', player): Fleet.deploy_hyper_denial(player): for Ship in ships: Ship.deploy_hyper_denial(player)
""" self_repair """ #written
    Fleet.excute('self_repair', player): Fleet.self_repair(): for Ship in ships: Ship.self_repair()
""" repair """ #written
    Fleet.excute('repair', player): Fleet.repair(player)
    Fleet.repair(player): repair_points = 0 for Ship in ships: repair_points += Ship.open_repair_bays(); for ship in game_engine.get('Ship/'):
        if (fleet.location - ship.location) <= (2*TM): ships_here.append(ship);; Fleet.distribute_repair(ships_here)
    Fleet.distribute_repair(ships_here, repair_points): while repair_points > 0 and Fleet.find_repair(ships_here) != False:
        ship = Fleet.find_repair(ships_here) Ship.repair(1) repair_points -= 1
    Fleet.find_repair(ships_here): damage_ratio = [] for ship in ships_here: damage_ratio.append([100 * (ship.armor / ship.max_armor), ship]);
        damage = 100 worst = 0 for i in range(len(damage_ratio)): if damage_ratio[i][0] <= damage: damage = damage_ratio[i][0] worst = i;;
        if damage_ratio[worst][0] == 100: return False; return dmage_ratio[worst][1]
""" lay_mines """ #written
    Fleet.excute('lay_mines', player): Fleet.lay_mines(player): find_system for ship in ships: Ship.lay_mines(player, system)
""" bomb """ #written
    Fleet.excute('bomb', player): Fleet.bomb(player): find_planet for ship in ships: Ship.bomb(player?, planet)
""" patrol """
    Fleet.excute('patrol', player): Fleet.patrol(player): 
""" scan """ #written
    Fleet.excute('scan', player): Fleet.scan(player): for ship in ships: Ship.scan(player)
