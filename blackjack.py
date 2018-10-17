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

    def __sub__(self, dealer):
        if self << dealer or self.bust:
            return "L"
        if dealer << self:
            return "B"
        if self > dealer or dealer.bust:
            return "W"
        if self < dealer:
            return "L"
        return "P"

        if self.bust or (self.value < dealer.value and dealer.value <= 21):
            return "L"

    def __lt__(self, other):
        return self.value < (other.value if isinstance(other, Hand) else other)

    def __gt__(self, other):
        return self.value > (other.value if isinstance(other, Hand) else other)

    def __lshift__(self, dealer):
        """
        Return True iff the right operand is a blackjack and the left one isn't.

        With the left operand representing the player Hand and the right
        operand representing the dealer Hand, This indicates the initial
        deal outcome where the player position in this game is
        immediately determined a loss.
        """
        return (dealer.blackjack and not self.blackjack)


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

    if player << dealer:
        outcome = "L"
        bankroll -= player.wager
    else:
        # player naively plays like a dealer:
        player.play(shoe, dealer[0])

        if player.bust:
            outcome = "L"
            bankroll -= player.wager
        else:
            dealer.play(shoe)
            outcome = player - dealer
            bankroll += (player.wager if outcome == "W" else
                         -player.wager if outcome == "L" else
                         3 * player.wager / 2 if outcome == "B" else 0)

    print(
        f"{str(player):7} {str(dealer):7} {player.value:2} {dealer.value:2}",
        outcome, f"{bankroll:6.1f} {8 * 52 - len(shoe):3d}"
    )

