from math import log, sqrt, e, inf

import random
import chess


class Node:
    def __init__(self):
        self.state = chess.Board()
        self.action = ''
        self.children = set()
        self.parent = None
        self.child_visits = 0
        self.parent_visits = 0
        self.score = 0


class MCTS:
    def __init__(self, board: chess.Board, depth, color):
        self.board = board
        self.depth = depth
        self.AIcolor = color

    def select(self, current, color):
        best_child = None
        if color != self.AIcolor:
            max_ucb = -inf
            for i in current.children:
                ucb_i = self.ucb(i)
                if ucb_i > max_ucb:
                    max_ucb = ucb_i
                    best_child = i
        else:
            min_ucb = inf
            for i in current.children:
                ucb_i = self.ucb(i)
                if ucb_i < min_ucb:
                    min_ucb = ucb_i
                    best_child = i
        return best_child

    def expand(self, current, color):
        if len(current.children) == 0:
            return current

        best_child = self.select(current, color)
        if color != self.AIcolor:
            return self.expand(best_child, self.AIcolor)
        else:
            return self.expand(best_child, color)

    def simulate(self, current):

        if current.state.is_game_over():
            if current.state.result() == '1-0':
                if self.AIcolor == chess.BLACK:
                    return 1, current
                else:
                    return -1, current
            elif current.state.result() == '0-1':
                if self.AIcolor == chess.BLACK:
                    return -1, current
                else:
                    return 1, current
            else:
                return 0.5, current

        possible_moves = [current.state.san(i) for i in list(current.state.legal_moves)]

        for move in possible_moves:
            temp_state = chess.Board(current.state.fen())
            temp_state.push_san(move)
            child = Node()
            child.state = temp_state
            child.root = current
            current.children.add(child)
        rand_state = random.choice(list(current.children))

        return self.simulate(rand_state)

    def backpropagation(self, current, reward):
        current.child_visits += 1
        while current.parent is not None:
            current.score += reward
            current.parent_visits += 1
            current = current.root
        current.score += reward
        return current

    def init_round(self, possible_moves, current):
        states_moves = dict()
        for move in possible_moves:
            temp_state = chess.Board(current.state.fen())
            temp_state.push_san(move)

            res = Node()
            res.state = temp_state
            res.root = current
            current.children.add(res)

            states_moves[res] = move
        return states_moves

    def select_move(self, current, states_moves, color):
        selected_move = ''
        if color != self.AIcolor:
            max_ucb = -inf
            for i in current.children:
                ucb_i = self.ucb(i)
                if ucb_i > max_ucb:
                    max_ucb = ucb_i
                    selected_move = states_moves[i]
        else:
            min_ucb = inf
            for i in current.children:
                ucb_i = self.ucb(i)
                if ucb_i < min_ucb:
                    min_ucb = ucb_i
                    selected_move = states_moves[i]
        return selected_move

    def algorithm(self, depth, *args):
        current = Node()
        current.state = self.board
        player_color = chess.BLACK
        if self.AIcolor == chess.BLACK:
            player_color = chess.WHITE

        possible_moves = [current.state.san(i) for i in list(current.state.legal_moves)]
        states_moves = self.init_round(possible_moves, current)
        i = 0
        while i < depth:

            best_child = self.select(current, player_color)

            if player_color:
                ex_child = self.expand(best_child, self.AIcolor)
            else:
                ex_child = self.expand(best_child, player_color)

            reward, state = self.simulate(ex_child)
            current = self.backpropagation(state, reward)
            i += 1

        selected_move = self.select_move(current, states_moves, player_color)
        return selected_move

    def ucb(self, current):
        ucb = current.score + 2 * (
            sqrt(log(current.parent_visits + e + (10 ** -8)) / (current.child_visits + (10 ** -10))))
        return ucb
