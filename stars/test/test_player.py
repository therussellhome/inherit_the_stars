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

    #'''
    def test_get_treaty01(self):
        p = player.Player()
        t = p.get_treaty(p)
        self.assertTrue(t.relation == 'me')
    
    #'''
    def test_get_treaty02(self):
        p = player.Player()
        t = p.get_treaty(p, True)
        self.assertTrue(t == None)
    
    #'''
    def test_get_treaty03(self):
        p = player.Player()
        p1 = player.Player()
        t = p.get_treaty(p1)
        self.assertTrue(t.other_player == reference.Reference(p1))
    
    #'''
    def test_get_treaty11(self):
        p1 = player.Player()
        p2 = player.Player()
        t1 = treaty.Treaty(other_player = reference.Reference(p2))
        t2 = treaty.Treaty(other_player = reference.Reference(p1), treaty_key = t1.treaty_key)
        p1.treaties.append(t1)
        p2.treaties.append(t2)
        t = p1.get_treaty(p2, True)
        self.assertTrue(t == t1)

    #'''
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

    #'''
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
        #'''



    def test_do_research(self):
        #TODO
        return
        p = player.Player()
        p.energy = 1000000
        p.energy_minister.allocate_budget(p.energy)
        p.energy_minister.research_budget = 100
        p.research_field = 'energy'
        p.tech_level.energy = 0
        p.next_tech_cost.energy = 100
        p._do_research()
        self.assertEqual(p.tech_level.energy, 1)
        self.assertEqual(p.energy_minister.research_budget, 0)
        p.energy_minister.research_budget = 300
        p.research_field = 'energy'
        p.tech_level.energy = 0
        p.next_tech_cost.energy = 100
        p._do_research()
        self.assertEqual(p.tech_level.energy, 2)
        self.assertEqual(p.energy_minister.research_budget, 0)

    def test_calc_research_cost(self):
        # TODO
        pass

    def test_calc_next_research_field(self):
        # TODO
        pass

    def test_allocate(self):
        return # TODO these tests predate the move to player
        m = energy_minister.EnergyMinister()
        # test 1
        m.energy_minister_construction_percent = 100
        m.energy_minister_mattrans_percent = 100
        m.energy_minister_research_percent = 100
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 100)
        self.assertEqual(m.mattrans_budget, 0)
        self.assertEqual(m.research_budget, 0)
        self.assertEqual(m.unallocated_budget, 0)
        # test 2
        m.energy_minister_construction_percent = 0
        m.energy_minister_mattrans_percent = 100
        m.energy_minister_research_percent = 100
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 0)
        self.assertEqual(m.mattrans_budget, 100)
        self.assertEqual(m.research_budget, 0)
        self.assertEqual(m.unallocated_budget, 0)
        # test 3
        m.energy_minister_construction_percent = 0
        m.energy_minister_mattrans_percent = 0
        m.energy_minister_research_percent = 100
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 0)
        self.assertEqual(m.mattrans_budget, 0)
        self.assertEqual(m.research_budget, 100)
        self.assertEqual(m.unallocated_budget, 0)
        # test 4
        m.energy_minister_construction_percent = 0
        m.energy_minister_mattrans_percent = 0
        m.energy_minister_research_percent = 0
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 0)
        self.assertEqual(m.mattrans_budget, 0)
        self.assertEqual(m.research_budget, 0)
        self.assertEqual(m.unallocated_budget, 100)
        # test 5
        m.energy_minister_construction_percent = 10
        m.energy_minister_mattrans_percent = 10
        m.energy_minister_research_percent = 10
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 10)
        self.assertEqual(m.mattrans_budget, 10)
        self.assertEqual(m.research_budget, 10)
        self.assertEqual(m.unallocated_budget, 70)

    def test_check_budget(self):
        return # TODO these tests predate the move to player
        m = energy_minister.EnergyMinister()
        m.energy_minister_construction_percent = 40
        m.energy_minister_mattrans_percent = 30
        m.energy_minister_research_percent = 20
        m.allocate_budget(100)
        self.assertEqual(m.check_budget('ship', 30), 30)
        self.assertEqual(m.check_budget('ship', 40), 40)
        self.assertEqual(m.check_budget('ship', 111), 40)
        self.assertEqual(m.check_budget('planetary', 111), 40)
        self.assertEqual(m.check_budget('baryogenesis', 111), 40)
        self.assertEqual(m.check_budget('mattrans', 111), 30)
        self.assertEqual(m.check_budget('research', 111), 20)
        self.assertEqual(m.check_budget('trade', 111), 100)
        m.energy_minister_mattrans_use_surplus = True
        self.assertEqual(m.check_budget('mattrans', 111), 70)
        m.energy_minister_research_use_surplus = True
        self.assertEqual(m.check_budget('research', 111), 90)
        self.assertEqual(m.construction_budget, 40)
        self.assertEqual(m.mattrans_budget, 30)
        self.assertEqual(m.research_budget, 20)
        self.assertEqual(m.unallocated_budget, 10)

    def test_spend_budget(self):
        return # TODO these tests predate the move to player
        m = energy_minister.EnergyMinister()
        m.energy_minister_construction_percent = 40
        m.energy_minister_mattrans_percent = 30
        m.energy_minister_research_percent = 20
        m.allocate_budget(100)
        # Construction
        self.assertEqual(m.spend_budget('ship', 1), 1)
        self.assertEqual(m.construction_budget, 39)
        self.assertEqual(m.spend_budget('planetary', 1), 1)
        self.assertEqual(m.construction_budget, 38)
        self.assertEqual(m.spend_budget('baryogenesis', 1), 1)
        self.assertEqual(m.construction_budget, 37)
        # Mattrans
        self.assertEqual(m.spend_budget('mattrans', 111), 30)
        self.assertEqual(m.mattrans_budget, 0)
        m.energy_minister_mattrans_use_surplus = True
        self.assertEqual(m.spend_budget('mattrans', 5), 5)
        self.assertEqual(m.mattrans_budget, -5)
        # Research
        self.assertEqual(m.spend_budget('research', 111), 20)
        self.assertEqual(m.research_budget, 0)
        m.energy_minister_research_use_surplus = True
        self.assertEqual(m.spend_budget('research', 111), 32)
        self.assertEqual(m.research_budget, -32)
        # Unallocated
        self.assertEqual(m.spend_budget('trade', 111), 10)
        self.assertEqual(m.unallocated_budget, 0)
