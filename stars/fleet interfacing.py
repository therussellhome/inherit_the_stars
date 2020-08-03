""" outline """
Game for action in actions: for Player in players: Player.ship_action(action)
Player.ship_action(action): for Fleet in fleets: Fleet.exceute(action,player)
Fleet.excute(action,player): Fleet do action(?player?): for Ship in ships: Ship.action(?player?)
Ship.action(?player?): Ship do stuff

""" involving transfer of Cargo """
Fleet.compile()
Fleet.returnn()
#Fleet hadles cargo not ship
""" load """
Player.ship_action('load'): for Fleet in fleets: Fleet.exceute('load', player)
Fleet.excute('load', player): Fleet.load(player): Fleet do stuff
""" unload """
Player.ship_action('unload'): for Fleet in fleets: Fleet.exceute('unload', Llayer)
Fleet.excute('unload', player): Fleet.unload(player): Fleet do stuff
""" buy """
Player.ship_action('buy'): for Fleet in fleets: Fleet.exceute('buy', player)
Fleet.excute('buy', player): Fleet.buy(player): Fleet do stuff
""" sell """
Player.ship_action('sell'): for Fleet in fleets: Fleet.exceute('sell', player)
Fleet.excute('sell', player): Fleet.sell(player): Fleet do stuff
""" colonize """
Player.ship_action('colonize'): for Fleet in fleets: Fleet.exceute('colonize', player)
Fleet.excute('colonize', player): Fleet.colonize(player): for Ship in ships: Ship.colonize(player, planet)
Ship.colonize(player, planet): Planet.colonize(player, 'default minister', cargo, num_col_modules, num_col_modules, num_col_modules)

""" involving transfer and editing fleets """
""" scrap """
Player.ship_action('scrap'): for Fleet in fleets: Fleet.exceute('scrap', player)
Fleet.excute('scrap', player): Fleet.scrap(): for Ship in ships: Ship.scrap(fleet.location)
Ship.scrap(location): Cargo=Cargo(t, l, i, cm=-1); if location != referance(Planet): create_salvage(location, Cargo); else: planet.cargo += cargo + Cargo
""" merge """
Player.ship_action('merge'): for Fleet in fleets: Fleet.exceute('merge', player)
Fleet.excute('merge', player): Fleet.merge(): for Ship in ships: o_fleet.ships.append(ship) o_fleet.compile() o_fleet.returnn()
