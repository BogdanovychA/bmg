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


@dataclass
class Input:
    city: str = ""


def last_letter(city: str, letters: tuple) -> str:

    if not city:
        return ""

    if city[-1] in letters:
        return city[-1]
    else:
        return last_letter(city[:-1], letters)


def main(cities: CityStorage):

    def _remove_city(first_char: str, the_city: str):
        cities[first_char].discard(the_city)
        used.add(the_city)

    used: UsedCities = set()
    all_letters = tuple(cities.keys())

    game_finished = False
    move = Move.AI
    letter = random.choice(all_letters)
    response = Input()
    char = ""

    while not game_finished:

        print(used)

        if move == Move.AI:

            city = random.choice(list(cities[letter]))
            _remove_city(first_char=letter, the_city=city)

            char = last_letter(city, all_letters)
            response = yield Event(
                error=False,
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

            _remove_city(first_char=char, the_city=city)

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
        except StopIteration:
            print("Гра завершена")
            break
