"""Unit tests for max_heap.py and draft.py.

Run with:  python3 -m unittest draft_test -v
"""

import random
import unittest

from draft import DraftBoard, fantasy_score
from max_heap import MaxHeap


def make_player(player_id, ppg):
    """A small fake player whose fantasy score equals his points."""
    return {"id": player_id, "name": player_id.upper(), "team": "ND",
            "pos": "G", "ppg": ppg, "rpg": 0.0, "apg": 0.0,
            "spg": 0.0, "bpg": 0.0}


def small_board():
    return DraftBoard([make_player("a", 10.0), make_player("b", 30.0),
                       make_player("c", 20.0), make_player("d", 25.0)])


class TestMaxHeap(unittest.TestCase):
    def test_removes_in_descending_order(self):
        heap = MaxHeap()
        for value in [5, 1, 9, 3, 7]:
            heap.insert(value)
        self.assertEqual([heap.remove() for _ in range(5)], [9, 7, 5, 3, 1])

    def test_peek_does_not_remove(self):
        heap = MaxHeap()
        heap.insert(4)
        heap.insert(8)
        self.assertEqual(heap.peek(), 8)
        self.assertEqual(len(heap), 2)

    def test_matches_sorting_on_random_values(self):
        random.seed(9)
        values = [random.randint(0, 1000) for _ in range(500)]
        heap = MaxHeap()
        for value in values:
            heap.insert(value)
        removed = [heap.remove() for _ in range(len(values))]
        self.assertEqual(removed, sorted(values, reverse=True))

    def test_parent_is_never_smaller_than_child(self):
        random.seed(3)
        heap = MaxHeap()
        for _ in range(200):
            heap.insert(random.random())
        array = heap.heap_array
        for i in range(1, len(array)):
            self.assertGreaterEqual(array[(i - 1) // 2], array[i])


class TestFantasyScore(unittest.TestCase):
    def test_formula(self):
        player = {"ppg": 20.0, "rpg": 10.0, "apg": 4.0, "spg": 1.0, "bpg": 2.0}
        # 20 + 1.2*10 + 1.5*4 + 3*1 + 3*2 = 47
        self.assertEqual(fantasy_score(player), 47.0)


class TestDraftBoard(unittest.TestCase):
    def test_best_available_is_highest_score(self):
        self.assertEqual(small_board().best_available()["id"], "b")

    def test_top_is_sorted_and_does_not_draft(self):
        board = small_board()
        self.assertEqual([p["id"] for p in board.top(3)], ["b", "d", "c"])
        self.assertEqual([p["id"] for p in board.top(3)], ["b", "d", "c"])

    def test_top_with_more_than_exist(self):
        self.assertEqual(len(small_board().top(10)), 4)

    def test_draft_best_takes_players_in_order(self):
        board = small_board()
        picks = [board.draft_best("Bots")["id"] for _ in range(4)]
        self.assertEqual(picks, ["b", "d", "c", "a"])
        self.assertIsNone(board.best_available())

    def test_drafting_a_specific_player_removes_him_from_the_top(self):
        board = small_board()
        board.draft("b", "Alan")              # b is in the heap's top spot
        self.assertEqual(board.best_available()["id"], "d")

    def test_drafting_from_the_middle_is_skipped_later(self):
        board = small_board()
        board.draft("d", "Alan")              # d is not on top yet
        self.assertEqual([p["id"] for p in board.top(4)], ["b", "c", "a"])

    def test_cannot_draft_twice(self):
        board = small_board()
        board.draft("c", "Alan")
        with self.assertRaises(ValueError):
            board.draft("c", "Bots")

    def test_unknown_player(self):
        with self.assertRaises(ValueError):
            small_board().draft("zzz", "Alan")

    def test_draft_best_when_empty(self):
        board = DraftBoard([])
        with self.assertRaises(ValueError):
            board.draft_best("Bots")

    def test_is_available(self):
        board = small_board()
        board.draft("a", "Alan")
        self.assertFalse(board.is_available("a"))
        self.assertTrue(board.is_available("b"))
        self.assertFalse(board.is_available("zzz"))

    def test_team_score_adds_up(self):
        board = small_board()
        board.draft("b", "Alan")
        board.draft("a", "Alan")
        self.assertEqual(board.team_score("Alan"), 40.0)
        self.assertEqual(board.team_score("Nobody"), 0.0)


if __name__ == "__main__":
    unittest.main()
