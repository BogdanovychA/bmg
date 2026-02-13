# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import httpx

from utils.config import API_URL, NUMBER_42, TEXT_42


class GameData(ABC):

    @abstractmethod
    def get_sequence(self, length, difficulty) -> tuple[tuple[int, ...], str]:
        pass


class APIData(GameData):

    def get_sequence(self, length, difficulty):

        target_url = f"{API_URL}/next-number/get/{length}"
        query_params = {
            "difficulty": difficulty,
            # "random": "true"
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

    def get_sequence(self, length, difficulty):
        return (1, 2, 3, 4, 5, 6), "Тестова послідовність"
