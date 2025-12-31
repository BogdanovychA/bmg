# -*- coding: utf-8 -*-

import asyncio
import flet as ft
import root

def back_button(page):
    return ft.Button(
                        "Перейти до списку ігор",
                        on_click=lambda: asyncio.create_task(
                            page.push_route(root.ROUTE)
                        ),
                    )