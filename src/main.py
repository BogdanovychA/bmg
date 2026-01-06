# -*- coding: utf-8 -*-

import asyncio

import flet as ft

from games import next_number, tic_tac_toe
from routes import about, error404, root
from utils import elements
from utils.config import TEXT_SIZE


def build_main_view(page: ft.Page) -> ft.View:
    page.title = root.TITLE
    return ft.View(
        route=root.ROUTE,
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
            ft.Button(
                tic_tac_toe.TITLE,
                on_click=lambda: asyncio.create_task(
                    page.push_route(tic_tac_toe.ROUTE)
                ),
            ),
            ft.Text(""),
            about.button(page),
        ],
    )


def main(page: ft.Page):
    page.title = root.TITLE
    page.theme_mode = ft.ThemeMode.DARK
    page.route = root.ROUTE

    def route_change():
        page.views.clear()
        page.views.append(build_main_view(page))
        match page.route:
            case next_number.ROUTE:
                page.views.append(next_number.build_view(page))
            case tic_tac_toe.ROUTE:
                page.views.append(tic_tac_toe.build_view(page))
            case about.ROUTE:
                page.views.append(about.build_view(page))
            case _:
                if page.route != root.ROUTE:
                    page.views.append(error404.build_view(page))

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
    ft.run(main, assets_dir="assets")
