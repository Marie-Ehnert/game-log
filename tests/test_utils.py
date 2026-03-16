import json
import os
from pathlib import Path
from game_log.constants import GAMES_DATA_JSON_PATH
from game_log.utils import is_dir_or_else_create, get_steam_data, query_player_input, get_total_hours_played
from game_log.constants import STEAM_GAME_DATA_PATH
import unittest
from unittest.mock import patch

EXAMPLE_DIR_PATH = Path(__file__).parent.joinpath("example")

class TestUtilsFunctions(unittest.TestCase):

    def test_is_dir_or_else_create(self):
        self.assertFalse(EXAMPLE_DIR_PATH.exists())
        is_dir_or_else_create(EXAMPLE_DIR_PATH)
        self.assertTrue(EXAMPLE_DIR_PATH.is_dir())
        EXAMPLE_DIR_PATH.rmdir()

    @patch("game_log.utils.req")
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
            result = json   .load(f)
            self.assertListEqual(mock_steam_api_response, result)
        if os.path.exists(GAMES_DATA_JSON_PATH):
            os.remove(GAMES_DATA_JSON_PATH)

    def test_query_player_input_writes_with_playtime(self):
        """Check that query_player_input writes prompts and optional playtime line."""
        from io import StringIO
        fake_file = StringIO()
        # Use unittest.mock.patch to simulate inputs
        from unittest.mock import patch
        with patch('builtins.input', side_effect=['Did something', 'Next steps']):
            query_player_input(fake_file, playtime=3.7)
        output = fake_file.getvalue().splitlines()
        self.assertTrue(output[0].startswith('LOG '))
        self.assertIn('Did something', output)
        self.assertIn('Next steps', output)
        self.assertIn('Total hours played: 3', output)

    def test_query_player_input_without_playtime(self):
        """When playtime is None, no total hours line should be written."""
        from io import StringIO
        from unittest.mock import patch
        fake_file = StringIO()
        with patch('builtins.input', side_effect=['A', 'B']):
            query_player_input(fake_file, playtime=None)
        output = fake_file.getvalue().splitlines()
        self.assertTrue(output[0].startswith('LOG '))
        self.assertIn('A', output)
        self.assertIn('B', output)
        # Ensure no line starts with Total hours
        self.assertFalse(any(line.startswith('Total hours played') for line in output))

    def test_get_total_hours_played_returns_correct(self):
        """Verify correct conversion from minutes to hours when game exists."""
        from unittest.mock import patch
        # Prepare mock JSON data
        sample = [{"name": "Game X", "appid": 1, "playtime_forever": 120}]
        # Ensure directory exists
        STEAM_GAME_DATA_PATH.mkdir(parents=True, exist_ok=True)
        with open(GAMES_DATA_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(sample, f)
        # Patch get_steam_data to avoid overwriting file
        with patch('game_log.utils.get_steam_data'):
            hours = get_total_hours_played('Game X')
        self.assertAlmostEqual(hours, 2.0)
        # Cleanup
        if GAMES_DATA_JSON_PATH.exists():
            GAMES_DATA_JSON_PATH.unlink()

    def test_get_total_hours_played_none_when_missing(self):
        """Return None when the game is not found in JSON data."""
        from unittest.mock import patch
        sample = [{"name": "Other", "appid": 2, "playtime_forever": 60}]
        STEAM_GAME_DATA_PATH.mkdir(parents=True, exist_ok=True)
        with open(GAMES_DATA_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(sample, f)
        with patch('game_log.utils.get_steam_data'):
            result = get_total_hours_played('Missing')
        self.assertIsNone(result)
        if GAMES_DATA_JSON_PATH.exists():
            GAMES_DATA_JSON_PATH.unlink()

if __name__ == '__main__':
    unittest.main()