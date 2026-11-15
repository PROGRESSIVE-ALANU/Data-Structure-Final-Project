"""Load real NBA player seasons and index them for fast lookups.

Three indexes are built from the same players:
  - a PlayerBST keyed by points per game   -> "who scored between X and Y?"
  - a dict keyed by player id              -> "show me this exact player"
  - a dict keyed by plain name             -> "which player ids have this name?"

Two different players can share a name (there are two Brandon Williams),
so the player id, not the name, is what identifies a player.
"""

import csv
import unicodedata

from bootstrap.player_bst import PlayerBST

DATA_FILE = "data/nba_seasons.csv"


def to_number(text):
    """Turn a CSV cell into a float. A blank cell (stat not recorded) is 0."""
    if text == "":
        return 0.0
    return float(text)


def plain(name):
    """Lowercase a name and remove accents, so 'Luka Dončić' -> 'luka doncic'.

    This lets a user type a name on a normal keyboard and still find it.
    """
    # NFKD splits 'č' into 'c' plus a separate accent mark;
    # combining() is true for the accent marks, so we drop them.
    letters = unicodedata.normalize("NFKD", name)
    return "".join(c for c in letters if not unicodedata.combining(c)).lower()


def load_players(path=DATA_FILE, season=None):
    """Read the CSV and return a list of player dicts.

    Each row is one player in one season. If season is given
    (e.g. 2026), only that season is returned.
    """
    players = []
    with open(path, newline="", encoding="utf-8") as stream:
        # DictReader uses the header row, so row["name"] works.
        for row in csv.DictReader(stream):
            if season is not None and int(row["season"]) != season:
                continue

            players.append({
                "id": row["player_id"],
                "name": row["name"],
                "season": int(row["season"]),
                "team": row["team"],
                "pos": row["pos"],
                "games": int(row["games"]),
                "ppg": to_number(row["ppg"]),
                "rpg": to_number(row["rpg"]),
                "apg": to_number(row["apg"]),
                "spg": to_number(row["spg"]),
                "bpg": to_number(row["bpg"]),
            })
    return players


def build_indexes(players):
    """Return (tree, by_id, ids_by_name) built from a list of player dicts."""
    tree = PlayerBST()      # points per game -> players with that average
    by_id = {}              # player id -> list of that player's seasons
    ids_by_name = {}        # plain name -> list of player ids with that name

    for player in players:
        tree.insert(player["ppg"], player)

        # A player has one entry per season, so each id maps to a list.
        if player["id"] not in by_id:
            by_id[player["id"]] = []
        by_id[player["id"]].append(player)

        # Usually one id per name, but shared names get more than one.
        key = plain(player["name"])
        if key not in ids_by_name:
            ids_by_name[key] = []
        if player["id"] not in ids_by_name[key]:
            ids_by_name[key].append(player["id"])

    return tree, by_id, ids_by_name


def find_player(name, by_id, ids_by_name):
    """Return one list of seasons for each player with this name."""
    ids = ids_by_name.get(plain(name), [])
    return [by_id[player_id] for player_id in ids]


def main():
    players = load_players(season=2026)
    tree, by_id, ids_by_name = build_indexes(players)
    print(f"Loaded {len(players)} players from the 2025-26 season")
    print(f"Tree height: {tree.height()}")

    print("\nPlayers averaging 27 or more points per game:")
    for player in tree.range_query(27, 60):
        print(f"  {player['ppg']:5.1f}  {player['name']} ({player['team']})")

    print("\nLookup by name: luka doncic")
    for seasons in find_player("luka doncic", by_id, ids_by_name):
        for player in seasons:
            print(f"  {player['season']} {player['name']}: {player['ppg']} ppg, "
                  f"{player['rpg']} rpg, {player['apg']} apg")


if __name__ == "__main__":
    main()
