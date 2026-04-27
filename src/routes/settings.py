# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import flet as ft

from config import app, style
from routes import about, author
from utils import elements
from utils.constants import GameMode

if TYPE_CHECKING:
    from flet_storage import FletStorage

TITLE = "Налаштування"
ROUTE = app.settings.base_url + "/settings"

logger = logging.getLogger(__name__)


def build_view(page: ft.Page, storage: FletStorage) -> ft.View:
    """Екран налаштувань"""

    async def _clear_cache(event: ft.Event) -> None:
        try:
            await storage.clear()
        except RuntimeError:
            logger.exception("Помилка при очистці кешу")

    async def _switch(event: ft.Event) -> None:
        """Обробник перемикача вкл/викл будильника"""

        value = event.control.selected[0]

        page.session.store.set("game_mode", value)

        try:
            await storage.set("game_mode", value)
        except RuntimeError:
            logger.exception("Помилка при записі game_mode")

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

    text = ft.Text("", size=style.settings.text_size)

    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text(""),
            ft.Text("Режим роботи застосунку", size=style.settings.text_size),
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
