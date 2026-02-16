# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import httpx

from utils.config import API_URL
from utils.exceptions import GameAPIError

from . import logic
from .constants import Symbol


class GameData(ABC):
    """Абстрактний метод для роботи з даними гри"""

    @abstractmethod
    def check_winner(self, board: list) -> str:
        """Перевірка чи є переможець на дошці"""
        pass

    @abstractmethod
    def best_move(self, board: list, player: str) -> int | str:
        """Обрахування кращого ходу"""
        pass


class APIData(GameData):
    """Робота по API"""

    def __init__(self):
        self.BASE_API_URL = f"{API_URL}/ttt"
        self.API_HEADERS = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.ERROR_TEXT = "Сталася помилка при запиті до API"

    def check_winner(self, board: list) -> str | None:

        target_url = f"{self.BASE_API_URL}/check"
        headers = self.API_HEADERS
        payload = board

        try:
            response = httpx.post(
                target_url, headers=headers, json=payload, timeout=10.0
            )

            response.raise_for_status()
            return response.json()["result"]

        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            text = f"{self.ERROR_TEXT}: {e}"
            print(text)
            raise GameAPIError(text) from e
        except Exception as e:
            text = f"Непередбачувана помилка: {e}"
            print(text)
            raise GameAPIError(text) from e

    def best_move(self, board: list, player: str) -> int:
        """Звернення до API для обрахування кращого ходу"""

        target_url = f"{self.BASE_API_URL}/move"
        headers = self.API_HEADERS
        payload = {"board": board, "max_player_symbol": player}

        try:
            response = httpx.post(
                target_url, headers=headers, json=payload, timeout=15.0
            )

            response.raise_for_status()
            return response.json()

        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            text = f"{self.ERROR_TEXT}: {e}"
            print(text)
            raise GameAPIError(text) from e
        except Exception as e:
            text = f"Непередбачувана помилка: {e}"
            print(text)
            raise GameAPIError(text) from e


class SelfData(GameData):
    """Робота локально"""

    def check_winner(self, board: list) -> str:
        return logic.check_winner(board)

    def best_move(self, board: list, player: str) -> int | str:

        return logic.best_move(
            board,
            player,
            Symbol.O.value if player == Symbol.X.value else Symbol.X.value,
        )
