import os
import chess.pgn
from stockfish import Stockfish
import csv

# Note: The comment might not always align with the objective best move

stockfish_path = "C:/Users/huang/repos/Personal/chess-ai/stockfish.exe"
pgn_folder_path = "C:/Users/huang/repos/Personal/chess-ai/pgn-files"
csv_file_path = "C:/Users/huang/repos/Personal/chess-ai/games_data.csv"

stockfish = Stockfish(path=stockfish_path)

def parse_pgns(directory_path):
    games_data = []

    pgn_files = [file for file in os.listdir(directory_path)]

    for file in pgn_files:
        # print(f"Parsing {file}")
        pgn = open(os.path.join(directory_path, file))

        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            # print(f"Parsing game {game}")

            board = game.board()

            for node in game.mainline():
                move = node.move
                board.push(move)

                # Inputs
                fen_string = board.fen()
                stockfish.set_fen_position(fen_string)
                best_move = stockfish.get_best_move()
                evaluation = stockfish.get_evaluation()

                # Label
                comment = node.comment if node.comment else ""

                if comment:
                    games_data.append({"inputs": f"FEN: {fen_string}. Best move: {best_move}. Evaluation: {evaluation['value']}. Explain why {best_move} is the best move.",
                                       "label": comment})

    return games_data
            
if __name__ == "__main__":
    games_data = parse_pgns(pgn_folder_path)

    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['inputs', 'label']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in games_data:
            writer.writerow(data)

    print(f"Games data saved to {csv_file_path}")