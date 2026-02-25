# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from routes import about, author
from utils import elements
from utils.config import BASE_URL, TEXT_SIZE
from utils.constants import GameMode

if TYPE_CHECKING:
    from flet_storage import FletStorage

TITLE = "Налаштування"
ROUTE = BASE_URL + "/settings"


def build_view(page: ft.Page, storage: FletStorage) -> ft.View:
    """Екран налаштувань"""

    async def _clear_cache(event: ft.Event) -> None:
        await storage.clear()

    async def _switch(event: ft.Event) -> None:
        """Обробник перемикача вкл/викл будильника"""

        value = event.control.selected[0]

        page.session.store.set("game_mode", value)
        await storage.set("game_mode", value)

        if value == GameMode.OFFLINE:
            text.value = "Локальний режим роботи (рекомендовано)"
        else:
            text.value = "Робота по API (не рекомендується)"

        text.update()

    game_mode_selector = ft.SegmentedButton(
        selected=[page.session.store.get("game_mode")],
        allow_empty_selection=False,
        allow_multiple_selection=False,
        show_selected_icon=False,
        segments=[
            ft.Segment(
                value=GameMode.OFFLINE,
                label=ft.Text(GameMode.OFFLINE),
                icon=ft.Icons.STAY_CURRENT_PORTRAIT,
            ),
            ft.Segment(
                value=GameMode.ONLINE,
                label=ft.Text(GameMode.ONLINE),
                icon=ft.Icons.CLOUD_QUEUE,
            ),
        ],
        on_change=_switch,
    )

    text = ft.Text("", size=TEXT_SIZE)

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            ft.Text("Режим роботи застосунку", size=TEXT_SIZE),
            ft.Text(""),
            game_mode_selector,
            ft.Text(""),
            text,
            ft.Text(""),
            ft.Button(
                "Видалити кеш", icon=ft.Icons.DELETE_OUTLINE, on_click=_clear_cache
            ),
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
