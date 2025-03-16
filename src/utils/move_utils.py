from typing import Dict

from utils.board_utils import get_piece_at_square

PIECE_NAMES: Dict[str, str] = {
    "P": "pawn", "N": "knight", "B": "bishop",
    "R": "rook", "Q": "queen", "K": "king",
    "p": "pawn", "n": "knight", "b": "bishop",
    "r": "rook", "q": "queen", "k": "king",
}

def convert_move_to_text(fen: str, best_move: str) -> str:
    """Convert chess move to human-readable text."""
    start_pos = best_move[:2]
    end_pos = best_move[2:]

    start_piece = get_piece_at_square(fen, start_pos)
    end_piece = get_piece_at_square(fen, end_pos[:2])

    # Handle castling
    if start_piece in ["K", "k"]:
        if (start_pos == "e1" and end_pos == "g1") or \
           (start_pos == "e8" and end_pos == "g8"):
            return "castling kingside"
        if (start_pos == "e1" and end_pos == "c1") or \
           (start_pos == "e8" and end_pos == "c8"):
            return "castling queenside"
    
    # Handle en passant
    if start_piece in ["P", "p"]:
        if start_pos[0] != end_pos[0] and end_piece is None:
            return "en passant"
    
    # Handle promotion
    if _is_promotion_move(start_piece, start_pos, end_pos):
        return _format_promotion_text(start_pos, end_pos, start_piece, end_piece)
    
    # Handle regular moves
    return _format_regular_move(start_piece, start_pos, end_pos, end_piece)

def _is_promotion_move(piece: str, start_pos: str, end_pos: str) -> bool:
    """Check if move is a promotion."""
    return ((piece == "P" and start_pos[1] == "7" and end_pos[1] == "8") or
            (piece == "p" and start_pos[1] == "2" and end_pos[1] == "1"))

def _format_promotion_text(start_pos: str, end_pos: str, 
                         start_piece: str, end_piece: str) -> str:
    """Format text for promotion moves."""
    assert len(end_pos) == 3, "end_pos must be 3 letters long for promotion"
    
    if start_pos[0] == end_pos[0]:
        return f"pawn on {start_pos} promotes to {PIECE_NAMES[end_pos[2]]} on {end_pos}"
    return f"pawn on {start_pos} captures {PIECE_NAMES[end_piece]} on {end_pos} and promotes to {PIECE_NAMES[end_pos[2]]}"

def _format_regular_move(start_piece: str, start_pos: str, 
                        end_pos: str, end_piece: str) -> str:
    """Format text for regular moves."""
    if end_piece is None:
        return f"{PIECE_NAMES[start_piece]} on {start_pos} to {end_pos}"
    return f"{PIECE_NAMES[start_piece]} on {start_pos} captures {PIECE_NAMES[end_piece]} on {end_pos}"