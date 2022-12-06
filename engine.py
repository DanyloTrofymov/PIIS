import chess

from algorithms.negamax import Negamax
from algorithms.negascout import NegaScout
from algorithms.pvs import PVS
from algorithms.mcts import MCTS
class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def humanMove(self):
        print("You can choose on of that moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        self.board.push_san(play)

    def AIMove(self, AI, algo):
        bestMove = chess.Move.null
        bestScore = float('-inf')
        if algo != "mcts":
            for move in AI.board.legal_moves:
                AI.board.push(move)
                score = -1 * (AI.algorithm(AI.depth, float('-inf'), float('inf')))
                AI.board.pop()

                if score > bestScore:
                    bestScore = score
                    bestMove = move
            print('Best move is: ', bestMove, '\n')
            self.board.push(bestMove)
        else:
            bestMove = AI.algorithm(AI.depth)
            print('Best move is: ', bestMove, '\n')
            self.board.push_san(bestMove)

        return

    def start(self, algo, depth, color):
        if color == "white":
            aiColor = chess.BLACK
        else:
            aiColor = chess.WHITE


        if algo == "negamax":
            AI = Negamax(self.board, aiColor, depth)
        if algo == "negascout":
            AI = NegaScout(self.board, aiColor, depth)
        if algo == "pvs":
            AI = PVS(self.board, aiColor, depth)
        if algo == "mcts":
            AI = MCTS(self.board, aiColor, depth)


        turn = chess.WHITE
        while not self.board.is_checkmate():
            print(self.board)
            if turn != aiColor:
                print('\nWhite move\n')
                self.humanMove()
                turn = chess.BLACK
                continue
            if turn == aiColor:
                print('\nBlack move\n')
                self.AIMove(AI, algo)
                turn = chess.WHITE
                continue
        print(self.board)
        print("WHITE WINS" if turn == chess.BLACK else "BLACK WINS")
        return
