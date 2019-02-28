import numpy as np

class GameState:
    def __init__(self):
        self.round = 1
        self.player1hands = [1,1]
        self.player2hands = [1,1]
        self.lastMove = ""
        self.allMoves = [[[1,1], [1,1]]]

    def display_game_state(self):
        print("round")
        print(self.round)
        self.print_hands()
        print("Last Move")
        print(self.lastMove)
        print("All Hands")
        print(self.allMoves)

    def print_hands(self):
        print("hands")
        print(self.player1hands)
        print(self.player2hands)

    def move(self, XX):
        if self.round % 2 == 1 :
            if XX == "LL" :
                self.player2hands[0] = self.player2hands[0] + self.player1hands[0]
        self.round += 1
        self.lastMove = XX
        self.allMoves.append([self.player1hands, self.player2hands])
        return self


r1 = GameState()
r1.display_game_state()

r2 = r1.move("LL")
r2.display_game_state()

r3 = r2.move("LL")
