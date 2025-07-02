# best-league-teams-by-alphabet-coverage
Simple Python script which generates League of Legends teams that have the most unique alphabetic characters. 

## Usage:
Run `main.py` with Python 3.10+.

If you want to try bigger/smaller teams (default is 5), change the variable `team_size` under the `if __name__ == "__main__"` block.

## Performance:
`team_size=5` takes about 2 seconds on my machine (R7 5700X3D) and `team_size=7` takes about 10 seconds.  
It's largely CPU-bound (single thread) but doesn't take much memory due to the DFS-style search.  
