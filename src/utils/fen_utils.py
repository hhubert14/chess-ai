from dataclasses import dataclass
from typing import Optional

from utils.board_utils import convert_fen_to_board_string

@dataclass
class FenInfo:
    """Structured representation of a chess position's FEN (Forsyth-Edwards Notation) components.
    
    Attributes:
        board: ASCII representation of the chess board
        player_to_move: Current player's turn ("White" or "Black")
        castling_rights: Available castling moves in human-readable format
        en_passant_target: Square where en passant capture is possible, or "None"
        halfmove_clock: Number of moves since last pawn move or capture (for 50-move rule)
        fullmove_number: Complete game move counter, starting from 1
    """
    board: str
    player_to_move: str
    castling_rights: str
    en_passant_target: str
    halfmove_clock: int
    fullmove_number: int

def parse_fen(fen: str) -> FenInfo:
    """Parse a Forsyth-Edwards Notation (FEN) string into structured game state information.
    
    Extracts and formats:
    - Board position as ASCII representation
    - Active player (White/Black)
    - Castling availability for both sides
    - En passant target square
    - Halfmove clock for 50-move rule
    - Fullmove counter
    
    Args:
        fen: A valid FEN string representing a chess position
        
    Returns:
        FenInfo: Dataclass containing parsed and formatted FEN components
    """
    components = fen.split(" ")
    
    castling_rights = ""
    if "K" in components[2]: castling_rights += "White can castle kingside. "
    if "Q" in components[2]: castling_rights += "White can castle queenside. "
    if "k" in components[2]: castling_rights += "Black can castle kingside. "
    if "q" in components[2]: castling_rights += "Black can castle queenside. "
    if components[2] == "-": castling_rights = "No castling rights remaining."

    return FenInfo(
        board=convert_fen_to_board_string(fen),
        player_to_move="White" if components[1] == "w" else "Black",
        castling_rights=castling_rights,
        en_passant_target=components[3] if components[3] != "-" else "None",
        halfmove_clock=int(components[4]),
        fullmove_number=int(components[5])
    )
