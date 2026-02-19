# -*- coding: utf-8 -*-

import random
from typing import Generator

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
        game: Generator,
    ) -> None:
        self.game = game
        self.event = next(game)


def build_view(page: ft.Page) -> ft.View:

    def _create_client() -> GameClient:
        return GameClient(
            game=logic.main(all_cities=abstract.SelfData().get_cities())
            # game=logic.main(all_cities=abstract.TestData().get_cities())
        )

    def _ok(event: ft.Event) -> None:

        if not client.game:
            return

        if not answer_block.value:
            return

        try:
            client.event = client.game.send(logic.Input(city=answer_block.value))
            if not client.event.error:
                city_block.value = client.event.city
                message_block.value = client.event.message
                answer_block.value = ""
                used_block.value = make_used_string(client.event.used_cities)
            else:
                message_block.value = client.event.message

        except StopIteration as e:
            client.game = None
            client.event = e.value

            if client.event.game_over:
                sub_title.value = ""
                city_block.value = (
                    client.event.message
                )  # Неявне використання city_block :)
                message_block.value = "Перезапусти гру".upper()
                answer_block.value = ""

        event.page.update()

    def _answer(event: ft.Event) -> None:

        if not client.game:
            return

        answer_block.value = random.choice(list(client.event.available_cities)).title()
        event.page.update()

    def _rerun(event: ft.Event) -> None:

        nonlocal client
        client = _create_client()

        sub_title.value = SUB_TITLE
        city_block.value = client.event.city
        message_block.value = client.event.message
        answer_block.value = ""
        used_block.value = make_used_string(client.event.used_cities)

        event.page.update()

    page.title = TITLE

    client = _create_client()

    sub_title = ft.Text(SUB_TITLE, size=TEXT_SIZE)
    city_block = ft.Text(client.event.city, size=TEXT_SIZE)
    message_block = ft.Text(client.event.message, size=TEXT_SIZE)
    answer_block = ft.TextField(
        value="", width=250, bgcolor=FORM_BG_COLOR, border_color=FORM_BORDER_COLOR
    )
    used_block = ft.Text(make_used_string(client.event.used_cities))

    return ft.View(
        route=ROUTE,
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
