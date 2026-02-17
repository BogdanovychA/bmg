# -*- coding: utf-8 -*-

from .database.normalised import NORMALISED

if __name__ == "__main__":

    cities_db = NORMALISED.copy()

    for key, value in cities_db.items():
        print(f"{key}: {value}")
