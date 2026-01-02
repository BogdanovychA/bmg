# -*- coding: utf-8 -*-

import flet as ft

from utils import elements
from utils.config import BASE_URL, TEXT_SIZE

TITLE = "Про автора"
ROUTE = BASE_URL + "/about"


def build_view(page: ft.Page) -> ft.View:

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text("Андрій БОГДАНОВИЧ", size=TEXT_SIZE),
            ft.Text(""),
            ft.Image(
                src="/images/bogdanovych.jpg",  # Посилання на картинку
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                size=TEXT_SIZE,
                spans=[
                    elements.link("Домашня сторінка", "https://www.bogdanovych.org"),
                    ft.TextSpan("\n"),
                    elements.link("GitHub", "https://github.com/BogdanovychA/"),
                ],
            ),
            ft.Text(""),
            elements.back_button(page),
        ],
    )
