# Data

`nba_seasons.csv` has one row per NBA player per season, 1950 to 2017 (20,309 rows).
The numbers are season totals: games played, points, rebounds, assists.

Source: "The NBA CSV" (https://github.com/peasant98/TheNBACSV), which collects
player season stats originally published by Basketball-Reference.

Cleaning done once to make this file from the original:
- kept only the columns the project uses
- removed blank rows
- for a player traded mid-season, kept the combined "TOT" row and dropped the per-team rows
- removed the `*` that marks Hall of Fame players in the name
- blank numbers (rebounds were not recorded in 1950) became 0
