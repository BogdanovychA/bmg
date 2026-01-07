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
CELL_RADIUS = 15


def build_view(page: ft.Page) -> ft.View:

    def _rerun(event: ft.Event) -> None:
        event.page.update()

    def _cell(content: ft.Icon | None) -> ft.Container:
        return ft.Container(
            content=content,
            data=Symbol.EMPTY.value,
            width=CELL_SIZE,
            height=CELL_SIZE,
            bgcolor=BOARD_BG_COLOR,
            border_radius=CELL_RADIUS,
            alignment=ft.Alignment.CENTER,
            ink=True,
            # animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
        )

    x_icon = ft.Icon(ft.Icons.CLOSE, color=X_COLOR)
    o_icon = ft.Icon(ft.Icons.CIRCLE_OUTLINED, color=O_COLOR)

    symbol_selector = ft.SegmentedButton(
        selected=[Symbol.X.value],
        allow_empty_selection=False,
        allow_multiple_selection=False,
        show_selected_icon=False,
        segments=[
            ft.Segment(
                value=Symbol.X.value,
                label=x_icon,
            ),
            ft.Segment(
                value=Symbol.O.value,
                label=o_icon,
            ),
        ],
        on_change=_rerun,
    )

    game_board = ft.Column(
        [
            ft.Row(
                [_cell(x_icon) for _ in range(3)], alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [_cell(None) for _ in range(3)], alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [_cell(o_icon) for _ in range(3)], alignment=ft.MainAxisAlignment.CENTER
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    page.title = TITLE

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text("Обери за кого грати", size=TEXT_SIZE),
            symbol_selector,
            ft.Text(""),
            game_board,
            ft.Text(""),
            elements.back_button(page),
            about.button(page),
        ],
    )
