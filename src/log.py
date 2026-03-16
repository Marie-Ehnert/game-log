import os
import click
from src.constants import LOG_PATH, USE_STEAM_STATS
from src.utils import query_player_input, get_total_hours_played, is_dir_or_else_create

@click.command()
def start_log():
    is_dir_or_else_create(LOG_PATH)
    print("Welcome to game-log! \n")
    print("To activate steam playtime data tracking, fill out the config.toml and make sure to turn \"use_steam_stats\" to True")
    show_commands()
    command = input()
    match command:
        case "new":
            create_game_log()
        case "update":
            update_game_log()
        case "list all":
            list_all()
        case "read":
            print("Enter name of log file: ")
            log_name = input()
            read_log(log_name)
        case "delete":
            print("Enter name of log file: ")
            log_name = input()
            delete_log(log_name)
        case _:
            print("Unknown command please retry!")

def show_commands():
    print("Type:"
          "\n> [new] to create a new log"
          "\n> [update] to append to an existing log"
          "\n> [list all] to list all existing logs"
          "\n> [read] to print the log content to the console"
          "\n> [delete] to delete a game log"
          "\n")

def create_game_log():
    print("Enter new game name: ")
    new_game = input()
    playtime = None
    if USE_STEAM_STATS:
        playtime = get_total_hours_played(new_game)

    try:
        game_file = f"{new_game.replace(' ', '_')}_log.txt"
        game_file_path = open(f"{LOG_PATH}/{game_file}", "x")
        query_player_input(game_file_path, playtime)
        print(f"\n 📝  {game_file} has been created!")
    except FileExistsError:
        print("This game is already logged, you can only update it!")

def update_game_log():
    print("What game shall be logged?: ")
    game = input()
    dir_list = os.listdir(LOG_PATH)
    game_found = False
    game_log_file_name = f"{game.replace(' ', '_')}_log.txt"
    game_log_path = f"{LOG_PATH}/{game_log_file_name}"
    for file in dir_list:
        if game_log_file_name == file:
            game_found = True
            continue
    if game_found:
        playtime = None
        if USE_STEAM_STATS:
            playtime = get_total_hours_played(game)
        with open(game_log_path, "a") as game_file:
            query_player_input(game_file, playtime)
        print(f"\n ✅  {game_log_file_name} has been updated!")
    else: print(f"No game file found with the name {game_log_path}, did you mean to create one? If yes please restart this program and use the \"new\" command")

def list_all():
    dir_list = os.listdir(LOG_PATH)
    for item in dir_list:
        print("> " + item)

def read_log(log_name: str):
    game_log_path = f"{LOG_PATH}/{log_name}"
    file = open(game_log_path, "r")
    content = file.read()
    # here no line seperator at the end because each log leaves a newline anyway
    print("\n" + "-->\n" + content + "<--")
    file.close()

def delete_log(log_name: str):
    game_log_path = f"{LOG_PATH}/{log_name}"
    if os.path.exists(game_log_path):
        os.remove(game_log_path)
        print(f"🗑️  {log_name} removed")
    else:
        print("No File found!")

if __name__ == "__main__":
    start_log()