import numpy as np


class Game:

    def __init__(self):
        self.deck = [2,3,4,5,6,7,8,9,10,10,10,10,'A']*4*8
        self.bet = 2
        '''
        self.actions = {0:hit,
                        1:stand,
                        2:double,
                        3:split}
        '''

    def play(self, player):
        dealer_hand = Hand(self)
        dealer_hand.add(self.draw())
        player_hand = PlayerHand(self,player)
        hands = player_hand.decide(dealer_hand)
        dealer_hand.add(self.draw())
        if dealer_hand.value == 21:
            for hand in hands:
                if hand.value != 'BJ':
                    player.score -= hand.pot
            return player
        while dealer_hand.value < 17:
            dealer_hand.add(self.draw())
        if dealer_hand.value > 21:
            for hand in hands:
                if hand.value == 'BJ':
                    player.score += (3/2) * hand.pot
                elif hand.value > 21:
                    player.score -= hand.pot
                else:
                    player.score += hand.pot
            return player
        for hand in hands:
            if hand.value == 'BJ':
                player.score += (3/2) * hand.pot
            elif hand.value > 21:
                player.score -= hand.pot
            elif hand.value < dealer_hand.value:
                player.score -= hand.pot
            elif hand.value > dealer_hand.value:
                player.score += hand.pot
        return player

    def draw(self):
        if len(self.deck) < 13*2*8:
            self.reshuffle()
        return self.deck.pop(np.random.randint(len(self.deck)))

    def reshuffle(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 'A'] * 4 * 8
        return self



class Hand:

    def __init__(self, game):
        self.soft = False
        self.value = 0
        self.size = 0
        self.pair = False
        self.game = game

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


class PlayerHand(Hand):

    def __init__(self, game, player):
        self.player = player
        self.pot = 0
        super().__init__(game)

    def decide(self,dealer_hand,i=1):
        if i > 3:
            self.pair = False
        self.pot += self.game.bet
        if i == 1:
            self.add(self.game.draw())
        self.add(self.game.draw())
        if self.value == 21:
            self.value = 'BJ'
            return [self]
        #if self.value == 4 and not self.pair:
        #    action = 0
        #else:
        action = self.player.action(self,dealer_hand)
        while action != 1:
            if action == 0:
                self.add(self.game.draw())
                if self.value >= 21:
                    break
            elif action == 2:
                self.pot += self.game.bet
                self.add(self.game.draw())
                break
            elif action == 3:
                if self.soft:
                    double_card = 'A'
                else:
                    double_card = int(self.value/2)
                new_hand1 = PlayerHand(self.game,self.player).add(double_card)
                new_hand2 = PlayerHand(self.game, self.player).add(double_card)
                i += 1
                decision1 = new_hand1.decide(dealer_hand,i)
                decision2 = new_hand2.decide(dealer_hand,i)
                return decision1 + decision2
        return [self]









