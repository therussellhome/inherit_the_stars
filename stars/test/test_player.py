import unittest
from unittest.mock import patch
from .. import *

class PlayerTestCase(unittest.TestCase):
    def test_init1(self):
        r = race.Race()
        p = player.Player(race=r)
        self.assertEqual(p.ID, r.ID)

    def test_init2(self):
        home = reference.Reference(planet.Planet())
        p = player.Player(planets=[home])
        self.assertEqual(home.player, p)

    def test_filename1(self):
        p = player.Player()
        self.assertEqual(p.filename(), ' - ' + p.ID)

    def test_save1(self):
        p = player.Player()
        home = reference.Reference(planet.Planet())
        home.colonize(p)
        home.on_surface.people = 100
        with patch.object(game_engine, 'save') as mock:
            p.save()
        self.assertEqual(home, p.planets[0])

    def test_load1(self):
        p0 = player.Player(ID='original')
        p1 = player.Player(ID='from file', ready_to_generate=True)
        with patch.object(game_engine, 'load_inspect', return_value=p1):
            p0.update_from_file()
        self.assertEqual(p0.ID, 'original')
        self.assertFalse(p0.ready_to_generate)

    def test_load2(self):
        p0 = player.Player(ID='original')
        p1 = player.Player(ID='from file', ready_to_generate=True, validation_key=p0.validation_key)
        with patch.object(game_engine, 'load_inspect', return_value=p1):
            p0.update_from_file()
        self.assertEqual(p0.ID, 'original')
        self.assertTrue(p0.ready_to_generate)

    def test_minister1(self):
        p = player.Player()
        home = reference.Reference(planet.Planet())
        self.assertEqual(p.get_minister(home), p.ministers[-1])

    def test_minister2(self):
        home = reference.Reference(planet.Planet())
        p = player.Player(planets=[home])
        self.assertNotEqual(p.get_minister(home), p.ministers[-1])

    def test_minister3(self):
        home = reference.Reference(planet.Planet())
        p = player.Player()
        p.ministers[-1].new_colony_minister = False
        cnt = len(p.ministers)
        p.get_minister(home)
        self.assertEqual(len(p.ministers), cnt + 1)

    def test_reconcile1(self):
        f = fleet.Fleet()
        p = player.Player(fleets=[f])
        p.reconcile_fleets()
        self.assertEqual(f.player, p)

    def test_buships1(self):
        bs = buships.BuShips()
        p = player.Player(buships=[bs])
        p.reconcile_buships()
        self.assertEqual(len(p.build_queue), 1)

    def test_buships2(self):
        build = build_ship.BuildShip()
        p = player.Player(build_queue=[build])
        p.reconcile_buships()
        self.assertEqual(len(p.build_queue), 0)

    def test_buships3(self):
        bs = buships.BuShips()
        print(bs.ID)
        build = build_ship.BuildShip(buships=reference.Reference(bs))
        p = player.Player(buships=[bs], build_queue=[build])
        p.reconcile_buships()
        self.assertEqual(len(p.build_queue), 1)

    def test_hundreth1(self):
        p = player.Player()
        date = p.date
        p.next_hundreth()
        self.assertNotEqual(date, p.date)

    def test_stats1(self):
        home = reference.Reference(planet.Planet())
        w = weapon.Weapon()
        f = fleet.Fleet() + ship.Ship() + ship.Ship(weapons=[w]) + ship.Ship(weapons=[w, w, w, w, w, w, w, w, w, w, w]) + ship.Ship()
        p = player.Player(planets=[home], fleets=[f])
        with patch.object(ship.Ship, 'is_space_station', side_effect=[True, False, False, False]):
            with patch.object(player.Player, 'add_intel') as mock:
                p.update_stats()
                self.assertEqual(mock.call_args.args[1]['starbases'], 1)

    def test_add1(self):
        p = player.Player()
        p.add_ships(ship.Ship())
        self.assertEqual(len(p.fleets), 1)
        self.assertEqual(len(p.fleets[0].ships), 1)

    def test_add2(self):
        p = player.Player()
        p.add_ships([ship.Ship(), reference.Reference(ship.Ship())])
        self.assertEqual(len(p.fleets), 1)
        self.assertEqual(len(p.fleets[0].ships), 2)

    def test_remove1(self):
        s = ship.Ship()
        p = player.Player()
        p.add_ships([s, ship.Ship()])
        p.remove_ships(s)
        self.assertEqual(len(p.fleets), 1)
        self.assertEqual(len(p.fleets[0].ships), 1)

    def test_remove2(self):
        s1 = ship.Ship()
        s2 = ship.Ship()
        p = player.Player()
        p.add_ships([s1, s2])
        p.remove_ships(p.fleets[0])
        self.assertEqual(len(p.fleets), 0)

    def test_remove3(self):
        s1 = ship.Ship()
        s2 = ship.Ship()
        p = player.Player()
        p.add_ships([s1, s2])
        p.remove_ships(reference.Reference(p.fleets[0]))
        self.assertEqual(len(p.fleets), 0)

    def test_token1(self):
        p = player.Player()
        self.assertEqual(str(id(p)), p.token())

    def test_addintel1(self):
        p = player.Player()
        s = reference.Reference(ship.Ship())
        p.add_intel(s, {'test': True})
        self.assertTrue(p.intel[s].test)

    def test_getintel1(self):
        p = player.Player()
        s = reference.Reference(ship.Ship())
        self.assertEqual(p.get_intel(reference=s), None)

    def test_getintel2(self):
        p = player.Player()
        s = reference.Reference(ship.Ship())
        p.add_intel(s, {'test': True})
        self.assertTrue(p.get_intel(reference=s).test)

    def test_getintel3(self):
        p = player.Player()
        s = reference.Reference(ship.Ship())
        p.add_intel(s, {'test': True})
        self.assertTrue(p.get_intel(by_type='Ship')[s].test)

    def test_name1(self):
        p = player.Player()
        s = reference.Reference(ship.Ship())
        self.assertEqual(p.get_name(s), s.ID)

    def test_name2(self):
        p = player.Player()
        s = reference.Reference(ship.Ship())
        p.add_intel(s, {'test': 'test'})
        self.assertEqual(p.get_name(s), s.ID)

    def test_name3(self):
        p = player.Player()
        s = reference.Reference(ship.Ship())
        p.add_intel(s, {'name': 'test'})
        self.assertEqual(p.get_name(s), 'test')

    def test_add_message1(self):
        p = player.Player()
        p.add_message(message = 'this is a test')
        self.assertEqual(p.messages[-1].message, 'this is a test')

    def test_cleanup_messages1(self):
        p = player.Player()
        cnt = len(p.messages)
        p.add_message(message = 'testing 1', star = False, read = False)
        p.add_message(message = 'testing 2', star = False, read = True)
        p.add_message(message = 'testing 3', star = True, read = False)
        p.add_message(message = 'testing 4', star = True, read = True)
        p.cleanup_messages()
        self.assertEqual(len(p.messages), cnt + 3)

    def test_treaty01(self):
        p1 = player.Player()
        p2 = player.Player()
        msg_cnt = len(p2.messages)
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        p1.treaty_negotiations()
        p2.treaty_negotiations()
        self.assertEqual(len(p2.messages), msg_cnt + 1)

    def test_treaty02(self):
        p1 = player.Player()
        p2 = player.Player()
        msg_cnt = len(p2.messages)
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        t1.status = 'signed'
        t2.status = 'signed'
        p1.treaty_finalization()
        p2.treaty_finalization()
        self.assertEqual(len(p2.messages), msg_cnt + 1)

    def test_treaty03(self):
        p1 = player.Player()
        p2 = player.Player()
        treaty_cnt = len(p2.treaties)
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        t1.status = 'rejected'
        t2.status = 'rejected'
        p1.treaty_finalization()
        p2.treaty_finalization()
        self.assertEqual(len(p2.treaties), treaty_cnt)

    def test_treaty04(self):
        p1 = player.Player()
        p2 = player.Player()
        treaty_cnt = len(p2.treaties)
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        t1.status = 'signed'
        t2.status = 'signed'
        p1.treaty_finalization()
        p2.treaty_finalization()
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        t1.status = 'signed'
        t2.status = 'signed'
        p1.treaty_finalization()
        p2.treaty_finalization()
        self.assertEqual(len(p2.treaties), treaty_cnt + 1)

    def test_get_treaty01(self):
        p = player.Player()
        t = p.get_treaty(p)
        self.assertTrue(t.relation == 'me')
    
    def test_get_treaty02(self):
        p = player.Player()
        t = p.get_treaty(p, True)
        self.assertTrue(t == None)
    
    def test_get_treaty03(self):
        p = player.Player()
        p1 = player.Player()
        t = p.get_treaty(p1)
        self.assertTrue(t.other_player == reference.Reference(p1))
    
    def test_get_treaty11(self):
        p1 = player.Player()
        p2 = player.Player()
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        t = p1.get_treaty(p2, True)
        self.assertTrue(t == t1)

    def test_get_treaty12(self):
        p1 = player.Player()
        p2 = player.Player()
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        t1.status = 'active'
        t2.status = 'active'
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        t = p1.get_treaty(p2, True)
        self.assertTrue(t == None)

    def test_get_treaty13(self):
        p1 = player.Player()
        p2 = player.Player()
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        t1.status = 'active'
        t2.status = 'active'
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        t = p1.get_treaty(p2)
        self.assertTrue(t == t1)

    def test_get_relation01(self):
        p = player.Player()
        self.assertEqual(p.get_relation(p), 'me')

    def test_get_relation02(self):
        p = player.Player()
        o = player.Player()
        self.assertEqual(p.get_relation(o), 'neutral')

    def test_max_terraform01(self):
        p = player.Player()
        p.tech_level.biotechnology = 0
        self.assertEqual(p.max_terraform(), 0.0)

    def test_max_terraform02(self):
        r = race.Race(lrt_Bioengineer=True)
        p = player.Player(race=r)
        p.tech_level.biotechnology = 0
        self.assertEqual(p.max_terraform(), 0)

    def test_max_terraform03(self):
        p = player.Player()
        p.tech_level.biotechnology = 1
        self.assertEqual(p.max_terraform(), 0.5)

    def test_max_terraform04(self):
        r = race.Race(lrt_Bioengineer=True)
        p = player.Player(race=r)
        p.tech_level.biotechnology = 1
        self.assertEqual(p.max_terraform(), 1)

    def test_max_terraform05(self):
        p = player.Player()
        p.tech_level.biotechnology = 50
        self.assertEqual(p.max_terraform(), 20)

    def test_max_terraform06(self):
        r = race.Race(lrt_Bioengineer=True)
        p = player.Player(race=r)
        p.tech_level.biotechnology = 50
        self.assertEqual(p.max_terraform(), 40)

    def test_predict_budget(self):
        pass #TODO

    def test_allocate_budget01(self):
        p = player.Player()
        p.energy = 0
        p.allocate_budget()
        for category in ['construction', 'mattrans', 'research']:
            self.assertEqual(p['budget_' + category], 0)


    def test_allocate_budget02(self):
        p = player.Player()
        p.energy = 100
        p.allocate_budget()
        self.assertEqual(p['budget_construction'], 90)
        self.assertEqual(p['budget_mattrans'], 0)
        self.assertEqual(p['budget_research'], 10)

    def test_allocate_budget03(self):
        p = player.Player()
        p.allocate_budget()
        self.assertEqual(p['budget_construction'], p.energy*0.9)
        self.assertEqual(p['budget_mattrans'], 0)
        self.assertEqual(p['budget_research'], p.energy*0.1)

    def test_add_energy01(self):
        p = player.Player()
        p.energy = 90
        len_intel = len(p.intel)
        p.add_energy(10)
        self.assertEqual(p.energy, 100)
        self.assertEqual(len(p.intel), len_intel +1)

    def test_spend01(self):
        p = player.Player()
        p.energy = 100
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('Ship', spend=False), 90)
        self.assertEqual(p.energy, 100)
        self.assertEqual(p.budget_construction, 90)        
        self.assertEqual(len(p.intel), len_intel)

    def test_spend02(self):
        p = player.Player()
        p.energy = 100
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('StarBase'), 90)
        self.assertEqual(p.energy, 10)
        self.assertEqual(p.budget_construction, 0)        
        self.assertEqual(len(p.intel), len_intel +1)

    def test_spend03(self):
        p = player.Player()
        p.energy = 100
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('Facility', 4), 4)
        self.assertEqual(p.energy, 96)
        self.assertEqual(p.budget_construction, 86)        
        self.assertEqual(len(p.intel), len_intel +1)

    def test_spend04(self):
        p = player.Player()
        p.energy = 100
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('Baryogenesis', request=8), 8)
        self.assertEqual(p.energy, 92)
        self.assertEqual(p.budget_construction, 82)        
        self.assertEqual(len(p.intel), len_intel +1)

    def test_spend11(self):
        p = player.Player()
        p.energy = 100
        p.finance_mattrans_use_surplus = False
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('mattrans'), 0)
        self.assertEqual(p.energy, 100)
        self.assertEqual(p.budget_construction, 90)        
        self.assertEqual(p.budget_mattrans, 0)        
        self.assertEqual(len(p.intel), len_intel +1)

    def test_spend12(self):
        p = player.Player()
        p.energy = 100
        p.finance_mattrans_use_surplus = True
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('mattrans'), 90)
        self.assertEqual(p.energy, 10)
        self.assertEqual(p.budget_construction, 90)        
        self.assertEqual(p.budget_mattrans, -90)        
        self.assertEqual(len(p.intel), len_intel +1)

    def test_spend21(self):
        p = player.Player()
        p.energy = 100
        p.finance_research_use_surplus = False
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('research'), 10)
        self.assertEqual(p.energy, 90)
        self.assertEqual(p.budget_construction, 90)        
        self.assertEqual(p.budget_research, 0)        
        self.assertEqual(len(p.intel), len_intel +1)

    def test_spend22(self):
        p = player.Player()
        p.energy = 100
        p.finance_research_use_surplus = True
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('research'), 100)
        self.assertEqual(p.energy, 0)
        self.assertEqual(p.budget_construction, 90)        
        self.assertEqual(p.budget_research, -90)        
        self.assertEqual(len(p.intel), len_intel +1)

    def test_spend31(self):
        p = player.Player()
        p.energy = 100
        p.allocate_budget()
        len_intel = len(p.intel)
        self.assertEqual(p.spend('planitoid'), 100)
        self.assertEqual(p.energy, 0)
        self.assertEqual(len(p.intel), len_intel +1)

    def test_build_from_queue01(self):
        p1 = player.Player()
        p2 = player.Player()
        home_planet = planet.Planet(player=reference.Reference(p2))
        to_build = build_ship.BuildShip(planet=reference.Reference(home_planet))
        p1.build_queue.append(to_build)
        p1.build_from_queue()
        self.assertEqual(len(p1.build_queue), 0)
        self.assertEqual(len(p1.fleets), 0)
        self.assertEqual(len(p2.build_queue), 0)
        self.assertEqual(len(p2.fleets), 0)

    def test_build_from_queue02(self):
        p1 = player.Player()
        home_planet = planet.Planet(player=reference.Reference(p1))
        to_build = build_ship.BuildShip(planet=reference.Reference(home_planet))
        p1.build_queue.append(to_build)
        with patch.object(planet.Planet, 'build', return_value=True) as mock:
            p1.build_from_queue()
        self.assertEqual(len(p1.build_queue), 0)
        self.assertEqual(mock.call_count, 1)

    def test_build_from_queue03(self):
        p1 = player.Player()
        home_planet = planet.Planet(player=reference.Reference(p1))
        to_build_1 = build_ship.BuildShip(planet=reference.Reference(home_planet))
        p1.build_queue.append(to_build_1)
        to_build_2 = build_ship.BuildShip(planet=reference.Reference(home_planet))
        p1.build_queue.append(to_build_2)
        self.assertEqual(len(p1.build_queue), 2)
        with patch.object(planet.Planet, 'build', side_effect=[True, False]) as mock:
            p1.build_from_queue()
        self.assertEqual(len(p1.build_queue), 1)
        self.assertEqual(mock.call_count, 2)

    def test_research01(self):
        p = player.Player()
        p.energy = 55000
        p.allocate_budget()
        p.research_field = 'energy'
        p.tech_level = tech_level.TechLevel()
        p.research()
        self.assertEqual(p.tech_level.energy, 1)
        self.assertEqual(p.budget_research, 0)
        self.assertEqual(p.energy, 49500)

    def test_research02(self):
        p = player.Player()
        p.finance_research_use_surplus = True 
        p.energy = 55000
        p.allocate_budget()
        p.research_field = 'energy'
        p.tech_level = tech_level.TechLevel()
        p.research()
        for f in player.TECH_FIELDS:
            if f == 'energy':
                self.assertEqual(p.research_partial[f], 22000)
                self.assertEqual(p.tech_level.energy, 3)
                continue
            self.assertEqual(p.research_partial[f], 0)
            self.assertEqual(p.tech_level[f], 0)
        self.assertEqual(p.budget_research, -49500)
        self.assertEqual(p.energy, 0)

    def test_research03(self):
        p = player.Player()
        p.race.lrt_MadScientist = True 
        p.energy = 55000
        p.allocate_budget()
        p.research_field = 'energy'
        p.tech_level = tech_level.TechLevel()
        p.research()
        print(p.tech_level.__dict__)
        print('Player.research_partial:', p.research_partial.__dict__)
        for f in player.TECH_FIELDS:
            self.assertEqual(p.tech_level[f], 0)
            if f == 'energy':
                self.assertEqual(p.research_partial[f], 3025)
                continue
            self.assertEqual(p.research_partial[f], 825)
        self.assertEqual(p.budget_research, 0)
        self.assertEqual(p.energy, 49500)

    def test_research04(self):
        p = player.Player()
        p.finance_research_use_surplus = True 
        p.race.lrt_MadScientist = True 
        p.energy = 55000
        p.allocate_budget()
        p.research_field = 'energy'
        p.tech_level = tech_level.TechLevel()
        p.research()
        for f in player.TECH_FIELDS:
            if f == 'energy':
                self.assertEqual(p.tech_level[f], 2)
                continue
            self.assertEqual(p.tech_level[f], 1)
        self.assertEqual(p.budget_research, -49500)
        self.assertEqual(p.energy, 0)

    def test_research11(self):
        p = player.Player()
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        for f in player.TECH_FIELDS:
            if f == 'energy':
                self.assertEqual(p.tech_level[f], 1)
                continue
            self.assertEqual(p.tech_level[f], 0)
        self.assertEqual(p.budget_research, 0)
        self.assertEqual(p.energy, 49500)

    def test_research12(self):
        p = player.Player()
        p.finance_research_use_surplus = True 
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        for f in player.TECH_FIELDS:
            if f == 'energy' or f == 'weapons':
                self.assertEqual(p.tech_level[f], 2)
                continue
            self.assertEqual(p.tech_level[f], 1)
        self.assertEqual(p.budget_research, -49500)
        self.assertEqual(p.energy, 0)

    def test_research13(self):
        p = player.Player()
        p.race.lrt_MadScientist = True 
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        for f in player.TECH_FIELDS:
            self.assertEqual(p.tech_level[f], 0)
            if f == 'energy':
                self.assertEqual(p.research_partial[f], 3025)
                continue
            self.assertEqual(p.research_partial[f], 825)
        self.assertEqual(p.budget_research, 0)
        self.assertEqual(p.energy, 49500)

    def test_research14(self):
        p = player.Player()
        p.finance_research_use_surplus = True 
        p.race.lrt_MadScientist = True 
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        print(p.tech_level.__dict__)
        print('Player.research_partial:', p.research_partial.__dict__)
        for f in player.TECH_FIELDS:
            if f == 'energy' or f == 'weapons':
                self.assertEqual(p.tech_level[f], 2)
                continue
            self.assertEqual(p.tech_level[f], 1)
        self.assertEqual(p.budget_research, -49500)
        self.assertEqual(p.energy, 0)

    def test_research21(self):
        p = player.Player()
        t_l = tech_level.TechLevel(weapons=1)
        t = tech.Tech(level=t_l)
        p.research_queue.append(t)
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        for f in player.TECH_FIELDS:
            if f == 'weapons':
                self.assertEqual(p.tech_level[f], 1)
                continue
            self.assertEqual(p.tech_level[f], 0)
        self.assertEqual(p.budget_research, 0)
        self.assertEqual(p.energy, 49500)

    def test_research22(self):
        p = player.Player()
        p.finance_research_use_surplus = True 
        t_l = tech_level.TechLevel(weapons=1)
        t = tech.Tech(level=t_l)
        p.research_queue.append(t)
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        print(p.tech_level.__dict__)
        print('Player.research_partial:', p.research_partial.__dict__)
        for f in player.TECH_FIELDS:
            if f == 'energy' or f == 'weapons':
                self.assertEqual(p.tech_level[f], 2)
                continue
            self.assertEqual(p.tech_level[f], 1)
        self.assertEqual(p.budget_research, -49500)
        self.assertEqual(p.energy, 0)

    def test_research23(self):
        p = player.Player()
        p.finance_research_use_surplus = True 
        t_l = tech_level.TechLevel(weapons=3)
        t = tech.Tech(level=t_l)
        p.research_queue.append(t)
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        print(p.tech_level.__dict__)
        print('Player.research_partial:', p.research_partial.__dict__)
        for f in player.TECH_FIELDS:
            if f == 'weapons':
                self.assertEqual(p.tech_level[f], 3)
                continue
            if f == 'biotechnology':
                self.assertEqual(p.tech_level[f], 0)
                continue
            self.assertEqual(p.tech_level[f], 1)
        self.assertEqual(p.budget_research, -49500)
        self.assertEqual(p.energy, 0)

    def test_research24(self):
        p = player.Player()
        p.race.lrt_MadScientist = True 
        t_l = tech_level.TechLevel(weapons=1)
        t = tech.Tech(level=t_l)
        p.research_queue.append(t)
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        print(p.tech_level.__dict__)
        print('Player.research_partial:', p.research_partial.__dict__)
        for f in player.TECH_FIELDS:
            self.assertEqual(p.tech_level[f], 0)
            if f == 'weapons':
                self.assertEqual(p.research_partial[f], 3025)
                continue
            self.assertEqual(p.research_partial[f], 825)
        self.assertEqual(p.budget_research, 0)
        self.assertEqual(p.energy, 49500)

    def test_research25(self):
        p = player.Player()
        p.finance_research_use_surplus = True 
        p.race.lrt_MadScientist = True 
        t_l = tech_level.TechLevel(weapons=3)
        t = tech.Tech(level=t_l)
        p.research_queue.append(t)
        p.energy = 55000
        p.allocate_budget()
        p.research_field = '<LOWEST>'
        p.tech_level = tech_level.TechLevel()
        p.research()
        print(p.tech_level.__dict__)
        print('Player.research_partial:', p.research_partial.__dict__)
        for f in player.TECH_FIELDS:
            if f == 'weapons':
                self.assertEqual(p.tech_level[f], 2)
                self.assertEqual(p.research_partial[f], 15735)
                continue
            self.assertEqual(p.tech_level[f], 1)
            self.assertEqual(p.research_partial[f], 2755)
        self.assertEqual(p.budget_research, -49500)
        self.assertEqual(p.energy, 0)

    def test_design_miniaturization(self):
        return #TODO
        p = player.Player()
        d = ship_design.ShipDesign()
        p.ship_designs.append(d)
        self.assertEqual(3, 2)
