# -*- coding: utf-8 -*-

from .types import CityStorage


def normalised(storage: CityStorage) -> CityStorage:
    return {letter: set(map(str.lower, cities)) for letter, cities in storage.items()}


def create_available(main: CityStorage, blacklist: CityStorage) -> CityStorage:
    return {
        letter: (cities - blacklist.get(letter, set()))
        for letter, cities in main.items()
    }
