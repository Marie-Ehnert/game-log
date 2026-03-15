import io
import unittest
from unittest.mock import patch
from datetime import date
from src import log as log_mod
from src.constants import LOG_PATH

from src.log import show_commands, create_game_log
from contextlib import redirect_stdout

class TestLogFunctions(unittest.TestCase):

    def test_show_commands(self):
        f = io.StringIO()
        expected = (
            "Type:"
            "\n> [new] to create a new log"
            "\n> [update] to append to an existing log"
            "\n> [list all] to list all existing logs"
            "\n> [read] to print the log content to the console"
            "\n> [delete] to delete a game log"
            "\n\n"
        )
        with redirect_stdout(f):
            show_commands()
        output = f.getvalue()
        self.assertEqual(output, expected)

    def setUp(self):
        # Ensure LOG_PATH exists but do not delete existing logs
        LOG_PATH.mkdir(parents=True, exist_ok=True)
        self._created_files = []
        # Disable Steam stats to avoid external calls
        self._original_use_steam = log_mod.USE_STEAM_STATS
        log_mod.USE_STEAM_STATS = False

    def tearDown(self):
        # Restore original flag
        log_mod.USE_STEAM_STATS = self._original_use_steam
        # Remove only files created during the tests
        for p in self._created_files:
            if p.exists():
                p.unlink()

    def test_create_game_log_success(self):
        game_name = "TestGame"
        with patch("builtins.input", return_value=game_name):
            with patch("builtins.print") as mock_print:
                log_mod.create_game_log()
        path = LOG_PATH / f"{game_name}_log.txt"
        self._created_files.append(path)
        self.assertTrue(path.exists())
        with path.open() as f:
            first = f.readline().strip()
        self.assertTrue(first.startswith("LOG "))
        mock_print.assert_any_call(f"\n 📝  {game_name}_log.txt has been created!")

    def test_create_game_log_already_exists(self):
        game_name = "ExistingGame"
        path = LOG_PATH / f"{game_name}_log.txt"
        path.touch()
        with patch("builtins.input", return_value=game_name):
            with patch("builtins.print") as mock_print:
                log_mod.create_game_log()
        mock_print.assert_any_call("This game is already logged, you can only update it!")

    def test_update_game_log_success(self):
        game_name = "UpdateGame"
        path = LOG_PATH / f"{game_name}_log.txt"
        path.write_text(f"LOG {date.today()}:\nInitial entry\n\n")
        self._created_files.append(path)
        inputs = iter([game_name, "Did something", "Plan next"])
        with patch("builtins.input", side_effect=lambda: next(inputs)):
            with patch("builtins.print"):
                log_mod.update_game_log()
        content = path.read_text()
        self.assertIn("Did something", content)
        self.assertIn("Plan next", content)

    def test_list_all(self):
        a = LOG_PATH / "a_test.txt"
        b = LOG_PATH / "b_test.txt"
        a.touch(); b.touch()
        self._created_files.extend([a, b])
        with patch("builtins.print") as mock_print:
            log_mod.list_all()
        printed = [call.args[0] for call in mock_print.call_args_list]
        self.assertIn(f"> {a.name}", printed)
        self.assertIn(f"> {b.name}", printed)

    def test_read_log(self):
        filename = "readme_test.txt"
        path = LOG_PATH / filename
        path.write_text("Hello World")
        self._created_files.append(path)
        with patch("builtins.print") as mock_print:
            log_mod.read_log(filename)
        printed = [call.args[0] for call in mock_print.call_args_list]
        self.assertTrue(any("Hello World" in p for p in printed))
        self.assertTrue(any("-->" in p for p in printed))

    def test_delete_log(self):
        filename = "todelete_test.txt"
        path = LOG_PATH / filename
        path.touch()
        with patch("builtins.print") as mock_print:
            log_mod.delete_log(filename)
        self.assertFalse(path.exists())
        mock_print.assert_any_call(f"🗑️  {filename} removed")

