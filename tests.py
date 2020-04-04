import unittest as ut
from map_objects import tile, game_map
from loader_functions import initialize_new_game


'''
Propositions de tests unitaires sur les methodes bloquantes
Requis : 4 methodes avec 2 tests par methode
'''


class TestTile(ut.TestCase):
    def testTile(self):
        t = tile.Tile(True)
        self.assertIsInstance(t, tile.Tile)
        self.assertTrue(t.blocked)


class TestGameMap(ut.TestCase):
    def testMakeMap(self):
        carte = game_map.GameMap(30, 30)
        constants = initialize_new_game.get_constants()
        new_game = initialize_new_game.get_game_variables(constants)
        player = new_game[0]
        entities = new_game[1]
        carte.make_map(5, 5, 8, 20, 20, player, entities)
        self.assertNotEqual(len(entities), 1)
        for e in entities:
            if e.fighter:
                self.assertTrue(e.blocks)

    def testInitializeTiles(self):
        carte = game_map.GameMap(30, 30)
        tiles = carte.initialize_tiles()
        for t in tiles:
            for t2 in t:
                self.assertIsInstance(t2, tile.Tile)
                self.assertTrue(not(t2.explored))


class TestGameMessages(ut.TestCase):
    def testMessageLog(self):
        constants = initialize_new_game.get_constants()
        new_game = initialize_new_game.get_game_variables(constants)
        message_log = new_game[3]
        self.assertTrue(message_log.messages == [])
        self.assertTrue(message_log.width <= constants.get('screen_width'))
        self.assertTrue(message_log.height <= constants.get('screen_height'))




if __name__ == "__main__":
    ut.main()
