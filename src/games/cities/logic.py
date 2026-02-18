# -*- coding: utf-8 -*-

from .types import CityStorage, UsedCities


def main(available: CityStorage):
    used: UsedCities = set()

    for key, value in available.items():
        print(f"{key}: {value}")

    print(used)


if __name__ == "__main__":

    from games.cities.abstract import SelfData

    client = SelfData()

    main(available=client.get_cities())
