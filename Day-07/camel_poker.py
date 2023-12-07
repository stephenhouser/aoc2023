#!/usr/bin/env python
"""
Advent of Code 2023 - Day 7: Camel Cards
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse

def score_hand(hand, joker=None):
    """Return a score for the poker hand"""

    # Translate to hex then use that as a number to give unique score
    poker_in ="123456789TJQKA"
    hex_out ="123456789ABCDE"
    if joker:
        idx = poker_in.index(joker)
        hex_out = hex_out[:idx] + '0' + hex_out[idx+1:]

    translated = hand.translate(str.maketrans(poker_in, hex_out))
    return int(translated, 16)

def rank_hand(hand):
    """Return int represeting poker hand ranking
        5-kind = 7, 4-kind = 6, ... high-card = 1
    """
    card_counts = sorted(
        map(lambda x: (hand.count(x), x), set(hand)),
        reverse=True)

    rank = 1                        # assume high card
    match card_counts:
        case [(5, _), *_]:          # 5 kind
            rank = 7
        case [(4, _), *_]:          # 4 kind
            rank = 6
        case [(3, _), (2, _), *_]:  # full house
            rank = 5
        case [(3, _), *_]:          # 3 kind
            rank = 4
        case [(2, _), (2, _), *_]:  # 2 pair
            rank = 3
        case [(2, _), *_]:         # 2 kind
            rank = 2

    return rank

def joker_score(hand, joker='J'):
    """Return hand score with joker counting as 0 points
    """
    return score_hand(hand, joker)

def expand_jokers(hand, joker='J'):
    """Return list of all possible hands with joker substitution

       Example: 'AJQ12' -> ['A2Q12', 'A1Q12', 'AQQ12', 'AAQ12']
    """
    if joker not in hand:
        return [hand]

    replacements = set(hand.replace(joker, ''))
    hands = []
    for card in hand:
        if card == joker:
            for replacement in replacements:
                hands.extend(expand_jokers(hand.replace(joker, replacement, 1)))

    return hands

def joker_rank(hand, joker='J'):
    """Return best ranking of a poker hand with jokers
    """
    # if only jokers, treat as 5-kind Aces
    if len(set(hand)) == 1 and joker in hand:
        return rank_hand("AAAAA")

    # otherwise, find the max of all the possibilities
    return max(map(rank_hand, expand_jokers(hand)))

class PokerHand:
    """Represents a Camel Poker hand"""

    # translation to use for scoring.
    # replace any char with 0 to treat it as a Joker/Wildcard
    translation = "123456789ABCDE"

    def __init__(self, text):
        """Initialize hand from line of text"""
        self.bid = 0
        self.hand = None
        self._parse_hand(text)

    def _parse_hand(self, text):
        """Parse text description of camel poker hand"""
        match = re.match(r'([AKQJT1-9]{5})\s+(\d+)', text)
        self.bid = int(match.group(2))
        self.hand = match.group(1)

    def __repr__(self):
        """Return REPL representation of the thing"""
        return str(self)

    def __str__(self):
        """Return string representation of the thing"""
        return f'PokerHand: {self.hand} {self.bid}'

def load_file(filename: str):
    """Load lines from file into a list of Camel Poker hands
        
       filename: the file to read game descriptions from.
       returns: a list of PokerHands
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file_handle:
            return list(map(PokerHand, file_handle.readlines()))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def pretty_print(hands):
    """Print my Camel Poker hands in a readable fashion"""
    for hand in hands:
        print(hand)

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        hands = load_file(filename)

        #
        # Part One
        #
        n_hands = len(hands)
        print(f'\tNumber of hands: {n_hands}')

        # sort by hand rank and then score within rank
        sorted_hands = sorted(hands, key=lambda x: (rank_hand(x.hand), score_hand(x.hand)))
        #pretty_print(sorted_hands)

        # each hand is worth (its position in the list) * (the listed bid)
        # compute the sum of all these values for the answer
        bid_sum = sum(map(lambda h, i: h.bid*i, sorted_hands, range(1, n_hands+1)))
        print(f'\tSum of ranked hand bids (regular): {bid_sum}')

        #
        # Part Two
        #
        sorted_hands = sorted(hands, key=lambda x: (joker_rank(x.hand), joker_score(x.hand)))
        #pretty_print(sorted_hands)

        bid_sum = sum(map(lambda h, i: h.bid*i, sorted_hands, range(1, n_hands+1)))
        print(f'\tSum of ranked hand bids (jokers) : {bid_sum}')

        print()

if __name__ == '__main__':
    main()
