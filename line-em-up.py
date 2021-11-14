import time
import numpy as np
import random
from timeout import *

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    # □ = 0
    # ◦ = 1
    # • = 2
    # ⊠ = 3

    def __init__(self, recommend = True, n = 3, b = 0, s = 3, d1=6, d2=6, t=8):
        self.recommend = recommend
        self.n = n
        self.b = b
        self.s = s
        self.d1 = d1
        self.d2 = d2
        self.t = t
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
        self.eval_by_depth = {}


        # initialize blocks
        placed_blocks = 0
        while placed_blocks < self.b:
            x = random.randrange(0, self.n)
            y = random.randrange(0, self.n)

            if self.current_state[x][y] != 3:
                self.current_state[x][y] = 3
                placed_blocks += 1


    def get_board_state(self):
        board = ''
        for y in range(0, self.n):
            for x in range(0, self.n):
                if self.current_state[x][y] == 0:
                    board += '□ '
                elif self.current_state[x][y] == 1:
                    board += '◦ '
                elif self.current_state[x][y] == 2:
                    board += '• '
                elif self.current_state[x][y] == 3:
                    board += '⊠ '
            board += '\n'
        return board

    def draw_board(self):
        print()
        print(self.get_board_state())
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
                self.game_trace(info='The winner is ◦ !')
                print('The winner is ◦ !')
            elif self.result == 2:
                print('The winner is • !')
                self.game_trace(info='The winner is • !')
            elif self.result == -1:
                print("It's a tie!")
                self.game_trace(info="It's a tie!")
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

    """
    Doesn't take into account diagonals
    """
    def heuristic_v1(self):
        # columns
        score = 0
        h1 = 0
        h2 = 0

        for x in range(0, self.n):
            for y in range(0, self.n):
                if self.current_state[x][y] == 1:
                    score += 1
                elif self.current_state[x][y] == 2:
                    score -= 1
        # cubed to keep negative
        h1 = score * score * score
        score = 0

        # rows
        for y in range(0, self.n):
            for y in range(0, self.n):
                if self.current_state[x][y] == 1:
                    score += 1
                elif self.current_state[x][y] == 2:
                    score -= 1
        h2 = score * score * score
        score = 0

        return (h1 + h2)



    def minimax(self, depth, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:

        self.eval_by_depth[depth] = self.eval_by_depth.get(depth, 0) + 1

        if depth == 0:
            return (self.heuristic_v1(), -0, -0)

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
                        (v, _, _) = self.minimax(depth - 1, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 1
                        (v, _, _) = self.minimax(depth - 1, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = 0
        return (value, x, y)


    def alphabeta(self, depth, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:


        self.eval_by_depth[depth] = self.eval_by_depth.get(depth, 0) + 1

        if depth == 0:
            return (self.heuristic_v1(), -0, -0)

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
                        (v, _, _) = self.alphabeta(depth - 1, alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 1
                        (v, _, _) = self.alphabeta(depth - 1, alpha, beta, max=True)
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

    def random_move(self):
        possible_moves = []
        for x in range(0, self.n):
            for y in range(0, self.n):
                if self.current_state[x][y] == 0:
                    possible_moves.append((-0, x, y))
        return possible_moves[random.randrange(0, len(possible_moves))]


    def play(self,algo=None,player_x=None,player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN

        self.game_trace(player_x, player_o, initial=True)

        while True:
            self.draw_board()
            state_before_timeout = np.copy(self.current_state)
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                with Timeout(self.t):
                    try:
                        if self.player_turn == '◦':
                            (_, x, y) = self.minimax(self.d1, max=False)
                        else:
                            (_, x, y) = self.minimax(self.d2, max=True)
                    except timeout.TimeoutError:

                        self.game_trace(info=f'** Timeout at depth {max(list(self.eval_by_depth.keys()))}**')
                        self.current_state = state_before_timeout
                        (_, x, y) = self.random_move()

            else: # algo == self.ALPHABETA
                with Timeout(self.t):
                    try:
                        if self.player_turn == '◦':
                            (m, x, y) = self.alphabeta(self.d1, max=False)
                        else:
                            (m, x, y) = self.alphabeta(self.d2, max=True)
                    except timeout.TimeoutError:
                        print("timed out")
                        self.current_state = state_before_timeout
                        (_, x, y) = self.random_move()

            end = time.time()

            if (self.player_turn == '◦' and player_x == self.HUMAN) or (self.player_turn == '•' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x,y) = self.input_move()
            if (self.player_turn == '◦' and player_x == self.AI) or (self.player_turn == '•' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')

                # Info for game trace
                game_trace_info = f'''Player {self.player_turn} under AI control plays: x = {x}, y = {y}
i\tEvaluation time: {round(end - start, 7)}s
ii\tHeuristic evaluations: {sum(self.eval_by_depth.values())}
iii\tEvaluations by depth: {self.eval_by_depth}
iv\tAverage evaluation depth 
v\tAverage recursion depth 
vi\tTotal number of moves: {self.play_count - self.b}
'''
                self.game_trace(info=game_trace_info)

            self.eval_by_depth = {}

            if(self.player_turn == '◦'):
                self.current_state[x][y] = 1
                self.play_count += 1
            elif(self.player_turn == '•'):
                self.current_state[x][y] = 2
                self.play_count += 1
            else:
                print("OOPS, SOMETHING WENT WRONG")

            self.switch_player()


    def game_trace(self, player_x=None, player_o=None, info=None, initial=False):
        file_name = f'gameTrace-{self.n}{self.b}{self.s}{self.t}.txt'

        if initial:
            with open(file_name, 'w') as f:
                f.write(f'n={self.n} b={self.b} s={self.s} t={self.t}\n')
                f.write(f'\nPlayer 1: {player_x}\n')
                f.write(f'Player 2: {player_o}\n')
                # f.write(f'\n{self.get_board_state()}\n')

        else:
            with open(file_name, 'a') as f:
                f.write(f'\n{self.get_board_state()}\n')
                f.write(f'\n{info}\n')


def main():
    g = Game(n=4, b=2, d1=2, d2=3)
    g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
    #g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)
    # g.play(algo=Game.HUMAN,player_x=Game.HUMAN,player_o=Game.HUMAN)

if __name__ == "__main__":
    main()


