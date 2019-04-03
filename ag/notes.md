
# Installation

Solve the import module headache
> $ export PYTHONPATH=$PYTHONPATH:`pwd`

install dependencies
> $ pip install -r requirements.txt

# Testing
launch the tests
> $ pytest



From the main menu, click new game

> New Game
    Choose a starting Region
    Choose a name for your tribe (or random)
    Click start

    > The Region is created with random resources and random terrains/special locations.

    The game start on turn 1, with 10 people, and a list of tasks to accomplish (find food, find clean water, find a shelter).
    The player must first train his tribemen to eat and to build a shelter to rest.
    Turn 1 is daytime, turn 2 is nighttime, etc.
    At the end of each turn, every tribeman will try to eat and drink from available stock (personal or group).
    If he cannot eat/drink, his hunger/thirst score increase.
    Past a certain threshold, he will start losing HP and try to eat/drink whatever is around (dirt, unknown plants, stagnating water etc)

    The game ends when everyone dies.

    That's it. Try to code that.

