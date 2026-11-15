# Data

`nba_seasons.csv` has one row per NBA player per season, from 1950 through 2026
(the 2025-26 season): 25,319 rows covering 4,915 players. The stats are per-game averages.

| Column | Meaning |
| --- | --- |
| `season` | The year the season ended (2026 means 2025-26) |
| `player_id` | Basketball-Reference's unique id for the player |
| `name`, `pos`, `age`, `team` | Player details for that season |
| `games` | Games played |
| `ppg`, `rpg`, `apg`, `spg`, `bpg` | Points, rebounds, assists, steals, blocks per game |

Source: Sumitro Datta's Basketball-Reference datasets
(https://github.com/sumitrodatta/bball-reference-datasets, file `Player Per Game.csv`),
which collect statistics published by Basketball-Reference.com.

Cleaning done once to make this file from the original:
- kept NBA seasons 1950 to 2026 (dropped the BAA, the ABA, and the unfinished 2027 season)
- kept only the columns the project uses
- for a player traded mid-season, kept the combined row (team `2TM`, `3TM`, ...) and dropped the per-team rows
- left a stat blank where it was not recorded (rebounds before 1951, steals and blocks before 1974)
