# -*- coding: utf-8 -*-

import asyncio

import flet as ft

import root
from config import TITLE_SIZE


def back_button(page):
    return ft.Button(
        "Перейти до списку ігор",
        on_click=lambda: asyncio.create_task(page.push_route(root.ROUTE)),
    )


def app_bar(title):
    return ft.AppBar(
        title=ft.Text(title, size=TITLE_SIZE, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
    )
