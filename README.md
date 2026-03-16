## Introduction 🎮
This CLI app is a first approach of mine to make a sort of game progress diary or log book! I always struggle to get back to games I started and have abandoned for a longer period. In that case a sort of diary helps a lot!

This CLI app works with the creation of log text files. Its really simple. When using the proper command you can either create a new log text file or update one. Logs add the date automatically and you get prompted with two defining questions "What have you done this session?" and "What are your goals?". Its also possible to track your playtime of the game if it is featured on the platform Steam. To configure everything to use this API feature please read further :)

## How to set it up
This Tutorial expects that you have the package manager __pip__ installed and preferably initialize a venv for this repo.
1. Clone this repo

2. Create a virtual environment:

    ``` python -m venv .venv && source .venv/bin/activate```

3. Install in editable mode:

    ```pip install -e .```

4. Run the app:

    ```game-log```

## How to make use of Steam API feature?
1. copy example_config.toml and rename the copy to just __config.toml__
2. fill the placeholders like instructed
3. BAM! thats it