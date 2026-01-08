# -*- coding: utf-8 -*-

from enum import Enum

import flet as ft
import requests

from routes import about
from utils import elements
from utils.config import API_URL, NUMBER_42, TEXT_SIZE

ROUTE = "/tic-tac-toe"
TITLE = "Хрестики-нулики"
SUB_TITLE = "Обери за кого грати"


class Symbol(Enum):
    X = "X"
    O = "O"
    EMPTY = "none"


X_COLOR = ft.Colors.BLUE_ACCENT
O_COLOR = ft.Colors.RED_ACCENT

BOARD_BG_COLOR = ft.Colors.ON_SURFACE_VARIANT
CELL_SIZE = 50
CELL_RADIUS = 10

EMPTY_BOARD = [Symbol.EMPTY.value] * 9

BASE_API_URL = f"{API_URL}/ttt"
API_HEADERS = {'accept': 'application/json', 'Content-Type': 'application/json'}
ERROR_TEXT = "Сталася помилка при запиті до API"


def check_winner(board: list) -> str:

    target_url = f"{BASE_API_URL}/check"
    headers = API_HEADERS
    payload = board

    try:
        response = requests.post(target_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["result"]

    except (requests.exceptions.RequestException, Exception) as e:
        text = f"{ERROR_TEXT}: {e}"
        print(text)
        return text


def best_move(board: list, player: str) -> int | str:

    target_url = f"{BASE_API_URL}/move"
    headers = API_HEADERS
    payload = {"board": board, "max_player_symbol": player}

    try:
        response = requests.post(
            target_url,
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    except (requests.exceptions.RequestException, Exception) as e:
        text = f"{ERROR_TEXT}: {e}"
        print(text)
        return text


def build_view(page: ft.Page) -> ft.View:

    def _set_ai() -> str:
        return Symbol.O.value if player == Symbol.X.value else Symbol.X.value

    def _check_game_status() -> None:

        nonlocal game_finished

        winner = check_winner(board)
        match winner:
            case Symbol.X.value | Symbol.O.value:
                message_block.value = f"Перемога {winner}"
                game_finished = True
            case "draw":
                message_block.value = "Нічия"
                game_finished = True

        if ERROR_TEXT in winner:
            message_block.value = winner
            game_finished = True

        message_block.update()

    def _ai_move(symbol) -> None:

        nonlocal game_finished

        ai_move = best_move(board, symbol)

        if isinstance(ai_move, str):  # Якщо помилка API
            message_block.value = ai_move
            message_block.update()
            game_finished = True
        elif isinstance(ai_move, int):  # Основний робочий блок
            board[ai_move] = symbol
            board_layout.controls = _render_board()
            board_layout.update()
        else:  # Інша непередбачувана помилка (вірогідність дуже низька)
            print("Непередбачуваний тип")

        _check_game_status()

    def _move_player(position: int, symbol: str) -> None:

        board[position] = symbol
        board_layout.controls = _render_board()
        board_layout.update()
        _check_game_status()

    def _click(event: ft.Event) -> None:

        if game_finished:
            return

        if event.control.data == NUMBER_42:
            _ai_move(player)
        else:
            if board[event.control.data] != Symbol.EMPTY.value:
                return
            _move_player(event.control.data, player)

        if game_finished:
            return

        _ai_move(ai)

    def _switch(event: ft.Event) -> None:

        _init(event.control.selected[0])
        board_layout.controls = _render_board()
        event.page.update()

    def _rerun(event: ft.Event) -> None:

        _init(player)
        board_layout.controls = _render_board()
        event.page.update()

    def _icon(icon: str) -> ft.Icon | None:

        match icon:
            case Symbol.X.value:
                return ft.Icon(ft.Icons.CLOSE, color=X_COLOR)
            case Symbol.O.value:
                return ft.Icon(ft.Icons.CIRCLE_OUTLINED, color=O_COLOR)
            case Symbol.EMPTY.value | _:
                return None

    def _cell(content: ft.Icon, data: int) -> ft.Container:

        return ft.Container(
            content=content,
            data=data,
            width=CELL_SIZE,
            height=CELL_SIZE,
            bgcolor=BOARD_BG_COLOR,
            border_radius=CELL_RADIUS,
            alignment=ft.Alignment.CENTER,
            ink=True,
            on_click=_click,
        )

    def _render_board() -> list:
        return [
            ft.Row(
                [_cell(_icon(board[i]), i) for i in range(start, start + 3)],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            for start in range(0, 9, 3)
        ]

    symbol_selector = ft.SegmentedButton(
        selected=[Symbol.X.value],
        allow_empty_selection=False,
        allow_multiple_selection=False,
        show_selected_icon=False,
        segments=[
            ft.Segment(
                value=Symbol.X.value,
                label=_icon(Symbol.X.value),
            ),
            ft.Segment(
                value=Symbol.O.value,
                label=_icon(Symbol.O.value),
            ),
        ],
        on_change=_switch,
    )

    def _init(player_symbol: str) -> None:

        nonlocal player, ai, board, game_finished
        board = EMPTY_BOARD.copy()
        player = player_symbol
        ai = _set_ai()
        game_finished = False
        message_block.value = ""

        if player == Symbol.O.value:
            _ai_move(ai)

    board = []
    player = ""
    ai = ""
    game_finished = False

    message_block = ft.Text(size=TEXT_SIZE)

    _init(Symbol.X.value)

    page.title = TITLE

    board_layout = ft.Column(
        controls=_render_board(),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text(SUB_TITLE, size=TEXT_SIZE),
            ft.Row(
                [
                    symbol_selector,
                    ft.IconButton(ft.Icons.REFRESH, on_click=_rerun),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            message_block,
            ft.Text(""),
            board_layout,
            ft.Text(""),
            ft.Button("Автохід", on_click=_click, data=NUMBER_42),
            ft.Text(""),
            elements.back_button(page),
            about.button(page),
        ],
    )
