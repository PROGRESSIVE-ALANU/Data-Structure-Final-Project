"""Bootstrap benchmark: BST range query vs. list scan vs. pandas filter.

Run with:  python3 benchmark.py
Prints a table of times and saves benchmark.png.
"""

import random
import time

import matplotlib
matplotlib.use("Agg")               # draw to a file, no window needed
import matplotlib.pyplot as plt
import pandas as pd

from player_bst import PlayerBST

SIZES = [100, 1000, 5000, 10000, 50000]   # number of players to test
REPEATS = 50                              # run each query this many times
QUERIES = {"narrow (28-40 ppg, few players)": (28.0, 40.0),
           "wide (2-20 ppg, most players)": (2.0, 20.0)}


def make_players(n):
    """Make n fake players. Most score a little, a few score a lot."""
    players = []
    for i in range(n):
        ppg = min(round(random.expovariate(1 / 8), 1), 40.0)
        players.append({"name": f"Player{i}", "ppg": ppg})
    return players


def average_time(function):
    """Call function REPEATS times; return the average time in milliseconds."""
    start = time.perf_counter()
    for _ in range(REPEATS):
        function()
    return (time.perf_counter() - start) / REPEATS * 1000


def main():
    random.seed(20312)
    # times[query name][method name] = list of times, one per size
    times = {q: {"BST": [], "list scan": [], "pandas": []} for q in QUERIES}

    for n in SIZES:
        players = make_players(n)

        # Build the three structures from the same players.
        tree = PlayerBST()
        for player in players:
            tree.insert(player["ppg"], player)
        frame = pd.DataFrame(players)

        print(f"\nN = {n}  (tree height {tree.height()})")
        for name, (lo, hi) in QUERIES.items():
            # The three ways to answer "who has lo <= ppg <= hi?"
            def use_bst():
                return tree.range_query(lo, hi)

            def use_list():
                return [p for p in players if lo <= p["ppg"] <= hi]

            def use_pandas():
                return frame[(frame["ppg"] >= lo) & (frame["ppg"] <= hi)]

            # All three must find the same number of players.
            k = len(use_bst())
            assert k == len(use_list()) == len(use_pandas())

            print(f"  {name}: K = {k}")
            for method, function in [("BST", use_bst),
                                     ("list scan", use_list),
                                     ("pandas", use_pandas)]:
                ms = average_time(function)
                times[name][method].append(ms)
                print(f"    {method:10s} {ms:8.4f} ms")

    # One chart per query, time against N.
    figure, axes = plt.subplots(1, 2, figsize=(11, 4))
    for axis, name in zip(axes, QUERIES):
        for method, values in times[name].items():
            axis.plot(SIZES, values, marker="o", label=method)
        axis.set_title(name)
        axis.set_xlabel("number of players (N)")
        axis.set_ylabel("time per query (ms)")
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.legend()
    figure.tight_layout()
    figure.savefig("benchmark.png", dpi=150)
    print("\nSaved benchmark.png")


if __name__ == "__main__":
    main()
