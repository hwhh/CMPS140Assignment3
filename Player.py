import numpy as np

# (starting coordinate, direction)
N = ([(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)], (-1, 0))
E = ([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)], (0, 1))
NE = ([(3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3)], (-1, 1))
SE = ([(5, 3), (5, 4), (5, 5), (5, 6), (4, 6), (3, 6)], (-1, -1))

scores = [[3, 4, 5, 7, 5, 4, 3],
          [4, 6, 8, 10, 8, 6, 4],
          [5, 8, 11, 13, 11, 8, 5],
          [5, 8, 11, 13, 11, 8, 5],
          [4, 6, 8, 10, 8, 6, 4],
          [3, 4, 5, 7, 5, 4, 3]]


class AIPlayer:

    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.lines = self.create_lines(self)

    @staticmethod
    def switch_player(player):
        if player == 1:
            return 2
        else:
            return 1

    @staticmethod
    def generate_moves(board, player):
        boards = []
        transposed_board = list(map(list, zip(*board)))
        for c1, col in enumerate(transposed_board):
            temp_board = transposed_board[:]
            for c2, value in enumerate(col):
                if value > 0 and c2 != 0:
                    new_col = col[:]
                    new_col[c2 - 1] = player
                    temp_board[c1] = new_col
                    boards.append(list(map(list, zip(*temp_board))))
                    break
                elif c2 == len(col) - 1:
                    new_col = col[:]
                    new_col[c2] = player
                    temp_board[c1] = new_col
                    boards.append(list(map(list, zip(*temp_board))))
        return boards

    @staticmethod
    def create_lines(self):
        lines = []
        for x in N[0]:
            lines.append(self.create_line(x[0], x[1], N[1][0], N[1][1]))
        for x in E[0]:
            lines.append(self.create_line(x[0], x[1], E[1][0], E[1][1]))
        for x in NE[0]:
            lines.append(self.create_line(x[0], x[1], NE[1][0], NE[1][1]))
        for x in SE[0]:
            lines.append(self.create_line(x[0], x[1], SE[1][0], SE[1][1]))
        return lines

    @staticmethod
    def create_line(x, y, d1, d2):
        line = []
        while 0 <= x <= 5 and 0 <= y <= 6:
            line.append((x, y))
            x += d1
            y += d2
        return line

    @staticmethod
    def check_empty(line, board):
        for pos in line:
            if board[pos[0]][pos[1]] != 0:
                return False
        return True

    def get_alpha_beta_move(self, board):
        return self.alpha_beta(board, 3, -10000, 100000, self.player_number)

    def alpha_beta(self, board, depth, alpha, beta, player):
        if depth == 0:
            return self.evaluation_function(board, depth)
        elif player == 1:
            v = -100000
            for child in self.generate_moves(board, player):
                v = max(v, self.alpha_beta(child, depth - 1, alpha, beta, self.switch_player(player)))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return v
        elif player == 2:
            v = 100000
            for child in self.generate_moves(board, player):
                v = min(v, self.alpha_beta(child, depth - 1, alpha, beta, self.switch_player(player)))
                alpha = min(beta, v)
                if beta <= alpha:
                    break
            return v

    def get_expectimax_move(self, board):
        # first look at the
        self.generate_moves(board, self.player_number)
        return 0


    def evaluation_function(self, board, level):
        # check the distance from the current state to board state
        score = 0
        for line in self.lines:
            # if not self.check_empty(line, board): #optermistation
            score += self.score_line(line, board)

    def score_line(self, line, board):
        line_score = 0
        for start in range(0, len(line) - 3):
            line_score = self.score_partial_line(line[start:start + 4], board)
        return line_score

    def score_partial_line(self, partial_line, board):
        partial_line_score = 0
        for (x, y) in partial_line:
            if board[x][y] == self.player_number:
                partial_line_score += 1 + scores[x][y]
            elif board[x][y] != self.player_number and board[x][y] > 0:
                return -scores[x][y]  # TODO
        if partial_line_score == 4:
            return partial_line_score ** 4
        elif partial_line_score == 3:
            return partial_line_score ** 3
        elif partial_line_score == 2:
            return partial_line_score ** 2
        else:
            return partial_line_score


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move
