# -*- coding: utf-8 -*-
import flet as ft

def main(page: ft.Page):
    page.title = "Bogdanovych's Mini Games"
    page.theme_mode = ft.ThemeMode.DARK
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def reduce_click(event: ft.ControlEvent):
        answer.value = str(int(answer.value) - 1)
        event.page.update()

    def add_click(event: ft.ControlEvent):
        answer.value = str(int(answer.value) + 1)
        event.page.update()

    def ok(event: ft.ControlEvent):
        text_info.value = answer.value
        event.page.update()

    text_info = ft.Text(value="")
    game_title = ft.Text("Вгадай наступне число")
    question = ft.Text("1, 2, 3, 4, 5, X")
    minus_button = ft.IconButton(ft.Icons.REMOVE, on_click=reduce_click)
    answer = ft.TextField(value="0", width=100)
    plus_button = ft.IconButton(ft.Icons.ADD, on_click=add_click)
    ok_button = ft.Button("Підтвердити", on_click=ok)

    main_layout = ft.Column(
        controls=[
            game_title,
            question,
            ft.Row([minus_button, answer, plus_button], alignment=ft.MainAxisAlignment.CENTER),
            text_info,
            ok_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Центрування по вертикалі в колонці
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Центрування по горизонталі
        expand=True  # Колонка розтягнеться на всю висоту сторінки
    )

    page.add(main_layout)

if __name__ == "__main__":
    ft.run(main)

