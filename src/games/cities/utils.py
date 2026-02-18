# -*- coding: utf-8 -*-

from .types import CityStorage


def normalised(the_dict: CityStorage) -> CityStorage:
    return {key: set(map(str.lower, cities)) for key, cities in the_dict.items()}
