"""Unit tests for loader.py.  Run with:  python3 -m unittest loader_test -v"""

import unittest

from loader import per_game, load_players, build_indexes


class TestLoader(unittest.TestCase):
    def test_per_game_rounds_to_one_decimal(self):
        self.assertEqual(per_game(1999, 79), 25.3)

    def test_loads_every_row(self):
        self.assertEqual(len(load_players()), 20309)

    def test_season_filter(self):
        players = load_players(season=2017)
        self.assertEqual(len(players), 486)
        self.assertTrue(all(p["season"] == 2017 for p in players))

    def test_known_player_stats(self):
        # Stephen Curry, 2017: 1999 points in 79 games.
        _, by_name = build_indexes(load_players(season=2017))
        curry = by_name["Stephen Curry"][0]
        self.assertEqual(curry["ppg"], 25.3)
        self.assertEqual(curry["team"], "GSW")

    def test_tree_and_dict_hold_the_same_players(self):
        players = load_players(season=2017)
        tree, by_name = build_indexes(players)
        self.assertEqual(len(tree), len(players))
        self.assertEqual(sum(len(s) for s in by_name.values()), len(players))

    def test_range_query_matches_a_plain_scan(self):
        players = load_players(season=2017)
        tree, _ = build_indexes(players)
        expected = [p["name"] for p in players if 20 <= p["ppg"] <= 30]
        found = [p["name"] for p in tree.range_query(20, 30)]
        self.assertEqual(sorted(found), sorted(expected))

    def test_name_maps_to_all_of_a_players_seasons(self):
        _, by_name = build_indexes(load_players())
        seasons = [p["season"] for p in by_name["Kobe Bryant"]]
        self.assertEqual(len(seasons), 20)


if __name__ == "__main__":
    unittest.main()
