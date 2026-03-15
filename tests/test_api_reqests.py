import unittest
from requests.exceptions import HTTPError

from src.api_requests import get_owned_games


class TestApiRequests(unittest.TestCase):

    def test_get_owned_games_without_mock(self):
        with self.assertRaises(HTTPError) as err:
            response: HTTPError = get_owned_games("test_api_key", "test_steam_id")
        expected_msg = "<html><head><title>Unauthorized</title></head><body><h1>Unauthorized</h1>Access is denied. Retrying will not help. Please verify your <pre>key=</pre> parameter.</body></html>"
        self.assertIn(err.exception.response.text, expected_msg)