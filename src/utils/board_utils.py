import chess

def convert_fen_to_board_string(fen: str) -> str:
    """Convert FEN string to a readable board representation."""
    board = chess.Board(fen)
    return str(board)

def get_piece_at_square(fen: str, square: str) -> str | None:
    """Get the piece symbol at a specific square."""
    board = chess.Board(fen)
    piece = board.piece_at(chess.parse_square(square))
    return piece.symbol() if piece else None