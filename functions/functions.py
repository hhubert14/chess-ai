import chess

def convert_fen_to_board_string(fen: str):
    board = chess.Board(fen)
    text = str(board)
    return text

def parse_fen(fen: str):
    components = fen.split(" ")
    player_to_move = "White" if components[1] == "w" else "Black"
    castling_rights = ""
    if "K" in components[2]:
        castling_rights += "White can castle kingside. "
    if "Q" in components[2]:
        castling_rights += "White can castle queenside. "
    if "k" in components[2]:
        castling_rights += "Black can castle kingside. "
    if "q" in components[2]:
        castling_rights += "Black can castle queenside. "
    if components[2] == "-":
        castling_rights = "No castling rights remaining."
    en_passant_target_square = components[3] if components[3] != "-" else "None"
    return {
        "board": convert_fen_to_board_string(fen),
        "player_to_move": player_to_move,
        "castling_rights": castling_rights,
        "en_passant_target": en_passant_target_square,
        "halfmove_clock": int(components[4]),
        "fullmove_number": int(components[5])
    }


def convert_move_to_text(fen: str, best_move: str):
    letter_to_word = {
        "P": "pawn",
        "N": "knight",
        "B": "bishop",
        "R": "rook",
        "Q": "queen",
        "K": "king",
        "p": "pawn",
        "n": "knight",
        "b": "bishop",
        "r": "rook",
        "q": "queen",
        "k": "king",
    }
    start_pos = best_move[:2]
    end_pos = best_move[2:]

    start_piece = get_piece_at_square(fen, start_pos)
    end_piece = get_piece_at_square(fen, end_pos[:2])

    # Castling
    if start_piece == "K":
        if start_pos == "e1" and end_pos == "g1":
            return "castling kingside"
        if start_pos == "e1" and end_pos == "c1":
            return "castling queenside"
    
    if start_piece == "k":
        if start_pos == "e8" and end_pos == "g8":
            return "castling kingside"
        if start_pos == "e8" and end_pos == "c8":
            return "castling queenside"
    
    # En passant
    if start_piece == "P" or start_piece == "p":
        if start_pos[0] != end_pos[0] and end_piece == None:
            return "en passant"
    
    # Promotion
    if start_piece == "P" and start_pos[1] == "7" and end_pos[1] == "8":
        assert len(end_pos) == 3, "end_pos is not 3 letters long"
        if start_pos[0] == end_pos[0]:
            return f"pawn on {start_pos} promotes to {letter_to_word[end_pos[2]]} on {end_pos}"
        else:
            return f"pawn on {start_pos} captures {letter_to_word[end_piece]} on {end_pos} and promotes to {letter_to_word[end_pos[2]]}"
    if start_piece == "p" and start_pos[1] == "2" and end_pos[1] == "1":
        assert len(end_pos) == 3, "end_pos is not 3 letters long"
        if start_pos[0] == end_pos[0]:
            return f"pawn on {start_pos} promotes to {letter_to_word[end_pos[2]]} on {end_pos}"
        else:
            return f"pawn on {start_pos} captures {letter_to_word[end_piece]} on {end_pos} and promotes to {letter_to_word[end_pos[2]]}"
    
    # Other
    if end_piece == None:
        return f"{letter_to_word[start_piece]} on {start_pos} to {end_pos}"
    else:
        return f"{letter_to_word[start_piece]} on {start_pos} captures {letter_to_word[end_piece]} on {end_pos}"

def get_piece_at_square(fen: str, square: str):
    board = chess.Board(fen)
    piece = board.piece_at(chess.parse_square(square))
    return piece.symbol() if piece else None

# def fen_to_