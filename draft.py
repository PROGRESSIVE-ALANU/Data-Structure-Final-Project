"""The draft board: who is the best player still available?

Data structures used:
  - MaxHeap of (fantasy score, player id) -> best available player on top
  - dict  player id -> player             -> O(1) lookup of any player
  - set   of drafted player ids           -> O(1) "is he taken?" check
  - dict  team name -> list of players    -> each team's roster
"""

from loader import load_players
from max_heap import MaxHeap


def fantasy_score(player):
    """One number for how valuable a player is, from his per-game stats."""
    score = (player["ppg"]
             + 1.2 * player["rpg"]
             + 1.5 * player["apg"]
             + 3.0 * player["spg"]
             + 3.0 * player["bpg"])
    return round(score, 1)


class DraftBoard:
    def __init__(self, players):
        self.by_id = {}         # player id -> player
        self.heap = MaxHeap()   # (score, player id), biggest score on top
        self.drafted = set()    # ids of players already taken
        self.teams = {}         # team name -> list of drafted players

        for player in players:
            player["score"] = fantasy_score(player)
            self.by_id[player["id"]] = player
            # The heap compares tuples by score first; the id breaks ties.
            self.heap.insert((player["score"], player["id"]))

    def is_available(self, player_id):
        return player_id in self.by_id and player_id not in self.drafted

    def best_available(self):
        """Return the best undrafted player, or None if nobody is left."""
        # Lazy deletion: a player drafted by name is still somewhere inside
        # the heap. We do not search for him. We just throw him away when
        # he finally reaches the top.
        while len(self.heap) > 0 and self.heap.peek()[1] in self.drafted:
            self.heap.remove()

        if len(self.heap) == 0:
            return None
        return self.by_id[self.heap.peek()[1]]

    def top(self, count):
        """Return the best `count` undrafted players, best first."""
        taken_off = []
        result = []
        # Take players off the top one at a time...
        while len(result) < count and self.best_available() is not None:
            entry = self.heap.remove()
            taken_off.append(entry)
            result.append(self.by_id[entry[1]])
        # ...then put them back, because looking is not drafting.
        for entry in taken_off:
            self.heap.insert(entry)
        return result

    def draft(self, player_id, team):
        """Put a specific player on a team. Returns the player."""
        if player_id not in self.by_id:
            raise ValueError(f"unknown player id: {player_id}")
        if player_id in self.drafted:
            raise ValueError(f"{self.by_id[player_id]['name']} is already drafted")

        self.drafted.add(player_id)
        if team not in self.teams:
            self.teams[team] = []
        self.teams[team].append(self.by_id[player_id])
        return self.by_id[player_id]

    def draft_best(self, team):
        """Put the best available player on a team (what a computer team does)."""
        player = self.best_available()
        if player is None:
            raise ValueError("no players left")
        return self.draft(player["id"], team)

    def team_score(self, team):
        """A team's strength: the sum of its players' fantasy scores."""
        return round(sum(p["score"] for p in self.teams.get(team, [])), 1)


def show(players):
    for player in players:
        print(f"  {player['score']:5.1f}  {player['name']} "
              f"({player['team']}, {player['pos']})")


def main():
    board = DraftBoard(load_players(season=2026))

    print("Top 5 available:")
    show(board.top(5))

    first = board.draft_best("Bots")
    print(f"\nBots take the best available: {first['name']}")
    mine = board.draft("gilgesh01", "Alan")
    print(f"Alan takes a specific player: {mine['name']}")

    print("\nTop 5 available now:")
    show(board.top(5))

    print(f"\nBots team score: {board.team_score('Bots')}")
    print(f"Alan team score: {board.team_score('Alan')}")


if __name__ == "__main__":
    main()
