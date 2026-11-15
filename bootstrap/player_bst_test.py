"""Unit tests for player_bst.py.  Run with:  python3 -m unittest player_bst_test -v"""

import random
import unittest

from player_bst import PlayerBST


def small_tree():
    """A tree with keys 20..80 and one tie at 40."""
    tree = PlayerBST()
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key, f"p{key}")
    tree.insert(40, "p40b")
    return tree


class TestPlayerBST(unittest.TestCase):
    def test_empty_tree(self):
        self.assertEqual(PlayerBST().range_query(0, 100), [])

    def test_len_counts_players_not_nodes(self):
        self.assertEqual(len(small_tree()), 8)

    def test_middle_range_is_sorted_and_keeps_ties(self):
        self.assertEqual(small_tree().range_query(35, 65),
                         ["p40", "p40b", "p50", "p60"])

    def test_bounds_are_inclusive(self):
        self.assertEqual(small_tree().range_query(30, 50),
                         ["p30", "p40", "p40b", "p50"])

    def test_single_key(self):
        self.assertEqual(small_tree().range_query(20, 20), ["p20"])

    def test_range_with_no_players(self):
        self.assertEqual(small_tree().range_query(81, 90), [])
        self.assertEqual(small_tree().range_query(41, 49), [])

    def test_backwards_range(self):
        self.assertEqual(small_tree().range_query(60, 30), [])

    def test_whole_range(self):
        self.assertEqual(len(small_tree().range_query(0, 100)), 8)

    def test_matches_a_plain_list_scan(self):
        # On random data the tree must agree with the obvious slow method.
        random.seed(1)
        stats = [round(random.uniform(0, 40), 1) for _ in range(2000)]
        tree = PlayerBST()
        for i, stat in enumerate(stats):
            tree.insert(stat, i)
        expected = [i for i, stat in enumerate(stats) if 10 <= stat <= 15]
        self.assertEqual(sorted(tree.range_query(10, 15)), sorted(expected))


if __name__ == "__main__":
    unittest.main()
