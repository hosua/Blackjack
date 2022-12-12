import random as r
import os
import sys

class NoStdStreams(object):
    # Source
    # https://codereview.stackexchange.com/questions/25417/is-there-a-better-way-to-make-a-function-silent-on-need
    def __init__(self, stdout=None, stderr=None):
        self.devnull = open(os.devnull, 'w')
        self._stdout = stdout or self.devnull or sys.stdout
        self._stderr = stderr or self.devnull or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush();
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush();
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        self.devnull.close()


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.color = ""
        self.card_dict = {"ranks": {"2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven",
                                    "8": "eight", "9": "nine", "10": "ten", "J": "jack", "Q": "queen", "K": "king",
                                    "A": "ace"},
                          "suits": {"S": ("spades", "♠"), "C": ("clubs", "♣"),
                                    "D": ("diamonds", "♢"), "H": ("hearts", "♡")},
                          "red": ["D", "H"],
                          "black": ["C", "S"]}

    def set_color(self):  # This is only to determine color. It should never be called later.
        if self.suit in self.card_dict["red"]:
            self.color = "red"
        else:
            self.color = "black"

    def get(self, rtn_type="dict"):
        self.set_color()
        d = {"rank": self.rank, "suit": self.suit, "color": self.color}
        if rtn_type == "dict":
            return d
        elif rtn_type == "super short":
            return self.rank + self.card_dict["suits"][self.suit][1]
        elif rtn_type == "fancy":
            return "|" + self.rank + self.card_dict["suits"][self.suit][1] + "|"
        elif rtn_type == "medium":
            return self.rank + " of " + self.card_dict["suits"][self.suit][1]
        elif rtn_type == "long":
            return self.card_dict["ranks"] + " of " + self.card_dict["suits"][self.suit][0]
        return None

    def set(self, suit, rank):
        self.suit = suit
        self.rank = rank


class CardHandler:
    def __init__(self):
        self.card_dict = {"ranks": {"2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven",
                                    "8": "eight", "9": "nine", "10": "ten", "J": "jack", "Q": "queen", "K": "king",
                                    "A": "ace"},
                          "suits": {"S": ("spades", "♠"), "C": ("clubs", "♣"),
                                    "D": ("diamonds", "♢"), "H": ("hearts", "♡")},
                          "red": ["D", "H"],
                          "black": ["C", "S"]}
        pass

    def make_deck(self, show=True):
        cards = []
        while len(cards) != 52:
            for rank in list(self.card_dict["ranks"]): 
                for suit in list(self.card_dict["suits"]):
                    cards.append(Card(rank, suit));
        self.shuffle_cards(cards)
        return cards

    @staticmethod
    def shuffle_cards(deck):
        print("Shuffling the deck...")
        r.shuffle(deck)

    @staticmethod
    def show_cards(cards, num=0):    # show any list of cards
        rtn_str = ""
        if num == 0:
            for i in range(len(cards)):
                rtn_str += cards[i].get("fancy")
        else:
            for i in range(num):
                rtn_str += cards[i].get("fancy")
        return rtn_str

    def count_cards(self, deck):  # counts and returns a dict of the number of all cards
        d = {}
        for key, value in self.card_dict["ranks"].items():
            d[key] = 0
        for card in deck:
            card_rank = card.get()["rank"]
            if card_rank not in d:
                d[card_rank] = 1
            else:
                d[card_rank] += 1
        return d

    @staticmethod
    def sort_deck(deck, by="suit", reverse=False):
        if by == "suit":
            sorted_deck = sorted(deck, key=lambda x: x.suit, reverse=reverse)  # Bro I don't get this but this is how you do it
        elif by == "rank":
            sorted_deck = sorted(deck, key=lambda x: x.rank, reverse=reverse)
        return sorted_deck

    @staticmethod
    def draw_card(deck, num=5):
        drawn_cards = []
        for i in range(num):
            try:
                drawn_cards.append(deck.pop(0))
            except IndexError:
                print("There are no cards left!")
        return drawn_cards
