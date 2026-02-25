# -*- coding: utf-8 -*-

from enum import StrEnum


class Difficulty(StrEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    RANDOM = "random"


class GameMode(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
