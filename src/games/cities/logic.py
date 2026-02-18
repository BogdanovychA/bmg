# -*- coding: utf-8 -*-

import random
from dataclasses import dataclass
from enum import Enum

from .types import CityStorage, UsedCities


class Move(Enum):
    PLAYER = "player"
    AI = "ai"


@dataclass
class Event:
    error: bool = False
    city: str = ""
    message: str = ""
    game_over: bool = False


@dataclass
class Input:
    city: str = ""


def last_letter(city: str, letters: tuple) -> str:
    """
    Повертає останню літеру міста, з урахуванням заборонених символів.
    Обережно, рекурсія! :)
    """

    if not city:
        return ""

    if city[-1] in letters:
        return city[-1]
    else:
        return last_letter(city[:-1], letters)


def main(cities: CityStorage):
    """Основна функція-генератор"""

    def _remove_city():
        """
        Допоміжна функція для видалення використаного міста з основного
        словника та додавання в сет використаних міст
        """
        cities[letter].discard(city)
        used.add(city)

    used: UsedCities = set()
    all_letters = tuple(cities.keys())

    move = Move.AI
    letter = random.choice(all_letters)  # Перша літера нового міста
    response = Input()
    char = ""  # Остання літера попереднього міста

    while True:

        if move == Move.AI:

            if not cities.get(letter):  # None або порожній set — обидва False
                return Event(
                    game_over=True,
                    message=f'Ви виграли! Більше немає міст на "{letter.upper()}"',
                )

            city = random.choice(list(cities[letter]))

            _remove_city()

            char = last_letter(city, all_letters)

            if not cities.get(char):
                return Event(
                    game_over=True,
                    city=city.upper(),
                    message=f'Ви програли! Більше немає міст на "{char.upper()}"',
                )

            response = yield Event(
                city=city.upper(),
                message=f'Назви місто на літеру "{char.upper()}"',
            )

            move = Move.PLAYER

        elif move == Move.PLAYER:

            city = response.city.lower()

            if not city:
                response = yield Event(
                    error=True,
                    message=f'Ти нічого не ввів. Введи місто на літеру "{char.upper()}"',
                )
                continue

            letter = city[0]

            if letter != char:
                response = yield Event(
                    error=True,
                    message=f'Місто "{city.upper()}" не починається на літеру "{char.upper()}". Введи інше',
                )
                continue
            elif city in used:
                response = yield Event(
                    error=True,
                    message=f'Місто "{city.upper()}" вже було використано. Введи інше на літеру "{char.upper()}"',
                )
                continue
            elif letter not in cities or city not in cities[letter]:
                response = yield Event(
                    error=True,
                    message=f'Місто "{city.upper()}" не існує. Введи інше на літеру "{char.upper()}"',
                )
                continue

            _remove_city()

            letter = last_letter(city, all_letters)
            move = Move.AI


if __name__ == "__main__":

    from games.cities.abstract import SelfData

    game = main(cities=SelfData().get_cities())

    event = next(game)

    while True:
        try:
            if event.city:
                print(event.city)
            event = game.send(Input(city=input(f"{event.message}: ")))
        except StopIteration as e:
            final_event = e.value
            print(final_event.message)
            break
