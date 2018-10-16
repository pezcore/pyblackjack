from random import shuffle
from collections import deque

DECK = ["A", 2, 3, 4, 5, 6, 7, 8, 9, "T", "J", "Q", "K"] * 4
H17 = True

class Hand (deque):

    def __init__(self, it=(), wager=2, **kwargs):
        self.value = 0
        self.soft = False
        self.wager = wager
        for i in it:
            self.append(i if isinstance(i, str) and i in "TJQKA" else int(i))

    def append(self, item):
        super().append(item)
        self.value += (
            10 if isinstance(item, str) and item in "TJQK" else
            11 if item == "A" else item
        )
        self.soft |= item == "A"
        if self.value > 21 and self.soft:
            self.soft = False
            self.value -= 10

    def clear(self):
        super().clear()
        self.value = 0
        self.soft = False 

    def __str__(self):
        return "".join(map(str, self))

    def comp(self, dealer):
        if self.bust or (dealer.blackjack and not self.blackjack):
            outcome = "L"
            delta = -self.wager
        else:
            dealer.play(shoe)

            if self.blackjack and not dealer.blackjack:
                outcome = "B"
                delta = 3 * self.wager / 2
            elif self.value > dealer.value or dealer.value > 21:
                outcome = "W"
                delta = self.wager
            elif self.value < dealer.value:
                outcome = "L"
                delta = -self.wager
            else:
                outcome = "P"
                delta = 0
        return outcome, delta

    def draw(self, shoe):
        self.clear()
        self.append(shoe.pop())
        self.append(shoe.pop())

    def play(self, shoe, dealer_up="?"):
        while self.value < 17:
            self.append(shoe.pop())
        if H17 and self.value == 17 and self.soft:
            self.append(shoe.pop())

    def split(self, shoe):
        new = Hand()
        new.append(self.pop())
        self.append(shoe.pop())
        new.append(shoe.pop())
        return new

    @property
    def blackjack(self):
        return self.value == 21 and len(self) == 2

    @property
    def bust(self):
        return self.value > 21

class Player (list):

    def play(self, shoe, dealer_up):
        this_hand = self[-1]
        # if all(x == "A" for x in this_hand) or all(x == 8 for x in this_hand):

        
# Start of game
shoe = DECK * 8
shuffle(shoe)
bankroll = 0
dealer = Hand()
player = Hand()

while len(shoe) > 15:

    # Deal out player and dealer
    dealer.draw(shoe)
    player.draw(shoe)

    # player naively plays like a dealer:
    player.play(shoe, dealer[0])
    outcome, delta = player.comp(dealer)
    bankroll += delta

    print(
        f"{str(player):7} {str(dealer):7} {player.value:2} {dealer.value:2}",
        outcome, f"{bankroll:3}")

