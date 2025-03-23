import os

import yaml
from dotenv import load_dotenv
from stockfish import Stockfish

load_dotenv()

with open(os.getenv("CONFIG_PATH"), "r") as file:
    config = yaml.safe_load(file)

def get_best_move(fen_string: str, wtime: int = None) -> str:
    """Get the best move for a given position using Stockfish engine.
    """
    stockfish_path = config["stockfish_path"]

    stockfish = Stockfish(path=stockfish_path)

    stockfish.set_fen_position(fen_string)
    best_move = stockfish.get_best_move_time(wtime) if wtime else stockfish.get_best_move()
    return best_move
