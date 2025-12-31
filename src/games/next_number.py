# -*- coding: utf-8 -*-

import flet as ft
import elements

ROUTE = "/next-number"
TITLE = "Вгадай наступне число"

def build_view(page: ft.Page) -> ft.View:
    return ft.View(
                route=ROUTE,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.AppBar(title=ft.Text(TITLE), center_title=True),
                    elements.back_button(page),
                ],
            )
