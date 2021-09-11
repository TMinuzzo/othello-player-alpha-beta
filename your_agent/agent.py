from typing import Tuple
from board import Board
from copy import deepcopy

INFINITY = float('inf')


def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """

    game_strategy = GameStrategy(4, the_board, color)
    return game_strategy.alpha_beta_min_max()



class GameStrategy:

    def __init__(self, depth_limit: int, board: Board, color: str):
        """
        Class responsible for the game strategy, that uses an Alpha Beta algorithm with a configurable maximum depth
    
        :param depth_limit: int, this is an important factor, the higher the value, the longer it will take to compute the better the move
        :param board: Board
        :param color: the color that will be used to play
        """
        self.depth_limit = depth_limit 
        self.board = board
        self.color = color
        self.opponent_color = self._opponent_color(color)
    
    def alpha_beta_min_max(self) -> Tuple[int, int]:
        """
        The main method of the strategy. Based on the maximum depth, it will try to compute the best play for it, and the worst for the oponent given the legal moves
        every time the depth is decreased
        :return: final_move, a tuple with the best play found
        """

        legal_moves = self.board.legal_moves(self.color)
        final_move = legal_moves[0]

        best_score = -INFINITY

        for move in legal_moves:
            test_board = deepcopy(self.board) # creates a copy of the board to test the plays on it
            test_board.process_move(move, self.color)
            score = self._min_score(test_board, self.opponent_color, -INFINITY, INFINITY, self.depth_limit-1)

            if score > best_score:
                best_score = score
                final_move = move

        return final_move


    def _min_score(self, board, color, alpha, beta, depth) -> int:
        """
        The MIN play, receives the initial score as + Infinite and computes the max score play for the opponent
        """
        if depth == 0:
            return self._cost_compute(board, color)

        best_score = INFINITY

        for move in board.legal_moves(color):
            test_board = deepcopy(board)
            test_board.process_move(move, color)

            score = self._max_score(test_board, self._opponent_color(color), alpha, beta, depth-1)

            if score < best_score:
                best_score = score
            
            if best_score <= alpha:
                return best_score

            beta = min(beta, best_score)

        return best_score


    def _max_score(self, board, color, alpha, beta, depth) -> int:
        """
        The MIN play, receives the initial score as - Infinite and computes the min score play for the opponent
        """
        if depth == 0:
            return self._cost_compute(board, color)

        best_score = -INFINITY

        for move in board.legal_moves(color):
            test_board = deepcopy(board)
            test_board.process_move(move, color)

            score = self._min_score(test_board, self._opponent_color(color), alpha, beta, depth-1)

            if score > best_score:
                best_score = score
            
            if best_score >= beta:
                return best_score

            alpha = max(alpha, best_score)

        return best_score
   

    def _cost_compute(self, board: Board, color: str) -> int:
        """
        A simple strategy for computing the score, using the number of pieces the play will give based on the current board
        """
        oponent_pieces = self._count_pieces(board, self._opponent_color(color))
        my_pieces = self._count_pieces(board, color)

        score = my_pieces - oponent_pieces
        return score


    def _count_pieces(self, board: Board, color: str) -> int:
        """
        Compute the number of pieces on the board given a color
        """
        count = 0
        for j in range(8):
            for i in range(8):
                if board.tiles[i][j]==color:
                    count += 1
        return count
    

    def _opponent_color(self, color):
        return 'B' if color == 'W' else 'W'