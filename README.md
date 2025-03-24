# Used Chess Sites
- https://chesstempo.com/

# Puzzle Data
- https://database.lichess.org/#puzzles
- https://czoins.github.io/sorted-lichess-puzzles/
- https://github.com/rebeccaloran/432k-chess-puzzles
- https://www.wtharvey.com/

# TODOs
- [x] Gather puzzle FEN positions
- [x] Prepare csv file with different FEN positions and best move
- [ ] Create chain to loop through positions analyze positions and prediction best move
  - [ ] store these in another file
- [ ] In parse_lichess_puzzles.py, add the functionality to start at a specific row for lichess_db_puzzle.csv
- [ ] Write util to convert from UCI notation to algebraic notation
- [ ] Create a logger file instead of writing to console for debugging purposes.
- [ ] In generate_llm_data.py, instead of matching the best move exactly, accept moves that are also very close to the best move in terms of evaluation
- [ ] Add during inference: When deploying your model, you can include the notation explanation in your prompt template or you can add it as a system prompt:
```
Chess Position Notation Guide:
- K, Q, R, B, N, P represent white King, Queen, Rook, Bishop, Knight, and Pawn
- k, q, r, b, n, p represent black pieces
- Periods (.) represent empty squares
- Board is shown from White's perspective (a1 is bottom left)
```


# Future Considerations
- Test fine-tuning approach with vs without notation explanation (K, Q, R, B, N, P are the notations...explain why the best move is as shown:) - Most likely unnecessary
