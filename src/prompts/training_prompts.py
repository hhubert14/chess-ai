INPUT_PROMPT = """Analyze why the following move is best in this chess position:

POSITION:
{board}

GAME INFO:
- Side to move: {side_to_move}
- Castling rights: {castling_rights}
- En passant target square: {en_passant_target_square}

BEST MOVE: {best_move}
"""

INPUT_PROMPT_W_ALG_NOT = """Analyze why the following move is best in this chess position:

POSITION:
{board}

GAME INFO:
- Side to move: {side_to_move}
- Castling rights: {castling_rights}
- En passant target square: {en_passant_target_square}

BEST MOVE: {best_move} ({move_in_algebraic_notation})
"""

OUTPUT_PROMPT = """# Chess Position Analysis

## Material Assessment
{material_assessment}

## King Safety Assessment
{king_safety_assessment}

## Tactical Assessment
{tactical_assessment}

## Strategic Assessment
{strategic_assessment}

## Best Move Analysis
{best_move_analysis}
"""