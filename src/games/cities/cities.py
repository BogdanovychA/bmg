# -*- coding: utf-8 -*-

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Generator

if TYPE_CHECKING:
    from flet_storage import FletStorage

import flet as ft

from routes import about, author
from utils import elements
from utils.config import FORM_BG_COLOR, FORM_BORDER_COLOR, TEXT_SIZE

from . import abstract, logic
from .utils import make_used_string

ROUTE = "/cities"
TITLE = "Міста світу"
SUB_TITLE = "Називай міста на останню літеру"


class GameClient:
    def __init__(
        self,
        game: Generator[logic.Event, logic.Input, logic.Event],
    ) -> None:
        self.game = game
        self.event = next(game)


async def build_view(page: ft.Page, storage: FletStorage) -> ft.View:

    async def _create_client() -> GameClient:

        cities_cache = await storage.get_or_default("cities_cache", None)

        if cities_cache is None:

            return GameClient(
                game=logic.main(all_cities=abstract.SelfData().get_cities())
                # game=logic.main(all_cities=abstract.TestData().get_cities())
            )

        else:
            return GameClient(
                game=logic.main(
                    all_cities=abstract.SelfData().get_cities(),
                    # all_cities=abstract.TestData().get_cities(),
                    restore=True,
                    **cities_cache,
                )
            )

    async def _save_cache() -> None:

        cities_cache = {
            "used_cities": client.event.used_cities,
            "last_ai_city": client.event.city,
        }
        await storage.set("cities_cache", cities_cache)

    async def _ok(event: ft.Event) -> None:

        if not client.game:
            return

        if not answer_block.value:
            return

        try:
            client.event = client.game.send(logic.Input(city=answer_block.value))

            if not client.event.error:

                await _save_cache()

                city_block.value = client.event.city
                message_block.value = client.event.message
                answer_block.value = ""
                used_block.value = make_used_string(client.event.used_cities)
            else:
                message_block.value = client.event.message

        except StopIteration as e:
            await storage.remove("cities_cache")
            client.game = None
            client.event = e.value

            if hasattr(client.event, 'game_over'):
                if client.event.game_over:
                    sub_title.value = ""
                    city_block.value = (
                        client.event.message
                    )  # Неявне використання city_block :)
                    message_block.value = "Перезапусти гру".upper()
                    answer_block.value = ""
                    used_block.value = make_used_string(client.event.used_cities)
                else:
                    pass  # На майбутнє :)

            else:
                msg = "StopIteration. Непередбачувана помилка"
                sub_title.value = msg
                city_block.value = msg
                message_block.value = msg
                answer_block.value = msg
                used_block.value = msg

        event.page.update()

    def _answer(event: ft.Event) -> None:

        if not client.game:
            return

        answer_block.value = random.choice(list(client.event.available_cities)).title()
        event.page.update()

    async def _rerun(event: ft.Event) -> None:

        nonlocal client

        await storage.remove("cities_cache")

        client = await _create_client()

        await _save_cache()

        sub_title.value = SUB_TITLE
        city_block.value = client.event.city
        message_block.value = client.event.message
        answer_block.value = ""
        used_block.value = make_used_string(client.event.used_cities)

        event.page.update()

    page.title = TITLE

    client = await _create_client()

    await _save_cache()

    sub_title = ft.Text(SUB_TITLE, size=TEXT_SIZE)
    city_block = ft.Text(client.event.city, size=TEXT_SIZE)
    message_block = ft.Text(client.event.message, size=TEXT_SIZE)
    answer_block = ft.TextField(
        value="", width=250, bgcolor=FORM_BG_COLOR, border_color=FORM_BORDER_COLOR
    )
    used_block = ft.Text(make_used_string(client.event.used_cities))

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            sub_title,
            ft.Text(""),
            city_block,
            ft.Text(""),
            ft.Row(
                [
                    answer_block,
                    ft.IconButton(ft.Icons.DONE_OUTLINE, on_click=_ok),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            message_block,
            ft.Text(""),
            ft.Row(
                [
                    ft.IconButton(ft.Icons.REFRESH, on_click=_rerun),
                    ft.IconButton(ft.Icons.QUESTION_MARK, on_click=_answer),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            ft.Text("Вже використано: ", size=TEXT_SIZE),
            used_block,
            ft.Text(""),
            elements.back_button(page),
            ft.Row(
                controls=[
                    author.button(page),
                    about.button(page),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )
