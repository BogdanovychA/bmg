# -*- coding: utf-8 -*-

type CityStorage = dict[str, set[str]]
type UsedCities = set[str]

from .database.blacklists import NORMALISED_BLACKLIST
from .database.normalised import NORMALISED


def create_available_cities() -> CityStorage:
    return {
        letter: (cities - NORMALISED_BLACKLIST.get(letter, set()))
        for letter, cities in NORMALISED.items()
    }


if __name__ == "__main__":
    available_cities: CityStorage = create_available_cities()
    used_cities: UsedCities = set()

    print("available_cities:")
    for key, value in available_cities.items():
        print(f"{key}: {value}")
