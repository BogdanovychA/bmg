# -*- coding: utf-8 -*-

import asyncio
import uuid

import flet as ft
import flet_storage as fts

from games import next_number, tic_tac_toe
from routes import about, error404, root
from utils import elements
from utils import measurement_api as ga
from utils.config import APP_NAME, TEXT_SIZE


def build_main_view(page: ft.Page) -> ft.View:
    page.title = root.TITLE
    return ft.View(
        route=root.ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(root.TITLE),
            ft.Text(""),
            ft.Image(
                src="/icons/loading-animation.png",  # Посилання на картинку
                width=200,
                height=200,
            ),
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


async def main(page: ft.Page):
    page.title = root.TITLE
    page.theme_mode = ft.ThemeMode.DARK
    page.route = root.ROUTE

    async def route_change():

        page.run_task(
            ga.log_event,
            page.session.store.get("client_id"),
            str(page.platform.value),
            "route_change",
            page.route,
        )

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

    async def _init() -> None:
        """Стартова ініціалізація змінних"""

        async def __init_obj(name: str, default_value: object):
            """Допоміжна функція ініціалізації об'єктів,
            зчитування налаштувань з кешу"""

            is_contains = await ft.SharedPreferences().contains_key(
                f"{APP_NAME}.{name}"
            )
            if is_contains:
                value = await fts.load(name, APP_NAME)
            else:
                value = default_value
                await fts.save(name, APP_NAME, value)

            page.session.store.set(name, value)

        await __init_obj("client_id", str(uuid.uuid4()))

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await _init()

    await route_change()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
