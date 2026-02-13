# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import httpx

from utils.config import API_URL, NUMBER_42, TEXT_42

from . import logic


class GameData(ABC):
    """Абстрактний метод для роботи з даними гри"""

    @abstractmethod
    def get_sequence(self, length, difficulty) -> tuple[tuple[int, ...], str]:
        """Функція отримання послідовності та її опису"""
        pass


class APIData(GameData):
    """Робота по API"""

    def get_sequence(self, length, difficulty):
        target_url = f"{API_URL}/next-number/get/{length}"
        query_params = {
            "difficulty": difficulty,
        }

        try:
            response = httpx.get(target_url, params=query_params, timeout=5.0)

            response.raise_for_status()
            return response.json()

        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            text = f"Сталася помилка при запиті до API: {e}"
            print(text)
            return (TEXT_42, NUMBER_42), text
        except Exception as e:
            text = f"Інша помилка: {e}"
            print(text)
            return (TEXT_42, NUMBER_42), text


class SelfData(GameData):
    """Робота локально"""

    def get_sequence(self, length, difficulty):
        return logic.get_sequence(length, difficulty)
