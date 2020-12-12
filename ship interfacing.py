""" outline """
Game for action in actions: for Player in players: Player.ship_action(action)
Player.ship_action(action): for Fleet in fleets: Fleet.exceute(action, player)
Fleet.excute(action, player): Fleet do_action(?player?): for Ship in ships: Ship.action(?player?)
Ship.action(?player?): Ship do stuff
""" involving transfer of Cargo """
Fleet.compile()
Fleet.returnn()
#Fleet hadles cargo not ship
""" piracy """
    Fleet.excute('piracy', player): Fleet.piracy(player): Fleet do stuff
""" colonize """ #written
    Ship.colonize(player, planet):
        Planet.colonize(player, copy.copy(player.colonize_minister), cargo, num_col_modules, num_col_modules, num_col_modules)
""" involving transfer and editing fleets """ #DONE
""" scrap """ #written
    Ship.scrap(location): Cargo=Cargo(t, l, s, cm = (t + l + s)); if location != referance(Planet): create_salvage(location, Cargo);
        else: planet.on_surface += cargo + Cargo
""" other? """ #-patrol
""" orbital_mining """ #written
    Ship.orbital_mining(planet)
""" deploy_hyper_denial (how to store hyper_denials?) """
    Ship.deploy_hyper_denial(player)
""" self_repair """ #written
    Ship.self_repair()
""" repair """ #written
    Ship.open_repair_bays()
    Ship.repair(1)
""" lay_mines """ #written
    Ship.lay_mines(player, system)
""" bomb """ #written
    Ship.bomb(player?, planet)
""" patrol """
    Fleet.excute('patrol', player): Fleet.patrol(player): 
""" scan """ #written
    Ship.scan(player):
