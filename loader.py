"""Load real NBA player seasons and index them for fast lookups.

Two indexes are built from the same players:
  - a PlayerBST keyed by points per game  -> "who scored between X and Y?"
  - a dict keyed by player name           -> "show me this player"
"""

import csv

from bootstrap.player_bst import PlayerBST

DATA_FILE = "data/nba_seasons.csv"


def per_game(total, games):
    """Turn a season total into a per-game average with one decimal."""
    return round(total / games, 1)


def load_players(path=DATA_FILE, season=None):
    """Read the CSV and return a list of player dicts.

    Each row is one player in one season. If season is given
    (e.g. 2017), only that season is returned.
    """
    players = []
    with open(path, newline="") as stream:
        # DictReader uses the header row, so row["name"] works.
        for row in csv.DictReader(stream):
            if season is not None and int(row["season"]) != season:
                continue

            games = int(row["games"])
            players.append({
                "name": row["name"],
                "season": int(row["season"]),
                "team": row["team"],
                "pos": row["pos"],
                "games": games,
                "ppg": per_game(int(row["points"]), games),
                "rpg": per_game(int(row["rebounds"]), games),
                "apg": per_game(int(row["assists"]), games),
            })
    return players


def build_indexes(players):
    """Return (tree, by_name) built from a list of player dicts."""
    tree = PlayerBST()      # points per game -> players with that average
    by_name = {}            # name -> list of that player's seasons

    for player in players:
        tree.insert(player["ppg"], player)

        # A player has one entry per season, so each name maps to a list.
        if player["name"] not in by_name:
            by_name[player["name"]] = []
        by_name[player["name"]].append(player)

    return tree, by_name


def main():
    players = load_players(season=2017)
    tree, by_name = build_indexes(players)
    print(f"Loaded {len(players)} players from the 2017 season")
    print(f"Tree height: {tree.height()}")

    print("\nPlayers averaging 25 to 40 points per game:")
    for player in tree.range_query(25, 40):
        print(f"  {player['ppg']:5.1f}  {player['name']} ({player['team']})")

    print("\nLookup by name: Stephen Curry")
    for player in by_name["Stephen Curry"]:
        print(f"  {player['season']}: {player['ppg']} ppg, "
              f"{player['rpg']} rpg, {player['apg']} apg")


if __name__ == "__main__":
    main()
