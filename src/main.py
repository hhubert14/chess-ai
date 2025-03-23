from runpy import run_module

# from scripts import generate_data

def main():
    # run_module("scripts.generate_data")
    run_module("scripts.parse_lichess_puzzles")

if __name__ == "__main__":
    main()