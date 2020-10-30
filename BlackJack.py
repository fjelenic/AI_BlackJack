import numpy as np


class Game:

    def __init__(self):
        self.deck = [2,3,4,5,6,7,8,9,10,10,10,10,'A']
        self.bet = 2
        '''
        self.actions = {0:self.hit,
                        1:self.stand,
                        2:self.double,
                        3:self.split}
        '''

    def play(self, player, player_hand=None, dealer_hand=None):
        pot = self.bet
        if not player_hand:
            player_hand = Hand()
            player_hand.add(self.draw())
        player_hand.add(self.draw())
        if not dealer_hand:
            dealer_hand = Hand()
            dealer_hand.add(self.draw())
        if player_hand.value == 21:
            dealer_hand.add((self.draw()))
            if dealer_hand.value != 21:
                pot += 3/2 * self.bet
            return
        action = player.action(player_hand,dealer_hand)
        while action != 1:
            if action == 0:
                player_hand.add(self.draw())
                if player_hand.value > 21:
                    player.score -= pot
                    return
                if player_hand.value == 21:
                    break
            if action == 2:
                player_hand.add(self.draw())
                pot += self.bet
                if player_hand.value > 21:
                    player.score -= pot
                    return
                break
            if action == 3:
                new_hand1 = Hand()
                new_hand2 = Hand()
                if player_hand.soft:
                    new_hand1.add('A')
                    new_hand2.add('A')
                else:
                    new_hand1.add(int(player_hand.value/2))
                    new_hand2.add(int(player_hand.value/2))
                self.play(player,new_hand1,dealer_hand)
                self.play(player,new_hand2,dealer_hand)
                return
            action = player.action(player_hand, dealer_hand)
        while dealer_hand.value < 17:
            dealer_hand.add(self.draw())
        if dealer_hand.value > 21:
            player.score += pot
            return
        if dealer_hand.value > player_hand.value:
            player.score -= pot
        elif player_hand.value > dealer_hand.value:
            player.score += pot
        return



    def draw(self):
        return self.deck[np.random.randint(len(self.deck))]




class Hand:

    def __init__(self):
        self.soft = False
        self.value = 0
        self.size = 0
        self.pair = False

    def add(self,card):
        self.pair = False
        if self.size == 1:
            if card == 'A' and self.value == 11:
                self.pair = True
            if card == self.value:
                self.pair = True
        if card == 'A':
            if self.value + 11 > 21:
                self.value += 1
            else:
                self.value += 11
                self.soft = True
        else:
            if self.value + card > 21 and self.soft:
                self.value += card - 10
                self.soft = False
            else:
                self.value += card
        self.size += 1
        return self


