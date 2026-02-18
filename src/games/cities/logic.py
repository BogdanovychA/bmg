# -*- coding: utf-8 -*-

from .database import blacklists, db
from .types import CityStorage, UsedCities
from .utils import create_available, normalised


def main(available: CityStorage):
    used: UsedCities = set()

    for key, value in available.items():
        print(f"{key}: {value}")

    print(used)


if __name__ == "__main__":

    available_cities = create_available(
        normalised(db.CITIES), normalised(blacklists.CITIES)
    )

    main(available_cities)
