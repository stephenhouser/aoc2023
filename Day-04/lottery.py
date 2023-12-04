#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
from itertools import chain
from functools import reduce

def parse_card(card_line):
    """Returns a card (card, (winning numbers), (your numbers), multiplier)

    """
    #Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    card_match = re.match(r'Card\s+(\d+):([\d ]+)\|([\d ]+)', card_line)
    card_id = int(card_match.group(1))
    winning_ns = list(map(int, re.findall(r'\d+', card_match.group(2))))
    card_ns = list(map(int, re.findall(r'\d+', card_match.group(3))))
    return [card_id, winning_ns, card_ns, 1]

def load_cards(filename: str) -> list[str]:
    """Load ...
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as map_file:
            return list(map(parse_card, map_file.readlines()))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def score_card_1(card):
    """Return the score for card"""
    card_winners = set(card[1]) & set(card[2])
    # score is 2^n-1
    return int(pow(2, len(card_winners)-1))

def score_cards_1(cards):
    """Return a list with all the scored cards"""
    return list(map(score_card_1, cards))

def score_card_2(card):
    return len(set(card[1]) & set(card[2]))
               
def score_cards_2(cards):
    n_cards = 0
    for card_n, card in enumerate(cards):
        (_, win_ns, card_ns, copies) = card
        n_cards += copies

        match_count = len(set(win_ns) & set(card_ns))
        for _ in range(copies):
            for copy_n in range(card_n, card_n + match_count + 1):
                if copy_n < len(cards):
                    cards[copy_n][3] += 1

    return n_cards

cards = load_cards('input.txt')
#cards = load_cards('input.txt')
#card_values = score_cards_1(cards)
#print(sum(card_values))

card_values = score_cards_2(cards)
print(card_values)
