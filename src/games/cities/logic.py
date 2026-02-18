# -*- coding: utf-8 -*-

from .database import blacklists
from .database.normalised import NORMALISED
from .types import CityStorage, UsedCities


def create_available_cities() -> CityStorage:
    return {
        letter: (cities - blacklists.CITIES.get(letter, set()))
        for letter, cities in NORMALISED.items()
    }


if __name__ == "__main__":

    available_cities: CityStorage = create_available_cities()
    used_cities: UsedCities = set()

    print("available_cities:")
    for key, value in available_cities.items():
        print(f"{key}: {value}")
