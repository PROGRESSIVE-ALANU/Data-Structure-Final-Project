"""Unit tests for loader.py.  Run with:  python3 -m unittest loader_test -v"""

import unittest

from loader import to_number, plain, load_players, build_indexes, find_player


class TestHelpers(unittest.TestCase):
    def test_to_number(self):
        self.assertEqual(to_number("25.3"), 25.3)
        self.assertEqual(to_number(""), 0.0)

    def test_plain_removes_accents_and_case(self):
        self.assertEqual(plain("Luka Dončić"), "luka doncic")
        self.assertEqual(plain("LeBron James"), "lebron james")


class TestLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load once and share between tests, because reading the file is slow.
        cls.players = load_players()
        cls.tree, cls.by_id, cls.ids_by_name = build_indexes(cls.players)

    def test_loads_every_row(self):
        self.assertEqual(len(self.players), 25319)

    def test_season_filter(self):
        players = load_players(season=2026)
        self.assertEqual(len(players), 582)
        self.assertTrue(all(p["season"] == 2026 for p in players))

    def test_known_player_stats(self):
        # Stephen Curry averaged 25.3 points for Golden State in 2016-17.
        curry = [p for p in self.by_id["curryst01"] if p["season"] == 2017][0]
        self.assertEqual(curry["ppg"], 25.3)
        self.assertEqual(curry["team"], "GSW")

    def test_missing_stat_becomes_zero(self):
        # Steals were not recorded in 1950.
        self.assertTrue(all(p["spg"] == 0.0
                            for p in self.players if p["season"] == 1950))

    def test_tree_and_dict_hold_the_same_players(self):
        self.assertEqual(len(self.tree), len(self.players))
        self.assertEqual(sum(len(s) for s in self.by_id.values()),
                         len(self.players))

    def test_range_query_matches_a_plain_scan(self):
        expected = [p["id"] for p in self.players if 20 <= p["ppg"] <= 30]
        found = [p["id"] for p in self.tree.range_query(20, 30)]
        self.assertEqual(sorted(found), sorted(expected))

    def test_id_maps_to_all_of_a_players_seasons(self):
        self.assertEqual(len(self.by_id["bryanko01"]), 20)

    def test_find_player_ignores_accents_and_case(self):
        found = find_player("LUKA DONCIC", self.by_id, self.ids_by_name)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0][0]["name"], "Luka Dončić")

    def test_players_who_share_a_name_stay_separate(self):
        found = find_player("Brandon Williams", self.by_id, self.ids_by_name)
        self.assertEqual(len(found), 2)
        self.assertNotEqual(found[0][0]["id"], found[1][0]["id"])

    def test_unknown_name(self):
        self.assertEqual(find_player("Nobody Here", self.by_id,
                                     self.ids_by_name), [])


if __name__ == "__main__":
    unittest.main()
