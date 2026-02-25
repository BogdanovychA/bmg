# -*- coding: utf-8 -*-
# from __future__ import annotations

import math

from .constants import Symbol

WIN_POSITIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def check_winner(board: list[str]) -> str | None:
    """Перевірка переможця"""

    for combo in WIN_POSITIONS:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != Symbol.EMPTY:
            return board[a]
    if Symbol.EMPTY not in board:
        return Symbol.DRAW
    return None


def minimax(
    board: list[str],
    is_max_turn: bool,
    max_player_symbol: str,
    min_player_symbol: str,
) -> int:
    """Побудова дерева ходів"""

    winner = check_winner(board)

    if winner == max_player_symbol:
        return 1
    if winner == min_player_symbol:
        return -1
    if winner == Symbol.DRAW:
        return 0

    if is_max_turn:
        best_score = -math.inf
        for i in range(9):
            if board[i] == Symbol.EMPTY:
                board[i] = max_player_symbol
                score = minimax(board, False, max_player_symbol, min_player_symbol)
                board[i] = Symbol.EMPTY
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == Symbol.EMPTY:
                board[i] = min_player_symbol
                score = minimax(board, True, max_player_symbol, min_player_symbol)
                board[i] = Symbol.EMPTY
                best_score = min(best_score, score)
        return best_score


def best_move(board: list, max_player_symbol: str, min_player_symbol: str) -> int:
    """Вибір кращого ходу"""
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == Symbol.EMPTY:
            board[i] = max_player_symbol
            score = minimax(board, False, max_player_symbol, min_player_symbol)
            board[i] = Symbol.EMPTY
            if score > best_score:
                best_score = score
                move = i

    if move is None:
        raise ValueError("Немає доступних ходів на дошці")

    return move
