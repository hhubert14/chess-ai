"""
Parse Lichess puzzle database (lichess_db_puzzle.csv) into a simplified format.

Input: lichess_db_puzzle.csv
Output: lichess_puzzles.csv with columns:
- FEN: Chess position in FEN notation
- best_move: Best move in UCI notation (e.g., e2e4)

This simplified format is used for initial puzzle evaluation and filtering.
"""

import yaml
import os

import pandas as pd
from dotenv import load_dotenv

from utils import get_best_move

load_dotenv()

with open(os.getenv("CONFIG_PATH")) as file:
    config = yaml.safe_load(file)

BASE_DIR = config["BASE_DIR"]
INPUT_PATH = BASE_DIR + "src/data/datasets/puzzles/lichess_db_puzzle.csv"
OUTPUT_PATH = BASE_DIR + "src/data/datasets/puzzles/lichess_puzzles.csv"

# Read input puzzles
puzzles = pd.read_csv(INPUT_PATH)

# Pre-allocate list for results
results = []

# Process each puzzle
for index, puzzle in puzzles.iterrows():
    print(f"Parsing puzzle {index + 1}/{len(puzzles)}")
    puzzle_fen = puzzle["FEN"]
    best_move = get_best_move(puzzle_fen)
    results.append({"FEN": puzzle_fen, "best_move": best_move})
    if index % 1000 == 0:
        print(f"Saving results to {OUTPUT_PATH}")
        simplified_puzzles = pd.DataFrame(results)
        simplified_puzzles.to_csv(OUTPUT_PATH, index=False)

# Create DataFrame from results and save
simplified_puzzles = pd.DataFrame(results)
simplified_puzzles.to_csv(OUTPUT_PATH, index=False)

print(f"Processed {len(puzzles)} puzzles. Results saved to {OUTPUT_PATH}")
