import requests
import json
from typing import List, Dict

URL_USER_STATS_OWNED_GAMES = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"

def get_owned_games(api_key: str, steam_id: str) -> List[Dict] | str:
    input_data = {"steamid": steam_id, "include_appinfo": True, "include_played_free_games": True}
    params = {
        "key": api_key,
        "input_json": json.dumps(input_data)
    }

    try:
        response = requests.get(URL_USER_STATS_OWNED_GAMES, params=params)
        response.raise_for_status()
        data = response.json()
        games_owned: List[Dict] = data["response"]["games"]
        if not games_owned or len(games_owned) == 0:
            raise SteamGamesError("No games found or profile is private.")
        concise_game_infos = [
            {
                "name": game["name"],
                "appid": game["appid"],
                "playtime_forever": game["playtime_forever"]
            }
            for game in games_owned
        ]
        return concise_game_infos
    except requests.exceptions.HTTPError and SteamGamesError as e:
        raise RuntimeError(e)

class SteamGamesError(Exception):
    pass

