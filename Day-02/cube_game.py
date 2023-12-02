#!/usr/bin/env python
"""
Advent of Code 2023 - Day 2: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
from functools import reduce


#
# Part 1
# - Parse the game file:
#    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
#    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
#     Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# - Determine which games are valid/possible if there were only
#    12 red, 13 blue, and 14 green cubes available.
# - Compute the sum of those game ids
#
def parse_color(text: str, color: str) -> int:
    """Return the number of cubes of the given color in the trial.

       trial_text: the text of an individual trial, e.g. "2 red, 3 blue"
       color: the color to return, e.g. "red"
       returns: the number of cubes of that color, e,g. 2
    """
    color_match = re.search(r'(\d+)\s+' + color, text)
    return int(color_match.group(1)) if color_match else 0

def parse_game_set(trail_text: str) -> tuple[int]:
    """Return the number of cubes of each color in the trial_text

       trial_text: the text of an individual trial, e.g. "2 red, 3 blue"
       retrurs: (red, green, blue)
    """
    color_names = ('red', 'green', 'blue')

    # TODO: Without list expansion something breaks later on...
    return list(map(lambda color: parse_color(trail_text, color), color_names))

def parse_game_sets(trials_text:str) -> list[tuple[int]]:
    """Return a list of tuples representing the trials for the given game.

       trials_text represents the semicolon separated list of trials.
       returns: [(3, 6, 9), (r, g, b), ...]
    """
    # TODO: Without list expansion something breaks later on...
    return list(map(parse_game_set, trials_text.split(';')))

def parse_game(game_text:str) -> tuple[int, list[tuple[int]]]:
    """Return the game_id and set of trials for the given game.

        game_text textual description of a game, e.g. "Game <id>: trial; ..."
        returns: (1, [(3, 6, 9), (r, g, b), ...])
    """
    game_match = re.match(r'^Game (\d+):(.*)$', game_text)
    game_id = int(game_match.group(1))
    game_sets = parse_game_sets(game_match.group(2))
    return (game_id, game_sets)

def load_games(filename: str):
    """Return the games contained in the give file as a dictionary
       of games (key = game_id) which contain a list of trials (tuples).
        
       filename: the file to read game descriptions from.
       returns: { 1:[(1, 2, 3), (5, 14, 12),...], 2:[...] }
    """
    games = {}
    try:
        with open(filename, 'r', encoding='utf-8') as gf:
            for line in gf.readlines():
                (game, sets) = parse_game(line)
                games[game] = sets

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return games

def valid_trial(trial: tuple[int], max_rgb: tuple[int]) -> bool:
    """Return True if the trial could have resulted in a game with max_rgb
        cubes. False otherwise.

        trial:  tuple (red, green, blue)
        max_rgb: tuple (red, green, blue)
    """
    return all(map(lambda a, b: a <= b, trial, max_rgb))

def valid_trials(trials: list[tuple], max_rgb: tuple[int]) -> bool:
    """Return True if the trials could have resulted in a game with max_rgb
        cubes. False otherwise

        trials: list of trials 
        max_rgb is a tuple (max red, max gree, max blue)
        returns: True of all trials were valid, False otherwise
    """
    # Partial lambda valid_trial(x, max_rgb)
    return all(map(lambda x: valid_trial(x, max_rgb), trials))

def valid_games(games: dict[int, list[tuple[int]]],
                max_rgb: tuple[int]) -> dict[int, list[tuple[int]]]:
    """Return a list of all the valid games

        A valid game is one which does not have any trials that resulted in
        more cubes than max_rgb cubes.
        max_rgb is a tuple (max red, max gree, max blue)
    """
    return {g: s for g, s in games.items() if valid_trials(s, max_rgb)}

#
# Part 2
# - Find fewest number of cubes needed for each game based on trials
# - Compute the power of each game from the min number of cubes needed
#       power = red cubes * green * blue
# - Sum all the powers
#
def max_sequence(a: tuple[int], b: tuple[int]) -> tuple[int]:
    """Returns a tuple representing the maximum value for each
       item in the sequences a and b.

       This is the minimum number of cubes needed for the given trials.

       Ex: Givem a=(1, 3, 4), b=(2, 1, 5) returns (2, 3, 5)
    """
    return (max(x, y) for x, y in zip(a, b))

def cubes_for_game(trials:list[tuple[int]]) -> tuple[int]:
    """Return the number of cubes needed for a game based on the number
       reported in each of that games trials.

       trials: the trials conducted for the game
    """
    return reduce(max_sequence, trials, trials[0])

def game_power(trials):
    """Return the power of the game.

       Power is defined as the product of the minimum cubes needed for the game.
       e.g. (1, 2, 3) -> 1 * 2 * 3 = 6
            (4, 2, 6) -> 4 * 2 * 6 = 48
    """
    return reduce(lambda x, y: x * y, cubes_for_game(trials), 1)

def game_powers(games: dict[int, list[tuple[int]]]) -> list[int]:
    """Return a list of the powers for the given games
    """
    return map(game_power, games.values())


sample_games = load_games('input.txt')
possible_games = valid_games(sample_games, (12, 13, 14))
possible_games_sum = sum(possible_games.keys())
print(f'The sum of the possible games ids is: {possible_games_sum}')

powers = game_powers(sample_games)
print(f'The sum of the game powers is: {sum(powers)}')
