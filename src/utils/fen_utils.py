from dataclasses import dataclass
from typing import Optional

from utils.board_utils import convert_fen_to_board_string

@dataclass
class FenInfo:
    """Structured FEN information."""
    board: str
    player_to_move: str
    castling_rights: str
    en_passant_target: str
    halfmove_clock: int
    fullmove_number: int

def parse_fen(fen: str) -> FenInfo:
    """Parse FEN string into structured information."""
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