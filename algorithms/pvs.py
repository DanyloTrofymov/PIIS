import chess
from algorithms.heuristic import heuristic


class PVS:
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
            score = -1 * (self.getPVScore(self.board, depth - 1, alpha, beta))
            self.board.pop()

            if score > bestScore:
                bestScore = score

        return bestScore

    def getPVScore(self, board, depth, alpha, beta):
        if depth == 0:
            return heuristic(board)
        bSearchPv = True
        for move in board.legal_moves:
            board.push(move)
            if bSearchPv:
                score = -1 * (self.algorithm(depth - 1, -beta, -alpha))
            else:
                score = -1 * (self.algorithm(depth - 1, -alpha - 1, -alpha))
                if score > alpha and score < beta:
                    score = -1 * (self.algorithm(depth - 1, -beta, -alpha))
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
                bSearchPv = False
        return alpha
