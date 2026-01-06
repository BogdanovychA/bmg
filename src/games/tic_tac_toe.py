# -*- coding: utf-8 -*-

import flet as ft
import requests

from routes import about
from utils import elements
from utils.config import FORM_BG_COLOR, FORM_BORDER_COLOR, TEXT_SIZE

ROUTE = "/tic-tac-toe"
TITLE = "Хрестики-нулики"


def build_view(page: ft.Page) -> ft.View:

    def _rerun(event: ft.Event) -> None:
        event.page.update()

    symbol_block = ft.Dropdown(
        label="Обери за кого грати",
        label_style=ft.TextStyle(size=TEXT_SIZE),
        value="X",
        options=[
            ft.DropdownOption(key="X", text="X"),
            ft.DropdownOption(key="O", text="0"),
        ],
        on_select=_rerun,
    )

    page.title = TITLE
    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text(""),
            symbol_block,
            ft.Text(""),
            ft.Text(""),
            elements.back_button(page),
            about.button(page),
        ],
    )
