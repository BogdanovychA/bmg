# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from .database import blacklists, db
from .types import CityStorage
from .utils import create_available, normalised


class GameData(ABC):
    """Абстрактний метод для роботи з даними гри"""

    @abstractmethod
    def get_cities(self) -> CityStorage:
        """Отримання очищеної та нормалізованої бази міст"""
        pass


class SelfData(GameData):
    """Робота локально"""

    def get_cities(self) -> CityStorage:
        return create_available(normalised(db.CITIES), normalised(blacklists.CITIES))
