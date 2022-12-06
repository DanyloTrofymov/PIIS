import chess
from algorithms.heuristic import heuristic


class NegaScout:
    def __init__(self, board: chess.Board, depth, color):
        self.board = board
        self.depth = depth
        self.color = color

    def algorithm(self, depth, alpha, beta):
        bestScore = float('-inf')
        if (depth == 0):
            return heuristic(self.board)

        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1 * (self.getMaxScore(self.board, depth - 1, alpha, beta))
            self.board.pop()

            if score > bestScore:
                bestScore = score

        return bestScore

    def getMaxScore(self, board, depth, alpha, beta):
        if (depth == 0):
            return heuristic(board)
        i = 1

        for move in board.legal_moves:
            board.push(move)
            score = -1 * (self.algorithm(depth - 1, -beta, -alpha)[0])
            board.pop()
            if score > alpha and score < beta and i > 1 and depth < self.depth - 1:
                alpha = -1 * (self.algorithm(depth - 1, -beta, -score))
            alpha = max(alpha, score)
            if alpha >= beta:
                return alpha
            beta = alpha + 1
            i = i + 1
        return alpha
