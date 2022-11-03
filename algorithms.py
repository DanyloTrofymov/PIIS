import chess


def heuristic(board: chess.Board):
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999

    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    white = board.occupied_co[chess.WHITE]
    black = board.occupied_co[chess.BLACK]

    score = (chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
             3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
             3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
             5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
             9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens)))

    if board.turn:
        return score
    else:
        return -score

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
        a = alpha
        b = beta
        i = 1

        for move in board.legal_moves:
            board.push(move)
            t = -1 * (self.algorithm(depth - 1, -b, -alpha)[0])
            board.pop()
            if t > alpha and t < beta and i > 1 and depth < self.depth - 1:
                a = -1 * (self.algorithm(depth - 1, -beta, -t))
            a = max(a, t)
            if a >= beta:
                return a
            b = a + 1
            i = i + 1
        return a

