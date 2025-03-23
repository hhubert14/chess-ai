import pandas as pd

from utils import get_best_move

# puzzles = pd.read_csv("C:/Users/huang/repos/Personal/chess-ai/src/data/datasets/puzzles/lichess_db_puzzle.csv")

# print(puzzles.head)
print(get_best_move("3r4/2R2pb1/4pk1p/6p1/8/3P3P/Pr3qP1/4QR1K b - - 0 1"))