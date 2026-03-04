import tomllib
from pathlib import Path

STEAM_GAME_DATA_PATH: Path = Path(__file__).parent.parent.joinpath("steam_game_data")
LOG_PATH: Path = Path(__file__).parent.parent.joinpath("logs")
CONFIG_PATH: Path = Path(__file__).parent.parent.joinpath("config.toml")
GAMES_DATA_JSON_PATH: Path = STEAM_GAME_DATA_PATH.joinpath("games_data.json")

with open(CONFIG_PATH, 'rb') as f:
    config = tomllib.load(f)

API_KEY = config["steam_api_key"]
STEAM_ID = config["steam_id_64"]
USE_STEAM_STATS = True if config["use_steam_stats"] == "True" else False