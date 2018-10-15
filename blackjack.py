from random import shuffle
from collections import deque

DECK = ["A", 2, 3, 4, 5, 6, 7, 8, 9, "T", "J", "Q", "K"] * 4
H17 = True

class Hand (deque):

    def __init__(self, it=(), **kwargs):
        self.value = 0
        self.soft = False
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

    @property
    def blackjack(self):
        return self.value == 21 and len(self) == 2

    @property
    def bust(self):
        return self.value > 21

class Player (Hand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def play(self, shoe, dealer_up="?"):
        while self.value < 17:
            self.append(shoe.pop())
        if H17 and self.value == 17 and self.soft:
            self.append(shoe.pop())
        

# Start of game
shoe = DECK * 8
shuffle(shoe)
bankroll = 0

while len(shoe) > 15:

    # Deal out player and dealer
    dealer = Player([shoe.pop(), shoe.pop()])
    player = Player([shoe.pop(), shoe.pop()])

    # player naively plays like a dealer:
    player.play(shoe)

    if player.bust or (dealer.blackjack and not player.blackjack):
        outcome = "L"
        bankroll -= 2
    else:
        dealer.play(shoe)

        if player.blackjack and not dealer.blackjack:
            outcome = "B"
            bankroll += 3
        elif player.value > dealer.value or dealer.value > 21:
            outcome = "W"
            bankroll += 2
        elif player.value < dealer.value:
            outcome = "L"
            bankroll -= 2
        else:
            outcome = "P"


    print(
        f"{str(player):7} {str(dealer):7} {player.value:2} {dealer.value:2}",
        outcome, f"{bankroll:3}")

