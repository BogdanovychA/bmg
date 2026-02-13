# -*- coding: utf-8 -*-

from enum import Enum


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    RANDOM = "random"


class GameMode(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
