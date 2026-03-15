import tomllib
from pathlib import Path

STEAM_GAME_DATA_PATH: Path = Path(__file__).parent.parent.joinpath("steam_game_data")
LOG_PATH: Path = Path(__file__).parent.parent.joinpath("logs")
CONFIG_PATH: Path = Path(__file__).parent.parent.joinpath("config.toml")
GAMES_DATA_JSON_PATH: Path = STEAM_GAME_DATA_PATH.joinpath("games_data.json")

def load_config():
    if not CONFIG_PATH.exists():
        # Return default/mock values if file is missing (for CI in GitHub)
        return {"steam_api_key": "MOCK", "steam_id_64": "0", "use_steam_stats": "False"}

    with open(CONFIG_PATH, 'rb') as f:
        return tomllib.load(f)

config = load_config()

API_KEY = config["steam_api_key"]
STEAM_ID = config["steam_id_64"]
USE_STEAM_STATS = True if config["use_steam_stats"] == "True" else False