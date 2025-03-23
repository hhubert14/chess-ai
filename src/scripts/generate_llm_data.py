import os

from dotenv import load_dotenv
import yaml
# from openai import OpenAI
import pandas as pd
from langchain_deepseek import ChatDeepSeek
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils import parse_fen

load_dotenv()

with open(os.getenv("CONFIG_PATH")) as file:
    config = yaml.safe_load(file)

BASE_DIR = config["BASE_DIR"]
INPUT_DIR = "src\data\datasets\puzzles\lichess_puzzles.csv"

from prompts import (
    SYSTEM_PROMPT,
    POSITION_ASSESSMENT_PROMPT,
    KING_SAFETY_PROMPT,
    TACTICAL_ANALYSIS_PROMPT,
    STRATEGIC_ANALYSIS_PROMPT,
    BEST_MOVE_PROMPT,
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

puzzles = pd.read_csv(BASE_DIR + INPUT_DIR)

for index, puzzle in puzzles.iterrows():
    fen_info = parse_fen(puzzle["FEN"])
    base_info = {
        "board": fen_info.board,
        "side_to_move": fen_info.player_to_move,
        "castling_rights": fen_info.castling_rights,
        "en_passant_target_square": fen_info.en_passant_target,
    }
    # board = fen_info.board
    # side_to_move = fen_info.player_to_move
    # castling_rights = fen_info.castling_rights
    # en_passant_target_square = fen_info.en_passant_target

    # Position Assessment
    position_assessment_prompt = ChatPromptTemplate(
        [
            ("system", SYSTEM_PROMPT),
            ("human", POSITION_ASSESSMENT_PROMPT),
        ]
    )
    position_chain = position_assessment_prompt | llm
    position_result = position_chain.invoke(base_info)
    print("position_result: ", position_result.content)

    # King Safety Assessment
    king_safety_prompt = ChatPromptTemplate.from_template(KING_SAFETY_PROMPT)
    king_safety_chain = king_safety_prompt | llm
    king_safety_result = king_safety_chain.invoke({
        **base_info,
        "material_assessment": position_result.content
    })
    print("king_safety_result: ", king_safety_result.content)

    # Tactical Analysis
    tactical_analysis_prompt = ChatPromptTemplate.from_template(TACTICAL_ANALYSIS_PROMPT)
    tactical_analysis_chain = tactical_analysis_prompt | llm
    tactical_analysis_result = tactical_analysis_chain.invoke({
        **base_info,
        "material_assessment": position_result.content,
        "king_safety_assessment": king_safety_result.content
    })
    print("tactical_analysis_result: ", tactical_analysis_result.content)

    # Strategic Analysis
    strategic_analysis_prompt = ChatPromptTemplate.from_template(STRATEGIC_ANALYSIS_PROMPT)
    strategic_analysis_chain = strategic_analysis_prompt | llm
    strategic_analysis_result = strategic_analysis_chain.invoke({
        **base_info,
        "material_assessment": position_result.content,
        "king_safety_assessment": king_safety_result.content,
        "tactical_assessment": tactical_analysis_result.content
    })
    print("strategic_analysis_result: ", strategic_analysis_result.content)

    # Best Move Analysis
    best_move_prompt = ChatPromptTemplate.from_template(BEST_MOVE_PROMPT)
    best_move_chain = best_move_prompt | llm
    best_move_result = best_move_chain.invoke({
        **base_info,
        "material_assessment": position_result.content,
        "king_safety_assessment": king_safety_result.content,
        "tactical_assessment": tactical_analysis_result.content,
        "strategic_assessment": strategic_analysis_result.content
    })
    print("best_move_result: ", best_move_result.content)

    # Combine all results
    final_result = {
        **base_info,
        "material_assessment": position_result.content,
        "king_safety_assessment": king_safety_result.content,
        "tactical_assessment": tactical_analysis_result.content,
        "strategic_assessment": strategic_analysis_result.content,
        "best_move_analysis": best_move_result.content
    }
    print("\nFinal Result:", final_result)
