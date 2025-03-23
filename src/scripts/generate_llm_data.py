import os
import re
import sys

from dotenv import load_dotenv
import yaml
# from openai import OpenAI
import pandas as pd
from langchain_deepseek import ChatDeepSeek
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils import parse_fen, safe_invoke
from errors import CSV_READ_ERROR

load_dotenv()

with open(os.getenv("CONFIG_PATH")) as file:
    config = yaml.safe_load(file)

BASE_DIR = config["BASE_DIR"]
INPUT_DIR = os.path.join("src", "data", "datasets", "puzzles", "playground_puzzles.csv")
OUTPUT_DIR = os.path.join("src", "data", "datasets", "llm_finetuning", "playground_dataset.csv")

from prompts import (
    SYSTEM_PROMPT,
    POSITION_ASSESSMENT_PROMPT,
    KING_SAFETY_PROMPT,
    TACTICAL_ANALYSIS_PROMPT,
    STRATEGIC_ANALYSIS_PROMPT,
    BEST_MOVE_PROMPT,
    INPUT_PROMPT,
    OUTPUT_PROMPT,
)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

llm = ChatDeepSeek(
    api_key=DEEPSEEK_API_KEY,
    model="deepseek-reasoner",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

try:
    puzzles = pd.read_csv(BASE_DIR + INPUT_DIR)
    dataset = pd.read_csv(BASE_DIR + OUTPUT_DIR)
except Exception as e:
    print(f"Error with reading csvs: {e}")
    sys.exit(CSV_READ_ERROR)

for index, puzzle in puzzles.iterrows():
    print(f"Processing puzzle {index + 1}/{len(puzzles)}")
    fen_info = parse_fen(puzzle["FEN"])
    base_info = {
        "board": fen_info.board,
        "side_to_move": fen_info.player_to_move,
        "castling_rights": fen_info.castling_rights,
        "en_passant_target_square": fen_info.en_passant_target,
    }

    # Position Assessment
    print("Analyzing Position")
    position_assessment_prompt = ChatPromptTemplate(
        [
            ("system", SYSTEM_PROMPT),
            ("human", POSITION_ASSESSMENT_PROMPT),
        ]
    )
    position_chain = position_assessment_prompt | llm
    position_result = safe_invoke(position_chain, base_info)
    if not position_result:
        print("Failed to get position assessment. Skipping puzzle.")
        continue

    # King Safety Assessment
    print("Analyzing King Safety")
    king_safety_prompt = ChatPromptTemplate.from_template(KING_SAFETY_PROMPT)
    king_safety_chain = king_safety_prompt | llm
    king_safety_result = safe_invoke(king_safety_chain, {
        **base_info,
        "material_assessment": position_result
    })
    if not king_safety_result:
        print("Failed to get king safety assessment. Skipping puzzle.")
        continue

    # Tactical Analysis
    print("Analyzing Tactical Analysis")
    tactical_analysis_prompt = ChatPromptTemplate.from_template(TACTICAL_ANALYSIS_PROMPT)
    tactical_analysis_chain = tactical_analysis_prompt | llm
    tactical_analysis_result = safe_invoke(tactical_analysis_chain, {
        **base_info,
        "material_assessment": position_result,
        "king_safety_assessment": king_safety_result
    })
    if not tactical_analysis_result:
        print("Failed to get tactical analysis. Skipping puzzle.")
        continue

    # Strategic Analysis
    print("Analyzing Strategic Analysis")
    strategic_analysis_prompt = ChatPromptTemplate.from_template(STRATEGIC_ANALYSIS_PROMPT)
    strategic_analysis_chain = strategic_analysis_prompt | llm
    strategic_analysis_result = safe_invoke(strategic_analysis_chain, {
        **base_info,
        "material_assessment": position_result,
        "king_safety_assessment": king_safety_result,
        "tactical_assessment": tactical_analysis_result
    })
    if not strategic_analysis_result:
        print("Failed to get strategic analysis. Skipping puzzle.")
        continue

    # Best Move Analysis
    print("Analyzing Best Move")
    best_move_prompt = ChatPromptTemplate.from_template(BEST_MOVE_PROMPT)
    best_move_chain = best_move_prompt | llm
    best_move_result = safe_invoke(best_move_chain, {
        **base_info,
        "material_assessment": position_result,
        "king_safety_assessment": king_safety_result,
        "tactical_assessment": tactical_analysis_result,
        "strategic_assessment": strategic_analysis_result
    })
    if not best_move_result:
        print("Failed to get best move analysis. Skipping puzzle.")
        continue

    # Combine all results
    # final_result = {
    #     **base_info,
    #     "material_assessment": position_result,
    #     "king_safety_assessment": king_safety_result,
    #     "tactical_assessment": tactical_analysis_result,
    #     "strategic_assessment": strategic_analysis_result,
    #     "best_move_analysis": best_move_result
    # }
    # print("\nFinal Result:", final_result)
    regex = r"UCI Notation:\S*\s+(\w{4,5})"
    match: re.Match = re.search(regex, best_move_result)

    if not match or match.group(1) != puzzle["best_move"]:
        print("No match found")
        continue

    print(f"Predicted move matches correct move: {match.group(1)}")
    dataset.loc[len(dataset)] = {
        "input": INPUT_PROMPT.format(
            board=base_info["board"],
            side_to_move=base_info["side_to_move"],
            castling_rights=base_info["castling_rights"],
            en_passant_target_square=base_info["en_passant_target_square"],
            best_move=match.group(1),
        ),
        "output": OUTPUT_PROMPT.format(
            material_assessment=position_result,
            king_safety_assessment=king_safety_result,
            tactical_assessment=tactical_analysis_result,
            strategic_assessment=strategic_analysis_result,
            best_move_analysis=best_move_result,
        )
    }
    dataset.to_csv(BASE_DIR + OUTPUT_DIR, index=False)

