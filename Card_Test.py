import Cards
import ASCII_Cards
import time
CH = Cards.CardHandler()
AC = ASCII_Cards.CardToASCII()

def multi_deck(n):
    deck = CH.make_deck()
    deck *= n
    return deck

deck = multi_deck(100000)

CH.shuffle_cards(deck)

while True:
    time.sleep(.00000001)
    hand = CH.draw_card(deck, 25)
    print("You have " + str(len(deck)) + " left.")
    #print(CH.count_cards(deck))
    print(AC.draw_ASCII(hand))
    if len(deck) == 0:
        time.sleep(.0000001)
        deck = CH.make_deck()
        print("Shuffling deck")
    hand.clear()
