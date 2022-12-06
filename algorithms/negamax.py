import chess
from algorithms.heuristic import heuristic


class Negamax:
    def __init__(self, board: chess.Board, depth, color):
        self.board = board
        self.depth = depth
        self.color = color

    def algorithm(self, depth, *args):
        if (depth == 0):
            return heuristic(self.board)

        bestScore = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1 * (self.algorithm(depth - 1))
            if score > bestScore:
                bestScore = score
            self.board.pop()
        return bestScore
