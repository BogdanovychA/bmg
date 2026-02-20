# -*- coding: utf-8 -*-

import asyncio

import flet as ft

from routes import about
from utils import elements
from utils.config import BASE_URL, TEXT_SIZE

TITLE = "Про автора"
ROUTE = BASE_URL + "/author"


def button(page) -> ft.Button:
    return ft.Button(
        TITLE,
        on_click=lambda: asyncio.create_task(page.push_route(ROUTE)),
    )


def build_view(page: ft.Page) -> ft.View:
    page.title = TITLE
    return ft.View(
        route=ROUTE,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            elements.app_bar(TITLE, page),
            ft.Text("Андрій БОГДАНОВИЧ", size=TEXT_SIZE),
            ft.Text(""),
            ft.Image(
                src="/images/bogdanovych-900x900.jpg",  # Посилання на картинку
                width=200,
                height=200,
            ),
            ft.Text(""),
            ft.Text(
                size=TEXT_SIZE,
                spans=[
                    elements.link("Домашня сторінка", "https://www.bogdanovych.org"),
                    ft.TextSpan("\n"),
                    elements.link("Інші застосунки", "https://apps.bogdanovych.org"),
                ],
            ),
            ft.Text(""),
            elements.back_button(page),
            about.button(page),
        ],
    )
