# -*- coding: utf-8 -*-

import flet as ft
import requests

from utils import elements
from utils.config import TEXT_SIZE
from utils.utils import is_int

ROUTE = "/next-number"
TITLE = "Вгадай наступне число"


def get_sequence(length):

    target_url = f"https://karatel.ua/api/next_number/get/{length}"
    query_params = {
        "difficulty": "easy",
        # "random": "true"
    }

    try:
        response = requests.get(target_url, params=query_params, timeout=5)
        response.raise_for_status()
        return response.json()

    except (requests.exceptions.RequestException, Exception) as e:
        text = f"Сталася помилка при запиті до API: {e}"
        print(text)
        return ("Головне питання життя, всесвіту і всього такого", 42), text


def build_view(page: ft.Page) -> ft.View:

    def _ok(event: ft.ControlEvent):
        if is_int(answer_block.value) and int(answer_block.value) == target_value:
            message_block.value = f"Правильно! {hint}"
        else:
            message_block.value = "Не вгадав!"
        event.page.update()

    def _hint(event: ft.ControlEvent):
        message_block.value = hint
        event.page.update()

    def _answer(event: ft.ControlEvent):
        answer_block.value = str(target_value)
        event.page.update()

    def _rerun(event: ft.ControlEvent):
        _init()
        answer_block.value = ""
        message_block.value = ""
        event.page.update()

    def _init():
        nonlocal target_value, hint
        sequence, hint = get_sequence(6)
        *quest_numbers, target_value = sequence
        quest_block.value = ",   ".join(map(str, quest_numbers))

    description = "Визнач, що це за послідовність\nта яке число має бути наступним:"
    target_value = None
    hint = ""
    quest_block = ft.Text("", size=TEXT_SIZE)
    answer_block = ft.TextField(value="", width=100)
    message_block = ft.Text("", size=TEXT_SIZE)

    _init()

    return ft.View(
        route=ROUTE,
        # vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE),
            ft.Text(""),
            ft.Text(description, size=TEXT_SIZE),
            quest_block,
            message_block,
            ft.Row(
                [
                    ft.IconButton(ft.Icons.REFRESH, on_click=_rerun),
                    answer_block,
                    ft.IconButton(ft.Icons.DONE_OUTLINE, on_click=_ok),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Button("Підказка", on_click=_hint),
                    ft.Button("Відповідь", on_click=_answer),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(""),
            elements.back_button(page),
        ],
    )
