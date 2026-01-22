# -*- coding: utf-8 -*-

import flet as ft
import httpx

from routes import about
from utils import elements
from utils.config import (
    API_URL,
    FORM_BG_COLOR,
    FORM_BORDER_COLOR,
    NUMBER_42,
    TEXT_42,
    TEXT_SIZE,
)
from utils.utils import is_int

ROUTE = "/next-number"
TITLE = "Вгадай наступне число"
SUB_TITLE = "Визнач, що це за послідовність\nта яке число має бути наступним:"


def get_sequence(length, difficulty):

    target_url = f"{API_URL}/next-number/get/{length}"
    query_params = {
        "difficulty": difficulty,
        # "random": "true"
    }

    try:
        response = httpx.get(target_url, params=query_params, timeout=5.0)

        response.raise_for_status()
        return response.json()

    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        text = f"Сталася помилка при запиті до API: {e}"
        print(text)
        return (TEXT_42, NUMBER_42), text
    except Exception as e:
        text = f"Інша помилка: {e}"
        print(text)
        return (TEXT_42, NUMBER_42), text


def build_view(page: ft.Page) -> ft.View:

    def _ok(event: ft.Event) -> None:
        if is_int(answer_block.value) and int(answer_block.value) == target_value:
            message_block.value = f"Правильно! {hint}"
        else:
            message_block.value = "Не вгадав!"
        event.page.update()

    def _hint(event: ft.Event) -> None:
        message_block.value = hint
        event.page.update()

    def _answer(event: ft.Event) -> None:
        answer_block.value = str(target_value)
        event.page.update()

    def _rerun(event: ft.Event) -> None:
        _init()
        answer_block.value = ""
        message_block.value = ""
        event.page.update()

    def _init():
        nonlocal target_value, hint
        sequence, hint = get_sequence(6, difficulty_block.value)
        *quest_numbers, target_value = sequence
        quest_block.value = ",   ".join(map(str, quest_numbers))

    difficulty_block = ft.Dropdown(
        label="Складність",
        label_style=ft.TextStyle(size=TEXT_SIZE),
        value="random",
        options=[
            ft.DropdownOption(key="easy", text="Низька"),
            ft.DropdownOption(key="medium", text="Середня"),
            ft.DropdownOption(key="hard", text="Висока"),
            ft.DropdownOption(key="expert", text="Надвисока"),
            ft.DropdownOption(key="random", text="Випадкова"),
        ],
        on_select=_rerun,
    )

    page.title = TITLE

    target_value = None
    hint = ""
    quest_block = ft.Text("", size=TEXT_SIZE)
    answer_block = ft.TextField(
        value="", width=100, bgcolor=FORM_BG_COLOR, border_color=FORM_BORDER_COLOR
    )
    message_block = ft.Text("", size=TEXT_SIZE)

    _init()

    return ft.View(
        route=ROUTE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text(""),
            ft.Text(SUB_TITLE, size=TEXT_SIZE),
            quest_block,
            message_block,
            ft.Text(""),
            ft.Row(
                [
                    ft.IconButton(ft.Icons.REFRESH, on_click=_rerun),
                    answer_block,
                    ft.IconButton(ft.Icons.DONE_OUTLINE, on_click=_ok),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            difficulty_block,
            ft.Text(""),
            ft.Row(
                [
                    ft.Button("Підказка", on_click=_hint),
                    ft.Button("Відповідь", on_click=_answer),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            elements.back_button(page),
            about.button(page),
        ],
    )
