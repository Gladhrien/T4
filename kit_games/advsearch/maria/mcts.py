from __future__ import annotations

import random
from math import log, sqrt
from time import time
from typing import List, Tuple

x = list()

C = 1 / sqrt(2)
MAX_TIME = 3


class Nodo:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move

        self.children = []
        self.wins = 0
        self.visits = 0
        self.possible_moves = list() if state.is_terminal() else list(state.legal_moves())

    @staticmethod
    def UCB(nodo: Nodo):
        if nodo.visits == 0:
            return float('inf')
        if nodo.parent is None:
            raise ValueError("Nodo raiz nao tem pai")

        return nodo.wins/nodo.visits + 2*C*sqrt(2*log(nodo.parent.visits)/nodo.visits)

    def ucb_select(self):
        return max(self.children, key=Nodo.UCB)

    def add_child(self, move, state):
        n = Nodo(state, self, move)
        self.possible_moves.remove(move)
        self.children.append(n)

        return n
    
    def __lt__(self, other) -> bool:
        return self.UCB(self) < other.UCB(self)

def backpropagation(nodo: Nodo | None, result):
    while nodo != None:
        nodo.visits += 1
        if result == 1:
            nodo.wins += 1
        elif result == 0:
            nodo.wins += 0.5
        nodo = nodo.parent


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state.
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo retorna uma jogada ilegal
    # Remova-o e coloque a sua implementacao do MCTS

    start_time = time()
    raiz = Nodo(state)

    while time() - start_time < MAX_TIME:
        nodo = raiz

        while len(nodo.possible_moves) == 0 and len(nodo.children) != 0:
            nodo = nodo.ucb_select()

        while not nodo.state.is_terminal():
            move = random.choice(list(nodo.possible_moves))
            new_state = nodo.state.copy().next_state(move)
            next_node = Nodo(new_state, nodo, move)
            nodo.add_child(move, new_state)
            nodo = next_node

        winner = nodo.state.winner()
        win = 0
        if winner == state.player:
            win = 1

        backpropagation(nodo, win)

    return max(raiz.children).move
