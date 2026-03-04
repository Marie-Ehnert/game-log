import json
import os
from datetime import date
from io import TextIOWrapper
from math import floor
from pathlib import Path
from typing import List, Dict

import src.api_requests as req
from src.constants import STEAM_GAME_DATA_PATH, API_KEY, STEAM_ID, GAMES_DATA_JSON_PATH


def is_dir_or_else_create(path: Path):
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)

def get_steam_data():
    try:
        games = req.get_owned_games(API_KEY, STEAM_ID)
    except RuntimeError() as e:
        print(e)
        return
    is_dir_or_else_create(STEAM_GAME_DATA_PATH)
    with open(GAMES_DATA_JSON_PATH, "w") as file:
        json.dump(games, file, indent=4)


def query_player_input(game_file: TextIOWrapper, playtime: None | float):
    game_file.write(f"LOG {date.today()}:\n")
    print("What have you done this session?: ")
    history = input()
    game_file.write(history + os.linesep)
    print("What are the next steps and goals?: ")
    future = input()
    game_file.write(future + os.linesep)
    if playtime:
        game_file.write("Total hours played: " + str(floor(playtime)) + os.linesep)
    game_file.write("\n")

def get_total_hours_played(new_game: str, playtime: float | None) -> float | None:
    get_steam_data()
    games_data: List[Dict] = []
    with open(GAMES_DATA_JSON_PATH, "r") as json_file:
        games_data = json.load(json_file)
    for game in games_data:
        if game.get("name") == new_game:
            playtime_in_minutes = game.get("playtime_forever")
            playtime = playtime_in_minutes / 60
            return playtime
    return None

