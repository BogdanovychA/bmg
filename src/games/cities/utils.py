# -*- coding: utf-8 -*-

from .types import Cities, CityStorage


def normalised(storage: CityStorage) -> CityStorage:
    return {letter: set(map(str.lower, cities)) for letter, cities in storage.items()}


def create_available(main: CityStorage, blacklist: CityStorage) -> CityStorage:
    return {
        letter: (cities - blacklist.get(letter, set()))
        for letter, cities in main.items()
    }


def make_used_string(cities: Cities) -> str:
    return ', '.join(sorted(map(str.title, cities)))


def create_used_dict(used_cities: Cities) -> CityStorage:
    used_dict = {}
    for city in used_cities:
        letter = city[0]

        if letter not in used_dict:
            used_dict[letter] = set()

        used_dict[letter].add(city)

    return used_dict
