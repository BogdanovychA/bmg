# -*- coding: utf-8 -*-

import random
from dataclasses import dataclass, field
from enum import Enum

from .types import Cities, CityStorage


class Move(Enum):
    PLAYER = "player"
    AI = "ai"


@dataclass
class Event:
    error: bool = False
    city: str = ""
    message: str = ""
    used_cities: Cities = field(default_factory=set)
    unused_cities: Cities | None = None
    game_over: bool = False


@dataclass
class Input:
    city: str = ""


def get_last_letter(city: str, letters: tuple) -> str:
    """
    Повертає останню літеру міста, з урахуванням заборонених символів.
    Обережно, рекурсія! :)
    """

    if not city:
        return ""

    if city[-1] in letters:
        return city[-1]
    else:
        return get_last_letter(city[:-1], letters)


def main(all_cities: CityStorage):
    """Основна функція-генератор"""

    def _remove_city():
        """
        Допоміжна функція для видалення використаного міста з основного
        словника та додавання в сет використаних міст
        """
        all_cities[first_letter].discard(city)
        used_cities.add(city)

    used_cities: Cities = set()
    all_letters = tuple(all_cities.keys())

    move = Move.AI
    first_letter = random.choice(all_letters)  # Перша літера нового міста
    response = Input()
    last_letter = ""  # Остання літера попереднього міста

    while True:

        if move == Move.AI:

            if not all_cities.get(first_letter):  # None або порожній set — обидва False
                return Event(
                    game_over=True,
                    message=f'Ви виграли! Більше немає міст на "{first_letter.upper()}"',
                    used_cities=used_cities,
                )

            city = random.choice(list(all_cities[first_letter]))

            _remove_city()

            last_letter = get_last_letter(city, all_letters)

            if not all_cities.get(last_letter):
                return Event(
                    game_over=True,
                    city=city.upper(),
                    message=f'Ви програли! Більше немає міст на "{last_letter.upper()}"',
                    used_cities=used_cities,
                )

            response = yield Event(
                city=city.upper(),
                message=f'Назви місто на літеру "{last_letter.upper()}"',
                unused_cities=all_cities[last_letter],
                used_cities=used_cities,
            )

            move = Move.PLAYER

        elif move == Move.PLAYER:

            city = response.city.lower()

            if not city:
                response = yield Event(
                    error=True,
                    message=f'Ти нічого не ввів. Введи місто на літеру "{last_letter.upper()}"',
                    unused_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue

            first_letter = city[0]

            if first_letter != last_letter:
                response = yield Event(
                    error=True,
                    message=f'Місто "{city.upper()}" не починається на літеру "{last_letter.upper()}". Введи інше',
                    unused_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue
            elif city in used_cities:
                response = yield Event(
                    error=True,
                    message=f'Місто "{city.upper()}" вже було використано. Введи інше на літеру "{last_letter.upper()}"',
                    unused_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue
            elif first_letter not in all_cities or city not in all_cities[first_letter]:
                response = yield Event(
                    error=True,
                    message=f'Місто "{city.upper()}" не існує. Введи інше на літеру "{last_letter.upper()}"',
                    unused_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue

            _remove_city()

            first_letter = get_last_letter(city, all_letters)
            move = Move.AI


if __name__ == "__main__":

    from games.cities.abstract import SelfData

    game = main(all_cities=SelfData().get_cities())

    event = next(game)

    while True:
        try:
            print(event)
            if event.city:
                print(event.city)
            event = game.send(Input(city=input(f"{event.message}: ")))
        except StopIteration as e:
            final_event = e.value
            print(final_event.message)
            break
