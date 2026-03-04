import json
import os
from pathlib import Path
from src.constants import GAMES_DATA_JSON_PATH
from src.utils import is_dir_or_else_create, get_steam_data
import unittest
from unittest.mock import patch

EXAMPLE_DIR_PATH = Path(__file__).parent.joinpath("example")

class TestUtilsFunctions(unittest.TestCase):

    def test_is_dir_or_else_create(self):
        self.assertFalse(EXAMPLE_DIR_PATH.exists())
        is_dir_or_else_create(EXAMPLE_DIR_PATH)
        self.assertTrue(EXAMPLE_DIR_PATH.is_dir())
        EXAMPLE_DIR_PATH.rmdir()

    @patch("src.utils.req")
    def test_get_steam_data_succeeds(self, mock_req):
        mock_steam_api_response = [
            {
                "name": "Battlerite",
                "appid": 504370,
                "playtime_forever": 328
            },
            {
                "name": "For The King",
                "appid": 527230,
                "playtime_forever": 2309
            },
            {
                "name": "TUNIC",
                "appid": 553420,
                "playtime_forever": 1753
            }
        ]
        mock_req.get_owned_games.return_value = mock_steam_api_response
        get_steam_data()
        mock_req.get_owned_games.assert_called_once()
        self.assertTrue(os.path.exists(GAMES_DATA_JSON_PATH))
        with open(GAMES_DATA_JSON_PATH, "r") as f:
            result = json.load(f)
            self.assertListEqual(mock_steam_api_response, result)
        if os.path.exists(GAMES_DATA_JSON_PATH):
            os.remove(GAMES_DATA_JSON_PATH)

if __name__ == '__main__':
    unittest.main()