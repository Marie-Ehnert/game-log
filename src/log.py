import os
from datetime import date
from io import TextIOWrapper
from pathlib import Path


PATH = Path(__file__).parent.parent.joinpath("logs")
print(PATH)

def start_log():
    print("Welcome to game-log! \n")
    print("Type \"new\" to create a new log or type \"update\" to append to an existing log")
    command = input()
    if command == "new":
        create_game_log()
    elif command == "update":
        update_game_log()


def create_game_log():
    print("Enter new game name: ")
    new_game = input()
    try:
        game_file = open(f"{PATH}/{new_game.replace(" ", "_")}_log.txt", "x")
        print(game_file)
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
    game_file.write(">< >< >< >< >< >< >< >< >< >< >< >< >< >< >< >< >< >< >< ><")


def update_game_log():
    print("What game shall be logged?: ")
    game = input()
    dir_list = os.listdir(PATH)
    for file in dir_list:
        if f"PATH{game.replace(" ", "_")}_log.txt" == file:
            continue
    with open(f"{PATH}{game.replace(" ", "_")}_log.txt", "a") as file:
        file.write("test")



