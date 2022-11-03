from sys import argv
import chess


class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board


if __name__ == '__main__':
    game = GameEngine(chess.Board())
