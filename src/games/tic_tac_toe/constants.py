# -*- coding: utf-8 -*-

from enum import StrEnum


class Symbol(StrEnum):
    X = "X"
    O = "O"  # noqa: E741
    EMPTY = "none"
    DRAW = "draw"
