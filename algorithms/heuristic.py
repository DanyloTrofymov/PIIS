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