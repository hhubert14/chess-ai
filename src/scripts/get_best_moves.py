import pandas as pd

from utils import get_best_move

puzzles = pd.read_csv("C:/Users/huang/repos/Personal/chess-ai/src/data/datasets/easy_puzzles.csv")

print(get_best_move("7k/1p3Q1p/p3Rnr1/2p5/r7/7P/1P1q1PP1/4R1K1 w - - 0 1"))