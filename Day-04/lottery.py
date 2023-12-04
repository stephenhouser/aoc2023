#!/usr/bin/env python
"""
Advent of Code 2023 - Day _: Cube Conundrum
Stephen Houser <stephenhouser@gmail.com>
"""

import re
import argparse

class Card:
    """Class to represent a card in the elf lottery"""

    def __init__(self, card_line):
        self.card_id = None
        self.winning = []
        self.picks = []
        self.score = None
        self.matches = 0
        self.copies = 1
        self._parse_card_line(card_line)

    def _compute_score(self):
        # cache the score and matches computation
        if not self.score or not self.matches:
            card_winners = set(self.winning) & set(self.picks)
            self.score = int(pow(2, len(card_winners)-1))
            self.matches = len(card_winners)

    def get_matches(self):
        """Return the number of picks that match winning numbers."""
        self._compute_score()
        return self.matches

    def get_score(self):
        """Return the score for this card."""
        self._compute_score()
        return self.score

    def add_copies(self, copies):
        """Increase the number of copies of this card"""
        self.copies += copies

    def get_copies(self):
        """Return the number of copies of this card."""
        return self.copies

    def _parse_card_line(self, card_line):
        """Parse text description of card"""
        card_match = re.match(r'Card\s+(\d+):([\d ]+)\|([\d ]+)', card_line)
        self.card_id = int(card_match.group(1))
        self.winning = list(map(int, re.findall(r'\d+', card_match.group(2))))
        self.picks = list(map(int, re.findall(r'\d+', card_match.group(3))))

    def __repr__(self):
        """Return REPL representation of the card"""
        return str(self)

    def __str__(self):
        """Return string representation of the card."""
        winn = ' '.join(map(str, self.winning))
        pick = ' '.join(map(str, self.picks))
        return f'Card {self.card_id}: {winn} | {pick} | score={self.score}, copies={self.copies}'

def load_cards(filename: str) -> list[str]:
    """Load ...
        
       filename: the file to read game descriptions from.
       returns: a list of strings, one string for each row in the map
    """
    try:
        with open(filename, 'r', encoding='utf-8') as map_file:
            return list(map(Card, map_file.readlines()))

    except FileNotFoundError:
        print(f'ERROR: file {filename} not found.')

    return []

def duplicate_cards(cards):
    """Updates cards to reflect winning new cards.
    """
    for card_n, card in enumerate(cards):
        for copy_n in range(card.get_matches()):
            card_copy = card_n + 1 + copy_n
            if card_copy < len(cards):
                cards[card_copy].add_copies(card.get_copies())

def main():
    """Main Routine, does all the work"""
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', default='input.txt', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        print(filename)
        cards = load_cards(filename)

        total_score = sum(map(Card.get_score, cards))
        print(f'\tSum of scores: {total_score}')

        duplicate_cards(cards)
        total_cards = sum(map(Card.get_copies, cards))
        print(f'\tTotal number of cards: {total_cards}')

        print()

if __name__ == '__main__':
    main()
