# -*- coding: utf-8 -*-

from enum import Enum

import flet as ft
import httpx

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


async def check_winner(board: list) -> str:
    """Звернення до API для перевірки чи є переможець на дошці"""

    target_url = f"{BASE_API_URL}/check"
    headers = API_HEADERS
    payload = board

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                target_url, headers=headers, json=payload, timeout=10.0
            )

            response.raise_for_status()
            return response.json()["result"]

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        text = f"{ERROR_TEXT}: {e}"
        print(text)
        return text
    except Exception as e:
        text = f"Непередбачувана помилка: {e}"
        print(text)
        return text


async def best_move(board: list, player: str) -> int | str:
    """Звернення до API для обрахування кращого ходу"""

    target_url = f"{BASE_API_URL}/move"
    headers = API_HEADERS
    payload = {"board": board, "max_player_symbol": player}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                target_url, headers=headers, json=payload, timeout=15.0
            )

            response.raise_for_status()
            return response.json()

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        text = f"{ERROR_TEXT}: {e}"
        print(text)
        return text
    except Exception as e:
        text = f"Непередбачувана помилка: {e}"
        print(text)
        return text


async def build_view(page: ft.Page) -> ft.View:
    """Побудова головного екрану гри"""

    def _set_ai() -> str:
        """Визначення символу, за який грає ШІ -- протилежний від людини"""

        return Symbol.O.value if player == Symbol.X.value else Symbol.X.value

    async def _check_game_status() -> None:
        """Перевірка чи є переможець на дошці"""

        nonlocal game_finished

        if game_finished:  # Ігноруємо, якщо гра закінчилася
            return

        winner = await check_winner(board)
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

    async def _ai_move(symbol) -> None:
        """Хід з використанням розрахунку кращого ходу.
        Використовується для ходу ШІ, або для людини (при
        натисканні кнопки автоматичного ходу)"""

        nonlocal game_finished

        ai_move = await best_move(board, symbol)

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

        await _check_game_status()

    async def _move_player(position: int, symbol: str) -> None:
        """Хід гравця. Винесено в окрему функцію для кращої читабельності коду"""

        board[position] = symbol
        board_layout.controls = _render_board()
        board_layout.update()
        await _check_game_status()

    async def _click(event: ft.Event) -> None:
        """Обробка кліку на дошці або кнопки автоматичного ходу"""

        # async def __run_ai() -> None:
        #     """Асинхронна обгортка для ходу ШІ"""
        #     _ai_move(ai)

        if game_finished:  # Ігноруємо, якщо гра закінчилася
            return

        if event.control.data == NUMBER_42:  # Якщо натиснули автоматичний хід
            await _ai_move(player)
        else:  # Звичайний клік по дошці
            # Якщо натиснули по заповненому полю дошки -- ігноруємо
            if board[event.control.data] != Symbol.EMPTY.value:
                return
            await _move_player(event.control.data, player)

        if game_finished:  # Ігноруємо код далі, якщо гра закінчилася
            return

        await _ai_move(ai)
        # page.run_task(__run_ai)

    async def _switch(event: ft.Event) -> None:
        """Перемикання за кого грати X-O зі скиданням стану гри"""

        await _init(event.control.selected[0])
        board_layout.controls = _render_board()
        event.page.update()

    async def _rerun(event: ft.Event) -> None:
        """Скидання стану гри, без перемикання за кого грати"""

        await _init(player)
        board_layout.controls = _render_board()
        event.page.update()

    def _icon(icon: str) -> ft.Icon | None:
        """Фабрика об'єктів іконок - залежно від використаного символу"""

        match icon:
            case Symbol.X.value:
                return ft.Icon(ft.Icons.CLOSE, color=X_COLOR)
            case Symbol.O.value:
                return ft.Icon(ft.Icons.CIRCLE_OUTLINED, color=O_COLOR)
            case Symbol.EMPTY.value | _:
                return None

    def _cell(content: ft.Icon, data: int) -> ft.Container:
        """Фабрика комірок дошки, залежно від використаної іконки та позиції в списку"""
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
        """Рендерінг дошки"""

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

    async def _init(player_symbol: str) -> None:
        """Ініціалізація стану гри або його зміна при перемиканні"""
        nonlocal player, ai, board, game_finished
        board = EMPTY_BOARD.copy()
        player = player_symbol
        ai = _set_ai()
        game_finished = False
        message_block.value = "Зроби свій хід:"

        if player == Symbol.O.value:  # Якщо ШІ грає за X -- одразу робимо хід
            await _ai_move(ai)

    board = []
    player = ""
    ai = ""
    game_finished = False
    message_block = ft.Text(size=TEXT_SIZE)

    await _init(Symbol.X.value)

    board_layout = ft.Column(
        controls=_render_board(),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.title = TITLE

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
