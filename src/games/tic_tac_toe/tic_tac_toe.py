# -*- coding: utf-8 -*-

import flet as ft

from routes import about, author
from utils import elements
from utils.config import NUMBER_42, TEXT_SIZE
from utils.constants import GameMode
from utils.exceptions import GameAPIError

from . import abstract
from .constants import Symbol

ROUTE = "/tic-tac-toe"
TITLE = "Хрестики-нулики"
SUB_TITLE = "Обери за кого грати"

X_COLOR = ft.Colors.BLUE_ACCENT
O_COLOR = ft.Colors.RED_ACCENT

BOARD_BG_COLOR = ft.Colors.ON_SURFACE_VARIANT
CELL_SIZE = 50
CELL_RADIUS = 10

EMPTY_BOARD = [Symbol.EMPTY.value] * 9


def build_view(page: ft.Page) -> ft.View:
    """Побудова головного екрану гри"""

    def _set_ai() -> str:
        """Визначення символу, за який грає ШІ -- протилежний від людини"""

        return Symbol.O.value if player == Symbol.X.value else Symbol.X.value

    def _check_game_status() -> None:
        """Перевірка чи є переможець на дошці"""

        nonlocal game_finished

        if game_finished:  # Ігноруємо, якщо гра закінчилася
            return

        try:  # На випадок, якщо працюємо по API
            winner = client.check_winner(board)
            match winner:
                case Symbol.X.value | Symbol.O.value:
                    message_block.value = f"Перемога {winner}"
                    game_finished = True
                case Symbol.DRAW.value:
                    message_block.value = "Нічия"
                    game_finished = True

        except GameAPIError as e:
            message_block.value = str(e)
            game_finished = True

        message_block.update()

    def _ai_move(symbol) -> None:
        """Хід з використанням розрахунку кращого ходу.
        Використовується для ходу ШІ, або для людини (при
        натисканні кнопки автоматичного ходу)"""

        nonlocal game_finished

        try:  # На випадок, якщо працюємо по API
            ai_move = client.best_move(board, symbol)
            board[ai_move] = symbol
            board_layout.controls = _render_board()
            board_layout.update()

        except GameAPIError as e:
            message_block.value = str(e)
            game_finished = True

        _check_game_status()

    def _move_player(position: int, symbol: str) -> None:
        """Хід гравця. Винесено в окрему функцію для кращої читабельності коду"""

        board[position] = symbol
        board_layout.controls = _render_board()
        board_layout.update()
        _check_game_status()

    async def _click(event: ft.Event) -> None:
        """Обробка кліку на дошці або кнопки автоматичного ходу"""

        async def __run_ai() -> None:
            """Асинхронна обгортка для ходу ШІ"""

            _ai_move(ai)

        if game_finished:  # Ігноруємо, якщо гра закінчилася
            return

        if event.control.data == NUMBER_42:  # Якщо натиснули автоматичний хід
            _ai_move(player)
        else:  # Звичайний клік по дошці
            # Якщо натиснули по заповненому полю дошки -- ігноруємо
            if board[event.control.data] != Symbol.EMPTY.value:
                return
            _move_player(event.control.data, player)

        if game_finished:  # Ігноруємо код далі, якщо гра закінчилася
            return

        await __run_ai()

    def _switch(event: ft.Event) -> None:
        """Перемикання за кого грати X-O зі скиданням стану гри"""

        _init(event.control.selected[0])
        board_layout.controls = _render_board()
        event.page.update()

    def _rerun(event: ft.Event) -> None:
        """Скидання стану гри, без перемикання за кого грати"""

        _init(player)
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

    def _create_client() -> abstract.GameData:
        """
        Фабрика об'єктів.
        Створює клієнт залежно від режиму гри online/offline
        """

        game_mode = page.session.store.get("game_mode")

        if game_mode == GameMode.OFFLINE.value:
            return abstract.SelfData()

        return abstract.APIData()

    def _init(player_symbol: str) -> None:
        """Ініціалізація стану гри або його зміна при перемиканні"""
        nonlocal player, ai, board, game_finished
        board = EMPTY_BOARD.copy()
        player = player_symbol
        ai = _set_ai()
        game_finished = False
        message_block.value = "Зроби свій хід:"

        if player == Symbol.O.value:  # Якщо ШІ грає за X -- одразу робимо хід
            _ai_move(ai)

    board = []
    player = ""
    ai = ""
    game_finished = False
    message_block = ft.Text(size=TEXT_SIZE)

    client = _create_client()

    _init(Symbol.X.value)

    board_layout = ft.Column(
        controls=_render_board(),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.title = TITLE

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(SUB_TITLE, size=TEXT_SIZE),
            symbol_selector,
            ft.Text(""),
            message_block,
            ft.Text(""),
            board_layout,
            ft.Text(""),
            ft.Row(
                [
                    ft.IconButton(ft.Icons.REFRESH, on_click=_rerun),
                    ft.IconButton(ft.Icons.LIGHTBULB, on_click=_click, data=NUMBER_42),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            elements.back_button(page),
            ft.Row(
                controls=[
                    author.button(page),
                    about.button(page),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )
