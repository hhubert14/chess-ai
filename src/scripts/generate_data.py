from dotenv import load_dotenv
from openai import OpenAI

import os

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

prompt = """Below is an instruction that describes a task, paired with an input that provides further context.
Write a response that appropriately completes the request.
Before answering, think carefully about the chess position and construct a step-by-step reasoning process to ensure a logical and accurate response.

### Instruction:
K, Q, R, B, N, P are the notations for the white king, queen, rook, bishop, knight, and pawn respectively.
The notation for the black pieces are the same but with lowercased letters. A period represents an empty square.
Please analyze the following chess position:

. k . . . . . .
p p p . . . p p
q . n b . . . .
. . . . . . . .
n . . P . P . .
N . P . . . . .
. B . . . . P P
. R . . R . . K

Side to move: White

Castling rights: None

En passant target square: None

### Analysis:
When evaluating this position, consider the following key factors:

1. **Material Balance and Piece Placement:**
   - Evaluate the current material (pawns and pieces) and identify where key pieces are positioned.

2. **King Safety:**
   - Assess the safety of both kings. Identify any vulnerabilities or potential threats.

3. **Piece Activity and Coordination:**
   - Consider how active the pieces are, how well they are placed, and whether they support each other effectively.

4. **Pawn Structure and Control of the Center:**
   - Analyze the pawn formations, including weaknesses (e.g., doubled, isolated, or backward pawns) and the control of central squares.

5. **Development and Tactical Considerations:**
   - Look at the stage of development for both sides and be alert to any tactical opportunities or threats (forks, pins, skewers, etc.).

6. **Long-Term Strategic Plans and Opponent's Counterplay:**
   - Discuss potential strategic ideas and maneuvers for both sides, including possible counterplay from the opponent.

Using these points, provide your analysis with a step-by-step reasoning that includes:
   - An overview of the material balance and piece placement.
   - Identification of key squares and the influence of the pawn structure.
   - A main line calculation (2-3 moves deep) with reasoning.
   - Strategic plans for both sides along with considerations for opponent's counterplay.

### Best Move:
Based on the above analysis, return the best move in UCI notation (e.g., e2e4, e7e5, e1g1, e7e8q...):
UCI Notation: [fill in here]
"""
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        # {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt},
    ],
    stream=False
)

print(response.choices[0].message.content)