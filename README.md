# Chess AI

A chess move prediction system that fine-tunes large language models to analyze board positions and predict optimal moves.

## Approach

1. **Data Collection** — Gather chess puzzle FEN positions from Lichess and other databases
2. **Data Preparation** — Parse positions and pair them with best-move labels in a structured CSV format
3. **LLM Fine-Tuning** — Fine-tune language models on FEN position analysis to predict strong moves
4. **Evaluation** — Compare predicted moves against engine-evaluated best moves

## Project Structure

```
chess-ai/
├── config/         # Configuration files
├── docs/           # Documentation and notes
├── engines/        # Chess engine integrations
├── notebooks/      # Jupyter notebooks for experiments
└── src/            # Source code for data processing and model training
```

## Data Sources

- [Lichess Puzzle Database](https://database.lichess.org/#puzzles)
- [Sorted Lichess Puzzles](https://czoins.github.io/sorted-lichess-puzzles/)
- [432k Chess Puzzles](https://github.com/rebeccaloran/432k-chess-puzzles)

## Tech Stack

- Python, Jupyter Notebooks
- LLM fine-tuning (LoRA)
- Chess position encoding (FEN notation)
