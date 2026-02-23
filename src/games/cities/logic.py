# -*- coding: utf-8 -*-

import random
from dataclasses import dataclass, field
from enum import Enum

from . import utils
from .database import blacklists
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
    available_cities: Cities | None = None
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


def main(
    all_cities: CityStorage,
    restore: bool = False,
    used_cities: Cities | None = None,
    last_ai_city: str | None = None,
):
    """Основна функція-генератор"""

    def _remove_city():
        """
        Допоміжна функція для видалення використаного міста з основного
        словника та додавання в сет використаних міст
        """
        all_cities[first_letter].discard(city)
        used_cities.add(city)

    all_letters = tuple(all_cities.keys())
    blacklist: CityStorage = utils.normalised(blacklists.CITIES)
    response = Input()

    if not restore:
        move = Move.AI
        city = ""  # Ініціалізація

        used_cities = set()

        first_letter = random.choice(all_letters)  # Перша літера нового міста
        last_letter = ""  # Остання літера попереднього міста. Ініціалізація

    else:
        if not used_cities:
            raise TypeError(
                "Список використаних міст (used_cities) не може бути порожнім"
            )
        if not last_ai_city:
            raise TypeError(
                "Останнє місто, яке назвав AI (last_ai_city) не може бути порожнім"
            )

        move = Move.PLAYER
        city = last_ai_city.lower().strip()

        used_cities = {city.lower() for city in used_cities}  # Перестраховка :)

        all_cities = utils.create_available(
            all_cities, utils.create_used_dict(used_cities)
        )

        first_letter = ""  # Перша літера нового міста. Ініціалізація
        last_letter = get_last_letter(
            city, all_letters
        )  # Остання літера попереднього міста.

    while True:

        if move == Move.AI:

            if not all_cities.get(first_letter):  # None або порожній set — обидва False
                msg = (
                    f'Ви виграли! Більше немає міст на літеру «{first_letter.upper()}»'
                )
                return Event(
                    game_over=True,
                    message=msg,
                    used_cities=used_cities,
                )

            city = random.choice(list(all_cities[first_letter]))
            _remove_city()
            last_letter = get_last_letter(city, all_letters)

            if not all_cities.get(last_letter):
                msg = (
                    f'Ви програли! Більше немає міст на літеру «{last_letter.upper()}»'
                )
                return Event(
                    game_over=True,
                    city=city.upper(),
                    message=msg,
                    used_cities=used_cities,
                )

            msg = f'Назви місто на літеру «{last_letter.upper()}» (лишилося {len(all_cities[last_letter])})'
            response = yield Event(
                city=city.upper(),
                message=msg,
                available_cities=all_cities[last_letter],
                used_cities=used_cities,
            )

            move = Move.PLAYER

        elif move == Move.PLAYER:

            if restore:
                restore = False

                msg = f'Відновлення гри... Назви місто на літеру «{last_letter.upper()}» (лишилося {len(all_cities[last_letter])})'
                response = yield Event(
                    city=city.upper(),
                    message=msg,
                    available_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )

            city = response.city.lower().strip()

            if not city:
                msg = f'Ти нічого не ввів. Назви місто на літеру «{last_letter.upper()}» (лишилося {len(all_cities[last_letter])})'
                response = yield Event(
                    error=True,
                    message=msg,
                    available_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue

            first_letter = city[0]

            if first_letter in blacklist and city in blacklist[first_letter]:
                msg = f'Місто «{city}» належить до території росії чи білорусі. Назви інше на літеру «{last_letter.upper()}» (лишилося {len(all_cities[last_letter])})'
                response = yield Event(
                    error=True,
                    message=msg,
                    available_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue
            elif first_letter != last_letter:
                msg = f'Місто «{city.title()}» не починається на літеру «{last_letter.upper()}» (лишилося {len(all_cities[last_letter])}). Назви інше'
                response = yield Event(
                    error=True,
                    message=msg,
                    available_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue
            elif city in used_cities:
                msg = f'Місто «{city.title()}» вже було використано. Назви інше на літеру «{last_letter.upper()}» (лишилося {len(all_cities[last_letter])})'
                response = yield Event(
                    error=True,
                    message=msg,
                    available_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue
            elif first_letter not in all_cities or city not in all_cities[first_letter]:
                msg = f'Місто «{city.title()}» не існує. Назви інше на літеру «{last_letter.upper()}» (лишилося {len(all_cities[last_letter])})'
                response = yield Event(
                    error=True,
                    message=msg,
                    available_cities=all_cities[last_letter],
                    used_cities=used_cities,
                )
                continue

            _remove_city()
            first_letter = get_last_letter(city, all_letters)
            move = Move.AI


if __name__ == "__main__":

    from games.cities.abstract import SelfData

    # game = main(all_cities=SelfData().get_cities())

    game = main(
        all_cities=SelfData().get_cities(),
        restore=True,
        used_cities={"Київ", "варшава", "варшава", "київ", "Житомир"},
        last_ai_city="Київ",
    )

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
