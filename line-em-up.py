import time
import numpy as np
import random

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    # □ = 0
    # ◦ = 1
    # • = 2
    # ⊠ = 3

    def __init__(self, recommend = True, n = 3, b = 0, s = 3):
        self.recommend = recommend
        self.n = n
        self.b = b
        self.s = s
        self.check_valid_args()
        self.initialize_game()


    def check_valid_args(self):
        invalid = False
        if self.n < 3 or self.n > 10:
            print("Invalid argument: n should be in the range [3..10]")
            invalid = True
        if self.b < 0 or self.b > 2*self.n:
            print("Invalid argument: b should be in the range [0..2n]")
            invalid = True
        if self.s < 3 or self.s > self.n:
            print("Invalid argument: s should be in the range [3..n]")
            invalid = True

        if invalid:
            quit()


    def initialize_game(self):
        print("DEBUG: INITIALIZING GAME")
        # empty matrix
        self.current_state = np.zeros((self.n, self.n))
        self.player_turn = '◦'
        self.play_count = self.b


        # initialize blocks
        placed_blocks = 0
        while placed_blocks < self.b:
            x = random.randrange(0, self.n)
            y = random.randrange(0, self.n)

            if self.current_state[x][y] != 3:
                self.current_state[x][y] = 3
                placed_blocks += 1


    def draw_board(self):
        print()
        for y in range(0, self.n):
            for x in range(0, self.n):
                if self.current_state[x][y] == 0:
                    print('□ ', end='')
                elif self.current_state[x][y] == 1:
                    print('◦ ', end='')
                elif self.current_state[x][y] == 2:
                    print('• ', end='')
                elif self.current_state[x][y] == 3:
                    print('⊠ ', end='')
            print()
        print()


    def is_valid(self, px, py):
        if px < 0 or px > self.n or py < 0 or py > self.n:
            return False
        elif self.current_state[px][py] != 0:
            return False
        else:
            return True


    # returns 1 for white win, 2 for black win, -1 for tie and None when game isn't done
    def is_end(self):
        # Vertical win
        prev = -1
        for y in range(0, self.n):
            consecutive = 0
            for x in range(0, self.n):
                # encounter block or empty
                if self.current_state[x][y] == 0 or self.current_state[x][y] == 3:
                    consecutive = 0
                # encounter previous x or o
                elif self.current_state[x][y] == prev:
                    consecutive += 1
                    if consecutive == self.s:
                        return self.current_state[x][y]
                # encounter new x or o
                else:
                    prev = self.current_state[x][y]
                    consecutive = 1

        # Horizontal win
        prev = -1
        for x in range(0, self.n):
            consecutive = 0
            for y in range(0, self.n):
                # encounter block or empty
                if self.current_state[x][y] == 0 or self.current_state[x][y] == 3:
                    consecutive = 0
                # encounter previous x or o
                elif self.current_state[x][y] == prev:
                    consecutive += 1
                    if consecutive == self.s:
                        return self.current_state[x][y]
                # encounter new x or o
                else:
                    prev = self.current_state[x][y]
                    consecutive = 1


        # Diagonal win
        # the max offset is n - s since |diag[]| with offset n = 0, n-1 = 1, n-2 = 2 ... n-s = s
        for i in range(0, self.n - self.s + 1):
            #### Standard Diagonals ####
            diag_r = self.current_state.diagonal(offset=i)
            diag_l = self.current_state.diagonal(offset=-i)

            # print(f"DEBUG:\n{diag_r}\n{diag_l} ")

            prev_r = -1
            prev_l = -1
            consecutive_r = 0
            consecutive_l = 0

            # both same length
            # diag_r
            for j in range(0, len(diag_r)):
                # encounter block or empty
                if diag_r[j] == 0 or diag_r[j] == 3:
                    consecutive_r = 0
                # encounter previous x or o
                elif diag_r[j] == prev_r:
                    # print(f"DEBUG: Consecutive r {consecutive_r}")
                    consecutive_r += 1
                    if consecutive_r == self.s:
                        return diag_r[j]
                # encounter new x or o
                else:
                    prev_r = diag_r[j]
                    consecutive_r = 1

                # diag_l
                # encounter block or empty
                if diag_l[j] == 0 or diag_l[j] == 3:
                    consecutive_l = 0
                # encounter previous x or o
                elif diag_l[j] == prev_l:
                    consecutive_l += 1
                    if consecutive_l == self.s:
                        return diag_l[j]
                # encounter new x or o
                else:
                    prev_l = diag_l[j]
                    consecutive_l = 1

            #### Inverse Diagonals ####
            diag_r = np.fliplr(self.current_state).diagonal(offset=i)
            diag_l = np.fliplr(self.current_state).diagonal(offset=-i)

            # print(f"DEBUG:\n{diag_r}\n{diag_l} ")

            prev_r = -1
            prev_l = -1
            consecutive_r = 0
            consecutive_l = 0

            # both same length
            # diag_r
            for j in range(0, len(diag_r)):
                # encounter block or empty
                if diag_r[j] == 0 or diag_r[j] == 3:
                    consecutive_r = 0
                # encounter previous x or o
                elif diag_r[j] == prev_r:
                    consecutive_r += 1
                    if consecutive_r == self.s:
                        return diag_r[j]
                # encounter new x or o
                else:
                    prev_r = diag_r[j]
                    consecutive_r = 1

                # diag_l
                # encounter block or empty
                if diag_l[j] == 0 or diag_l[j] == 3:
                    consecutive_l = 0
                # encounter previous x or o
                elif diag_l[j] == prev_l:
                    consecutive_l += 1
                    if consecutive_l == self.s:
                        return diag_l[j]
                # encounter new x or o
                else:
                    prev_l = diag_l[j]
                    consecutive_l = 1



        # Is whole board full?
        if self.play_count >= self.n*self.n:
            print("DEBUG: BOARD FULL")
            # It's a tie!
            return -1

        return None

    def check_end(self):
        if self.play_count - self.b < self.s:
            return None

        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 1:
                print('The winner is ◦ !')
            elif self.result == 2:
                print('The winner is • !')
            elif self.result == -1:
                print("It's a tie!")
            self.initialize_game()
        return self.result


    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == '◦':
            self.player_turn = '•'
        elif self.player_turn == '•':
            self.player_turn = '◦'
        return self.player_turn


    def minimax(self, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 1:
            return (-1, x, y)
        elif result == 2:
            return (1, x, y)
        elif result == -1:
            return (0, x, y)
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == 0:
                    if max:
                        self.current_state[i][j] = 2
                        (v, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 1
                        (v, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = 0
        return (value, x, y)


    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 1:
            return (-1, x, y)
        elif result == 2:
            return (1, x, y)
        elif result == -1:
            return (0, x, y)
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.current_state[i][j] == 0:
                    if max:
                        self.current_state[i][j] = 2
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 1
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = 0
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)


    def play(self,algo=None,player_x=None,player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == '◦':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else: # algo == self.ALPHABETA
                if self.player_turn == '◦':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == '◦' and player_x == self.HUMAN) or (self.player_turn == '•' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x,y) = self.input_move()
            if (self.player_turn == '◦' and player_x == self.AI) or (self.player_turn == '•' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')

            if(self.player_turn == '◦'):
                self.current_state[x][y] = 1
                self.play_count += 1
            elif(self.player_turn == '•'):
                self.current_state[x][y] = 2
                self.play_count += 1
            else:
                print("OOPS, SOMETHING WENT WRONG")

            self.switch_player()

def main():
    g = Game(recommend=True, n=3, b=1)
    g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
    g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)
    # g.play(algo=Game.HUMAN,player_x=Game.HUMAN,player_o=Game.HUMAN)

if __name__ == "__main__":
    main()


