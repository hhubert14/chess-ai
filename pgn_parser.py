import os
import chess.pgn
import chess.svg
from stockfish import Stockfish
import csv
import random

# Note: The comment might not always align with the objective best move

# Adjustable variables
stockfish_path = "C:/Users/huang/repos/Personal/chess-ai/stockfish.exe"
pgn_folder_path = "C:/Users/huang/repos/Personal/chess-ai/pgn-files"
train_csv_file_path = "C:/Users/huang/repos/Personal/chess-ai/train_dataset.csv"
test_csv_file_path = "C:/Users/huang/repos/Personal/chess-ai/test_dataset.csv"
test_set_percentage = 0.01

stockfish = Stockfish(path=stockfish_path)

def parse_pgns(directory_path):
    games_data = []

    pgn_files = [file for file in os.listdir(directory_path)]

    for file in pgn_files:
        print(f"Parsing {file}")

        pgn = open(os.path.join(directory_path, file))

        game_counter = 1

        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            print(f"Parsing game {game_counter}")

            game_counter += 1

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
                comment = node.comment.strip() if node.comment else ""

                player_to_move = 'White' if board.turn else 'Black'

                if comment:
                    # games_data.append({"inputs": f"It is {player_to_move}'s turn to move. The board position is:\n{fen_to_text(fen_string)}\nThe best move is {best_move} and the centipawn loss is {evaluation['value']}. Explain why {best_move} is the best move.",
                    #                    "label": comment})
                    games_data.append({"inputs": f"It is {player_to_move}'s turn to move. The board position is:\n{fen_to_text(fen_string)}\nThe best move is {best_move}. Explain why {best_move} is the best move.",
                                       "label": comment})
                    
    random.shuffle(games_data)

    split_idx = int(len(games_data) * test_set_percentage)
    
    train_dataset = games_data[split_idx:]
    test_dataset = games_data[:split_idx]

    return train_dataset, test_dataset

def fen_to_text(fen):
    board = chess.Board(fen)
    text = str(board)
    return text
            
if __name__ == "__main__":
    train_dataset, test_dataset = parse_pgns(pgn_folder_path)

    with open(train_csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['inputs', 'label']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in train_dataset:
            writer.writerow(data)

    with open(test_csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['inputs', 'label']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in test_dataset:
            writer.writerow(data)

    print(f"Games data saved to {train_csv_file_path} and {test_csv_file_path}")