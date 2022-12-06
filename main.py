from sys import argv
from engine import GameEngine
import chess

if __name__ == '__main__':
    algo = argv[1].lower()
    algos = {"negamax", "negascout", "pvs", "mcts"}
    if algo not in algos:
        print("You need to set algorythm as a first argument (\"negamax\", \"negascout\", \"pvs\" or \"mcts\")")
        exit()

    try:
        depth = int(argv[2])
    except:
        print("You need to set integer algorythm`s depth(iterations for mcts) as a second argument")
        exit()

    color = argv[3].lower()
    if color != "white" and algo != "black":
        print("You need to set your starting color as a first argument (\"white\" or \"black\")")
        exit()

    print("Algorithm: ", algo)
    print("Depth(iterations for mcts): ", depth)
    print("You starting as ", color)

    game = GameEngine(chess.Board())
    game.start(algo, depth, color)

