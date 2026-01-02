# -*- coding: utf-8 -*-

import asyncio

import flet as ft

import games.next_number as next_number
from routs import root
from utils import elements
from utils.config import TEXT_SIZE


def build_main_view(page: ft.Page) -> ft.View:
    return ft.View(
        route=root.ROUTE,
        # vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(root.TITLE),
            ft.Text(""),
            ft.Text("Обери гру, в яку хочеш зіграти:", size=TEXT_SIZE),
            ft.Text(""),
            ft.Button(
                next_number.TITLE,
                on_click=lambda: asyncio.create_task(
                    page.push_route(next_number.ROUTE)
                ),
            ),
        ],
    )


def main(page: ft.Page):
    page.title = root.TITLE
    page.theme_mode = ft.ThemeMode.DARK

    def route_change():
        page.views.clear()
        page.views.append(build_main_view(page))
        match page.route:
            case next_number.ROUTE:
                page.views.append(next_number.build_view(page))
                # if page.route == next_number.ROUTE:
        #     page.views.append(next_number.build_view(page))
        page.update()

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


if __name__ == "__main__":
    ft.run(main)
