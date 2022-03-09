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
        flush_suit = temp["suit"].loc[temp["size"] >= 5].values[0]  # prints the name of the suit with the flush
        return True, flush_suit
    except:
        print("no flush")
        return False, None


def is_straight_flush(cards):
    flush, suit = is_flush(cards)  # late i will change it that the function will be called only if flush was correct
    if is_flush(cards):
        cardsLst = cards.loc[cards["suit"] == suit].sort_values("value").value.to_list()
        if len(cardsLst) == 7 and cardsLst[2:7] == list(range(cardsLst[2], cardsLst[2] + 5)):
            return True, cardsLst, suit
        elif len(cardsLst) == 6 and cardsLst[1:6] == list(range(cardsLst[1], cardsLst[0] + 5)):
            return True, cardsLst, suit
        elif cardsLst == list(range(cardsLst[0], cardsLst[0] + 5)):
            return True, cardsLst, suit
        else:
            return False, None, None
    else:
        return False, None, None


def is_straight(cards):
    cardsLst = cards.sort_values("value").value.to_list()
    cardsLst = list(set(cardsLst))
    for i in range(3):
        if any((cardsLst[i:(i + 5)] == list(range(cardsLst[i], cardsLst[i] + 5)) for i in range(3))):
            print(cardsLst)
            return True
    return False


def main():
    c1 = Card(2, "hearts")
    c2 = Card(2, "diamonds")
    cc = CommunityCards()
    cc.flop(Card(2, "diamonds"), Card(7, "diamonds"), Card(7, "spades"))
    cc.turn(Card(5, "diamonds"))
    cc.river(Card(5, "diamonds"))
    noy = PlayerHand(c1, c2)
    print(is_straight(pd.concat([noy.hand, cc.comCard], ignore_index=True)))


if __name__ == '__main__':
    main()
