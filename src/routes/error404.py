# -*- coding: utf-8 -*-

import flet as ft

from utils import elements

TITLE = "Сторінка не знайдена"
ROUTE = "/404"


def build_view(page: ft.Page) -> ft.View:

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text(""),
            ft.Text(""),
            elements.back_button(page),
        ],
    )
