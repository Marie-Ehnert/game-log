import os
from datetime import date
from io import TextIOWrapper
from pathlib import Path

PATH = Path(__file__).parent.parent.joinpath("logs")

def start_log():
    if not PATH.is_dir():
        PATH.mkdir(parents=True, exist_ok=True)
    print("Welcome to game-log! \n")
    print("Type:"
          "\n> [new] to create a new log"
          "\n> [update] to append to an existing log"
          "\n> [list all] to list all existing logs"
          "\n> [read] to print the log content to the console"
          "\n> [delete] to delete a game log"
          "\n")
    command = input()
    if command == "new":
        create_game_log()
    elif command == "update":
        update_game_log()
    elif command == "list all":
        list_all()
    elif command == "read":
        print("Enter name of log file:\n")
        log_name = input()
        read_log(log_name)
    elif command == "delete":
        print("delete")

def create_game_log():
    print("Enter new game name: ")
    new_game = input()
    try:
        game_file = open(f"{PATH}/{new_game.replace(" ", "_")}_log.txt", "x")
        query_player_input(game_file)
    except FileExistsError:
        print("This game is already logged, you can only update it!")


def query_player_input(game_file: TextIOWrapper):
    game_file.write(f"LOG {date.today()}:\n")
    print("What have you done this session?: ")
    history = input()
    game_file.write(history + os.linesep)
    print("What are the next steps and goals?: ")
    future = input()
    game_file.write(future + os.linesep)
    game_file.write("\n")


def update_game_log():
    print("What game shall be logged?: ")
    game = input()
    dir_list = os.listdir(PATH)
    game_found = False
    game_log_path = f"{PATH}/{game.replace(" ", "_")}_log.txt"
    game_log_file_name = f"{game.replace(" ", "_")}_log.txt"
    for file in dir_list:
        if game_log_file_name == file:
            game_found = True
            continue
    if game_found:
        with open(game_log_path, "a") as game_file:
            query_player_input(game_file)
    else: print(f"No game file found with the name {game_log_path}, did you mean to create one? If yes please restart this program and use the \"new\" command")


def list_all():
    dir_list = os.listdir(PATH)
    for item in dir_list:
        print("* " + item + "\n")

def read_log(log_name: str):
    game_log_path = f"{PATH}/{log_name}"
    file = open(game_log_path, "r")
    content = file.read()
    # here no line seperator at the end because each log leaves a newline anyway
    print("\n" + "-->\n" + content + "<--")
    file.close()

