POSITION_ASSESSMENT_PROMPT = """K, Q, R, B, N, P are the notations for the white king, queen, rook, bishop, knight, and pawn respectively.
The notation for the black pieces are the same but with lowercased letters. A period represents an empty square.
Assess the material balance and piece placement in the following chess position:

{board}

Side to move: {side_to_move}
Castling rights: {castling_rights}
En passant target square: {en_passant_target_square}

Provide a detailed evaluation of:
1. The current material count for both sides (e.g., pawns, minor pieces, major pieces)
2. Key piece placements and their influence on the position
3. Overall material advantage/disadvantage and its significance

Respond with a concise but complete assessment of the material situation.
"""

KING_SAFETY_PROMPT = """Based on the following chess position and material assessment:

{board}

Side to move: {side_to_move}
Castling rights: {castling_rights}
En passant target square: {en_passant_target_square}

Material assessment: {material_assessment}

Analyze the safety of both kings by considering:
1. Pawn shield integrity around each king
2. Potential attack vectors toward each king
3. Nearby defensive pieces
4. Any immediate threats or potential threats in the next few moves
5. Relative king safety comparison between both sides

Respond with a focused analysis of king safety issues for both sides.
"""

TACTICAL_ANALYSIS_PROMPT = """Based on the following chess position and previous assessments:

{board}

Side to move: {side_to_move}
Castling rights: {castling_rights}
En passant target square: {en_passant_target_square}

Material assessment: {material_assessment}
King safety assessment: {king_safety_assessment}

Analyze the tactical elements of this position:
1. Identify any immediate tactical opportunities (forks, pins, skewers, discovered attacks, etc.)
2. Evaluate piece activity and coordination for both sides
3. Note any hanging or undefended pieces
4. Identify key squares that should be controlled or contested
5. Calculate any forced sequences (2-3 moves deep) that could be advantageous

Respond with a tactical evaluation focused on immediate opportunities and threats.
"""

STRATEGIC_ANALYSIS_PROMPT = """Based on the following chess position and previous assessments:

{board}

Side to move: {side_to_move}
Castling rights: {castling_rights}
En passant target square: {en_passant_target_square}

Material assessment: {material_assessment}
King safety assessment: {king_safety_assessment}
Tactical assessment: {tactical_assessment}

Provide a strategic and positional evaluation of the position:
1. Analyze the pawn structure and its implications
2. Evaluate control of key squares and the center
3. Assess piece mobility and potential improvements
4. Identify long-term plans for both sides
5. Consider possible counterplay and defensive resources

Respond with a forward-looking strategic assessment that builds upon the tactical and material considerations already identified.
"""

BEST_MOVE_PROMPT = """Based on the following chess position and complete analysis:

{board}

Side to move: {side_to_move}
Castling rights: {castling_rights}
En passant target square: {en_passant_target_square}

Material assessment: {material_assessment}
King safety assessment: {king_safety_assessment}
Tactical assessment: {tactical_assessment}
Strategic assessment: {strategic_assessment}

Determine the single best move in this position:
1. Consider the 2-3 most promising candidate moves
2. For each candidate, calculate the main line (2-3 moves deep)
3. Evaluate the resulting positions
4. Select the move that best addresses the key factors identified in the analysis

Return the best move in UCI notation (e.g., e2e4, e7e5, e1g1, e7e8q) and explain why this move is optimal, referencing specific elements from the previous analyses.

UCI Notation: 
"""

# Might be unnecessary
COMBINED_ANALYSIS_PROMPT = """Position Analysis Summary

Chess Position:
{board}

Side to move: {side_to_move}
Castling rights: {castling_rights}
En passant target square: {en_passant_target_square}

Material Assessment:
{material_assessment}

King Safety Assessment:
{king_safety_assessment}

Tactical Assessment:
{tactical_assessment}

Strategic Assessment:
{strategic_assessment}

Best Move Analysis:
{best_move_analysis}

Final UCI Move: {uci_move}
"""