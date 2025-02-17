import os
import chess.pgn
import chess.svg
from stockfish import Stockfish
import csv
import random
from functions.functions import convert_fen_to_board_string, parse_fen

# Adjustable variables
stockfish_path = "C:/Users/huang/repos/Personal/chess-ai/stockfish.exe"
pgn_folder_path = "C:/Users/huang/repos/Personal/chess-ai/pgn-files"
train_csv_file_path = "C:/Users/huang/repos/Personal/chess-ai/train_dataset.csv"
test_csv_file_path = "C:/Users/huang/repos/Personal/chess-ai/test_dataset.csv"
test_set_percentage = 0.01

stockfish = Stockfish(path=stockfish_path)

def parse_pgns(directory_path):
	dataset = []

	pgn_files = [file for file in os.listdir(directory_path)]

	for file in pgn_files:
		print(f"Parsing {file}")

		pgn = open(os.path.join(directory_path, file))

		game_count = 1

		while True:
			game = chess.pgn.read_game(pgn) # Gets current game in pgn
			if game is None:
				break

			print(f"Parsing game {game_count}")

			game_count += 1

			board = game.board()

			for node in game.mainline():
				move = node.move
				board.push(move)

				# Inputs
				fen_string = board.fen()
				parsed_fen = parse_fen(fen_string)
				stockfish.set_fen_position(fen_string)
				# best_move = stockfish.get_best_move()
				top_moves = stockfish.get_top_moves(10)
				print(parsed_fen["player_to_move"])
				print(top_moves)
				print()

				# evaluation = stockfish.get_evaluation()

				# # Label
				# comment = node.comment.strip() if node.comment else ""

				# player_to_move = 'White' if board.turn else 'Black'

				dataset.append({"board": parsed_fen["board"],
								"side to move": parsed_fen["player_to_move"],
								"castling rights": parsed_fen["castling_rights"],
								"en passant target square": parsed_fen["en_passant_target"],
								})
					
	random.shuffle(dataset)

	split_idx = int(len(dataset) * test_set_percentage)
	
	train_dataset = dataset[split_idx:]
	test_dataset = dataset[:split_idx]

	return train_dataset, test_dataset
			
if __name__ == "__main__":
	# print(convert_fen_to_board_string("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"))
	train_dataset, test_dataset = parse_pgns(pgn_folder_path)

	# with open(train_csv_file_path, mode='w', newline='') as csv_file:
	#     fieldnames = ['inputs', 'label']
	#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

	#     writer.writeheader()
	#     for data in train_dataset:
	#         writer.writerow(data)

	# with open(test_csv_file_path, mode='w', newline='') as csv_file:
	#     fieldnames = ['inputs', 'label']
	#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

	#     writer.writeheader()
	#     for data in test_dataset:
	#         writer.writerow(data)

	# print(f"Games data saved to {train_csv_file_path} and {test_csv_file_path}")