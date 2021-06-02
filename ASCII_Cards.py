import Cards
from colorama import Fore
from colorama import Back
from colorama import Style
# 10's were manually drawn because of its length.
ascii_dict = {"S": [[" _____ ",
                     "|R .  |",
                     "| /.\ |",
                     "|(_._)|",
                     "|  |  |",
                     "|____R|"],
                    [" _____ ",
                     "|10.  |",
                     "| /.\ |",
                     "|(_._)|",
                     "|  |  |",
                     "|___10|"]],
              "D": [[" _____ ",
                     "|R ^  |",
                     "| / \ |",
                     "| \ / |",
                     "|  .  |",
                     "|____R|"],
                    [" _____ ",
                     "|10^  |",
                     "| / \ |",
                     "| \ / |",
                     "|  .  |",
                     "|___10|"]],
              "C": [[" _____ ",
                     "|R _  |",
                     "| ( ) |",
                     "|(_'_)|",
                     "|  |  |",
                     "|____R|"],
                    [" _____ ",
                     "|10_  |",
                     "| ( ) |",
                     "|(_'_)|",
                     "|  |  |",
                     "|___10|"]],
              "H": [[" _____ ",
                     "|R_ _ |",
                     "|( v )|",
                     "| \ / |",
                     "|  .  |",
                     "|____R|"],
                    [" _____ ",
                     "|10 _ |",
                     "|( v )|",
                     "| \ / |",
                     "|  .  |",
                     "|___10|"]],
        "Facedown": [" _____ ",
                    r"|\\~//|",
                     "|}}:{{|",
                     "|}}:{{|",
                     "|}}:{{|",
                    r"|//~\\|"]}
class CardToASCII:
    def __init__(self):
        pass

    @staticmethod
    def draw_ASCII(hand, num_facedown=0):
        rtn_str = Back.LIGHTBLACK_EX + ""
        for i in range(len(ascii_dict["S"][0])):
            for card in hand:
                rank = card.get()["rank"]
                suit = card.get()["suit"]
                color = card.get()["color"]
                if color == "red":
                    if rank == "10":
                        rtn_str += Fore.RED + ascii_dict[suit][1][i] + Fore.RESET
                    else:
                        rtn_str += Fore.RED + ascii_dict[suit][0][i].replace("R", rank)
                elif color == "black":
                    if rank == "10":
                        rtn_str += Fore.BLACK + ascii_dict[suit][1][i] + Fore.RESET
                    else:
                        rtn_str += Fore.BLACK + ascii_dict[suit][0][i].replace("R", rank) + Fore.WHITE
            for j in range(num_facedown):
                rtn_str += Fore.RESET + ascii_dict["Facedown"][i]
            rtn_str += "\n"
        rtn_str += Back.RESET + Fore.RESET
        return rtn_str
""" # Test cards
CH = Cards.CardHandler()
CTA = CardToASCII()
deck = CH.make_deck(show=True)
deck.insert(0, Cards.Card("10", "S"))
hand = []
hand += CH.draw_card(deck)
print(CH.show_cards(hand))
print(CTA.draw_ASCII(hand, num_facedown=2))
"""