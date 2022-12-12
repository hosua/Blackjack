import Cards
import os
import pickle
import ASCII_Cards
import time
# from playsound import playsound
from Large_Text_Handler import Handler
from colorama import Fore
from colorama import Back
AC = ASCII_Cards.CardToASCII()
root = os.getcwd()
# sound_path = os.path.join(root, "Sounds")
# win_sound = os.path.join(sound_path, "tada.mp3")
# lose_sound = os.path.join(sound_path, "fail.mp3")
# neutral_sound = os.path.join(sound_path, "neutral.mp3")
# no_money_sound = os.path.join(sound_path, "the-price-is-right-losing-horn.mp3")

COLOR_MODE = True

# Colors
COL_WHITE = ""
COL_WIN = ""
COL_LOSE = ""
COL_PLAYER = ""
COL_AI = ""
COL_BLACKJACK = ""
COL_STATS = ""
COL_BLACK = ""
COL_RESET = ""
if COLOR_MODE: 
    COL_WHITE = Fore.LIGHTWHITE_EX
    COL_WIN = Fore.GREEN
    COL_LOSE = Fore.RED
    COL_PLAYER = Fore.BLUE
    COL_AI = Fore.RED
    COL_BLACKJACK = Fore.YELLOW
    COL_STATS = Fore.MAGENTA
    COL_BLACK = Fore.LIGHTBLACK_EX
    COL_RESET = Fore.RESET

CH = Cards.CardHandler()
deck = CH.make_deck()
card_dict = CH.card_dict
blackjack_dict = {"2": [2], "3": [3], "4": [4], "5": [5], "6": [6], "7": [7], "8": [8], "9": [9], "10": [10], "J": [10],
                  "Q": [10], "K": [10], "A": [1, 11]}


class Blackjack:
    def __init__(self):
        self.deck = []  # Implement more decks later
        pass

    @staticmethod
    def create_decks(num_decks):
        new_deck = []
        for i in range(num_decks):
            new_deck += CH.make_deck()
        print(COL_WHITE + "Created deck of size " + str(num_decks) + ".")
        CH.shuffle_cards(new_deck)
        return new_deck

    @staticmethod
    def win_message(win):
        if win == "win":
            # playsound(win_sound, block=False)
            return COL_WIN + "You win!" + "\n" + COL_RESET
        elif win == "lose":
            # playsound(lose_sound, block=False)
            return COL_LOSE + "You lose!" + "\n" + COL_RESET
        elif win == "tie":
            # playsound(neutral_sound, block=False)
            return COL_WHITE + "Tie!" + "\n"

    @staticmethod
    def move_ace_to_end(hand):  # need this for points calculations
        for i in range(len(hand)-1, -1, -1):     # Since were appending a popped index, the indices change
            if hand[i].get()["rank"] == "A":    # so iterate backwards to get around this
                hand.append(hand.pop(i))

    def check_hand(self, hand, player=True, no_sort=False):
        pts = 0
        if not no_sort:
            self.move_ace_to_end(hand)  # important for checking points later

        def tally_score():
            pts = 0
            for i in range(len(hand)):
                if hand[i].get()["rank"] != "A":
                    pts += blackjack_dict[hand[i].get()["rank"]][0] # Just add points for every card except aces.
                else:  # if it's an ace
                    ace_1 = blackjack_dict[hand[i].get()["rank"]][0]
                    ace_11 = blackjack_dict[hand[i].get()["rank"]][1]
                    if hand.count(card_dict["ranks"]["A"]) > 0:  # if there are still aces left
                        pts += ace_1  # add one point
                    else:  # if this is the last ace
                        if hand[i] == hand[-1]:  # if the last card in hand
                            hand.append(hand.pop(i))  # add ace to end of hand
                        if pts + ace_11 > 21:
                            pts += ace_1
                        else:
                            pts += ace_11
                if hand[i] == hand[-1]:
                    return pts
        if pts > 21:
            if hand.count(card_dict["ranks"]["A"]) == 0:    # if no aces, automatic loss
                if player:
                    pl = "Your"
                    self.win_message("lose")
                else:
                    pl = "Dealer"
                    self.win_message("win")
                print(pl, "points:", pts)
                return -1
        return tally_score()

    def check_hand_again(self, hand, player=True, no_sort=False):
        pts = 0
        if not no_sort:
            self.move_ace_to_end(hand)  # important for checking points later

        def tally_score():
            pts = 0
            for i in range(len(hand)):
                pts += blackjack_dict[hand[i].get()["rank"]][0]     # Treat aces as ones this time
                if hand[i] == hand[-1]:
                    return pts
        if pts > 21:
            if hand.count(card_dict["ranks"]["A"]) == 0:    # if no aces, automatic loss
                if player:
                    pl = "Your"
                    self.win_message("lose")
                else:
                    pl = "Dealer"
                    self.win_message("win")
                print(pl, "points:", pts)
                return -1
        return tally_score()
    def split_pair(self):   # Might implement this later idk. I need to implement a betting system first.
        pass

    @staticmethod
    def hit(deck, hand, player="player"):
        time.sleep(1)
        hand.append(CH.draw_card(deck, 1)[0])
        BJ.move_ace_to_end(hand)
        pts = BJ.check_hand(hand)
        if pts > 21:
            pts = BJ.check_hand_again(hand)
        if player == "player":
            print(COL_PLAYER + "Your hand:")
            print("Your points:", pts)
            print(AC.draw_ASCII(hand))

        else:
            print(COL_AI + "Dealer hand:")
            print("Dealer points:", pts)
            print(AC.draw_ASCII(hand))

        if pts > 21:
            BJ.move_ace_to_end(hand)
            CH.show_cards(hand)
            pts = BJ.check_hand(hand)
            if pts > 21:    # if points are still greater than 21 after previous check, player loses
                print(BJ.check_hand_again(hand))
                pts = BJ.check_hand_again(hand)

                if pts > 21:
                    return -1
        return pts

    def get_player_move(self, p1_hand, p1_points):
        try:
            user_move = input(COL_WHITE + "Enter hit or stand.\n"
                                                   "You can also type h or s instead.\n").lower()
            if user_move == "hit":
                p1_hand + CH.draw_card(deck, 1)
            elif user_move == "stand":
                CH.show_cards(p1_hand)
            elif user_move == "quit":
                quit()
            return user_move
        except:
            print("Invalid input, try again.")
            self.get_player_move(p1_hand, p1_points)

    @staticmethod
    def display_stats(win_dict, money_dict):
        rtn = ""
        rtn += "Stats: \n"
        for key, value in win_dict.items():
            rtn += key + ":" + str(value) + "|"
        rtn += "\n"
        for key, value in money_dict.items():
            rtn += key + ": " + "${:,.2f}".format(value) + "|"
        return print(COL_STATS + rtn.upper() + COL_RESET)

    @staticmethod
    def get_bet(money):     # returns bet, money left
        print(COL_WHITE + "You have " + COL_WIN + "${:,.2f}".format(money) + COL_RESET + ".")
        try:
            bet = float(input(COL_WHITE +
                              "How much would you like to bet? You may only bet up to $500 per game.\n"))
            if bet <= 0:
                print("You must bet more than $0!!")
                return 0
            if bet > 500:
                print("You can't bet over $500!")
                return 0
            if bet > money:
                print("You do not have enough money!")
                return 0
        except ValueError:
            return 0
        money -= bet  # if we reach here then all checks were passed
        print("You now have " + COL_WIN + "${:,.2f}".format(money) + COL_RESET + ".")
        return bet, money

    @staticmethod
    def get_payout(bet, payout_type="normal"):
        if payout_type == "normal":
            payout = 2 * bet
        elif payout_type == "blackjack":
            payout = bet + bet * (3/2)
        elif payout_type == "no winner":
            payout = bet
        print(COL_WIN + "You won " + "${:,.2f}".format(payout) + "!" + COL_RESET)
        return payout

    @staticmethod
    def compare_scores(p1_score, p2_score, win_dict):
        if p1_score > 21 or p1_score == -1:
            win_dict["losses"] += 1
            return "lose"
        if p2_score > 21 or p2_score == -1:
            win_dict["wins"] += 1
            return "win"
        if p1_score > p2_score:
            win_dict["wins"] += 1
            return "win"
        elif p2_score > p1_score:
            win_dict["losses"] += 1
            return "lose"
        elif p2_score == p1_score:  # scores are equal
            win_dict["ties"] += 1
            return "tie"

    def title_screen(self):
        global COLOR_MODE
        print("NOTE: If you see leading and trailing garbage characters, colors do not work in your terminal!\n"
                "Refer to the README to fix this issue.\n\n");
        user_in = int(input(COL_WHITE + "1) Play Game\n" \
                            "2) How to play\n"
                            "3) Delete save\n"
                            "4) Quit\n"))
        if user_in == 1:
            return
        if user_in == 2:
            with open("Blackjack_Tutorial.txt", "r") as f:
                line_lst = f.readlines()
            rtn = COL_STATS + ""
            for line in line_lst:
                rtn += line
            print(rtn + "\n" + COL_RESET)
            f.close()
            self.title_screen()
        if user_in == 3:
            try:
                options = input("Are you sure? Doing this will start a new game and wipe your save. (y/n)\n").lower()
                if options == "y":
                    d = [{"wins": 0, "losses": 0, "ties": 0},
                                            {"money won": 0, "money lost": 0, "net gain": 0}]
                    DH.save_data(d)
                elif options == "n":
                    print("Returning to the title screen.")
                    self.title_screen()
            except ValueError:
                print("Invalid input.")
                self.title_screen()
        if user_in == 4:
            print("Quitting the game...")
            quit()

    @staticmethod
    def main(deck, win_dict, bet_amount, player_money):

        p1_points, dealer_points = 0, 0
        p1_hand = CH.draw_card(deck, 2)
        dealer_hand = CH.draw_card(deck, 2)
        p1_points = BJ.check_hand(p1_hand)
        print(COL_PLAYER + "Your hand:")
        print(COL_PLAYER + "Your points:", p1_points)
        print(AC.draw_ASCII(p1_hand))
        print(COL_AI + "Dealer hand:")  # show one of the dealer's cards
        print(AC.draw_ASCII(dealer_hand[:1], num_facedown=1))
        BJ.move_ace_to_end(p1_hand)  # with a card face down
        isBlackjack = False
        player_turn = True
        #double_down = False

        while player_turn:
            # first_turn = True   # For double down
            if p1_points != 21:  # Check that we do not already have a blackjack first
                move = BJ.get_player_move(p1_hand, p1_points).lower()
                if move == "hit" or move == "h":
                    # first_turn = False
                    p1_points = BJ.hit(deck, p1_hand, player="player")  # Aces are sorted and score is reevaluated.
                    BJ.check_hand(p1_hand)
                    if p1_points == 21:
                        payout = BJ.get_payout(bet_amount, "blackjack")
                        isBlackjack = True
                        print(COL_BLACKJACK + "Blackjack!")
                        player_turn = False
                if move == "stand" or move == "s":
                    BJ.check_hand(p1_hand, no_sort=True)    # sorting when will screw up point calculations so don't
                    player_turn = False
                if p1_points == -1:
                    player_turn = False
                """
                if (move == "double" or move == "d") and first_turn and player_money > bet_amount * 2:    # For double down
                    print(COL_WIN + "You doubled down! Good luck." + COL_RESET)
                    double_down = True
                    player_money -= bet_amount
                    bet_amount += bet_amount
                """
            else:
                isBlackjack = True
                player_turn = False
        dealer_turn = True
        dealer_points = BJ.check_hand(dealer_hand, dealer_points)
        print(COL_AI + "Dealer hand: ")
        print(COL_AI + "Dealer points: " + str(dealer_points))
        print(AC.draw_ASCII(dealer_hand))
        while dealer_turn:
            if p1_points == -1:
                break  # Game winner was already decided, so skip dealer's turn
            if dealer_points < 17:
                if not isBlackjack:
                    move = "hit"
                else:
                    move = "stand"
            elif dealer_points > 16:
                move = "stand"
            if move == "hit":
                dealer_points = BJ.hit(deck, dealer_hand,
                                       player="Dealer")
                # Here, aces are sorted and score is reevaluated.
                BJ.move_ace_to_end(dealer_hand)
            elif move == "stand":
                BJ.check_hand(dealer_hand, player=False, no_sort=True)
                dealer_turn = False
            if dealer_points == -1:
                dealer_turn = False


        result = BJ.compare_scores(p1_points, dealer_points, win_dict)
        if result == "win":
            if not isBlackjack:
                payout = BJ.get_payout(bet_amount)
            else:
                payout = BJ.get_payout(bet_amount, "blackjack")
            money_dict["money won"] += payout - bet_amount
        if result == "lose":
            money_dict["money lost"] += bet_amount
            payout = 0
        if result == "tie":
            payout = BJ.get_payout(bet_amount, "no winner")
        money_dict["net gain"] = money_dict["money won"] - money_dict["money lost"]
        print("\n" + BJ.win_message(result))
        return payout


class DataHandler:
    def __init__(self):
        pass

    @staticmethod
    def get_data():
        try:
            print(COL_WIN + "Loading data from file" + COL_RESET + "\n")
            with open("data.p", "rb") as handle:
                return pickle.load(handle)
        except FileNotFoundError:
            print("File not found!")
        return None

    @staticmethod
    def save_data(data):
        pickle.dump(data, open("data.p", "wb"))


d = [{"wins": 0, "losses": 0, "ties": 0}, {"money won": 0, "money lost": 0, "net gain": 0}]
win_dict, money_dict = d
LTH = Handler()     # Large text handler
DH = DataHandler()
BJ = Blackjack()
print(COL_BLACK + LTH.get_text("blackjack title"))
print(COL_BLACKJACK + LTH.get_text("logo1") + "\n")
BJ.title_screen()
if "data.p" not in os.listdir():  # make data file if it doesn't exist
    print(COL_WIN + "Save data not found, creating new one...")
    DH.save_data(d)
    DH.get_data()
else:
    win_dict, money_dict = DH.get_data()

print(COL_RESET)

player_money = 2000
deck = BJ.create_decks(6)
# TEST CASES
"""
deck.insert(0, Cards.Card("K", "D"))    # TEST 5
deck.insert(0, Cards.Card("7", "D"))    # TEST 5
deck.insert(0, Cards.Card("7", "D"))    # TEST 5
deck.insert(0, Cards.Card("A", "D"))    # TEST 5
deck.insert(0, Cards.Card("K", "D"))    # TEST 5
"""
"""
deck.insert(0, Cards.Card("Q", "D"))    # TEST 4    # Should be a double blackjack resulting in a tie
deck.insert(0, Cards.Card("K", "D"))    # TEST 4      
deck.insert(0, Cards.Card("A", "D"))    # TEST 4
deck.insert(0, Cards.Card("K", "D"))    # TEST 4
deck.insert(0, Cards.Card("A", "D"))    # TEST 4
"""
"""
deck.insert(0, Cards.Card("Q", "D"))    # TEST 3    
deck.insert(0, Cards.Card("A", "D"))    # TEST 3
deck.insert(0, Cards.Card("A", "D"))    # TEST 3
deck.insert(0, Cards.Card("A", "D"))    # TEST 3
deck.insert(0, Cards.Card("A", "D"))    # TEST 3
"""
"""
deck.insert(0, Cards.Card("9", "D"))    # TEST 2    # Should be blackjack and dealer should not draw
deck.insert(0, Cards.Card("A", "D"))    # TEST 2
deck.insert(0, Cards.Card("A", "D"))    # TEST 2
deck.insert(0, Cards.Card("A", "D"))    # TEST 2
deck.insert(0, Cards.Card("A", "D"))    # TEST 2
"""
"""
deck.insert(0, Cards.Card("A", "D"))    # TEST 1
deck.insert(0, Cards.Card("8", "D"))    # TEST 1
"""
while True:
    BJ.display_stats(win_dict, money_dict)
    dont_play = False
    try:
        player_bet, player_money = BJ.get_bet(player_money)
    except TypeError:
        print("Invalid input!")
        dont_play = True

    if not dont_play:
        if player_bet == 0:     # This means user input was invalid.
            break
        player_money += BJ.main(deck, win_dict, player_bet, player_money)     # Funky way to do this but it works.

        d = [win_dict, money_dict]
        DH.save_data(d)
        if player_money == 0:
            print("Game over, you lost all your money!")
            # playsound(no_money_sound, block=False)
            player_money = 2000
            BJ.title_screen()
        print(COL_WHITE + "Starting a new game...")

    if len(deck) < 20:
        print("Deck was low on cards... resetting the deck.")
        deck = BJ.create_decks(6)
        CH.shuffle_cards(deck)
    print("Deck has " + str(len(deck)) + " cards remaining\n")

