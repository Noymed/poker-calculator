from collections import Counter
import pandas as pd


class Card:
    def __init__(self, value, suit):
        self.card = pd.DataFrame.from_dict({"suit": [suit], "value": [value]})


class PlayerHand:
    def __init__(self, card1, card2):
        self.hand = pd.concat([card1.card, card2.card], ignore_index=True)


class CommunityCards:
    def __init__(self):
        self.comCard = pd.DataFrame(columns=['suit', 'value'])
        self.stage = 'pre flop'

    def flop(self, card1, card2, card3):
        self.comCard = pd.concat([card1.card, card2.card, card3.card], ignore_index=True)
        self.stage = 'flop'

    def turn(self, card):
        self.comCard = pd.concat([self.comCard, card.card])
        self.stage = 'turn'

    def river(self, card):
        self.comCard = pd.concat([self.comCard, card.card])
        self.stage = 'river'


def is_flush(cards):
    """ check if there is a flush combination out of a df of cards"""
    temp = cards.groupby('suit').size().reset_index(name='size')
    try:
        print(temp["suit"].loc[temp["size"] == 5].values[0])  # prints the name of the suit with the flush
    except:
        print("no flush")


def is_straight_flush(card_arr):
    card_arr.sort(key=lambda x: x.suit)


def main():
    c1 = Card(7, "hearts")
    c2 = Card(7, "diamonds")
    cc = CommunityCards()
    cc.flop(Card(3, "diamonds"), Card(2, "diamonds"), Card(6, "spades"))
    cc.turn(Card(4, "spades"))
    cc.turn(Card(4, "diamonds"))
    noy = PlayerHand(c1, c2)
    is_flush(pd.concat([noy.hand, cc.comCard], ignore_index=True))


if __name__ == '__main__':
    main()
