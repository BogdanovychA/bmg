# -*- coding: utf-8 -*-

from enum import Enum

import flet as ft
import requests

from routes import about
from utils import elements
from utils.config import TEXT_SIZE

ROUTE = "/tic-tac-toe"
TITLE = "Хрестики-нулики"


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


def build_view(page: ft.Page) -> ft.View:

    def _init() -> None:
        pass

    def _click(event: ft.Event) -> None:

        board[event.control.data] = player
        board_layout.controls = _render_board()

        event.page.update()

    def _switch(event: ft.Event) -> None:
        nonlocal player, board
        player = event.control.selected[0]
        _rerun(event)

        # board = EMPTY_BOARD.copy()
        # board_layout.controls = _render_board()
        # event.page.update()

    def _rerun(event: ft.Event) -> None:

        nonlocal board
        board = EMPTY_BOARD.copy()
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

    board = EMPTY_BOARD.copy()
    player = Symbol.X.value
    page.title = TITLE

    board_layout = ft.Column(
        controls=_render_board(),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text("Обери за кого грати", size=TEXT_SIZE),
            ft.Row(
                [
                    symbol_selector,
                    ft.IconButton(ft.Icons.REFRESH, on_click=_rerun),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            board_layout,
            ft.Text(""),
            ft.Text(""),
            elements.back_button(page),
            about.button(page),
        ],
    )
