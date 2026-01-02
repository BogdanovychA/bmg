# -*- coding: utf-8 -*-

import flet as ft

from utils import elements
from utils.config import TEXT_SIZE

TITLE = "Про автора"
ROUTE = "/about"


def build_view(page: ft.Page) -> ft.View:

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text("Андрій БОГДАНОВИЧ", size=TEXT_SIZE),
            ft.Text(""),
            ft.Text(
                size=TEXT_SIZE,
                spans=[
                    elements.link("www.bogdanovych.org", "https://www.bogdanovych.org"),
                ],
            ),
            ft.Text(""),
            elements.back_button(page),
        ],
    )
