from runpy import run_module

# from scripts import generate_data

def main():
    run_module("scripts.parse_lichess_puzzles")
    # run_module("scripts.generate_llm_data")

if __name__ == "__main__":
    main()