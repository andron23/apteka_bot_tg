# -*- coding: utf-8 -*-

from enum import Enum

token = "1234567:ABCxyz"
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    S_ENTER_CARD = "3"
    S_ENTER_PHONE = "4"
    S_ENTER_PHONE_REG = "5"
    S_ENTER_DATE = "6"
    S_ACCEPT = "7"