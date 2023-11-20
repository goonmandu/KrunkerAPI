from enum import Enum

class WeaponClass:
    def __init__(self, name, level, currentxp, thresholdxp):
        self.name = name
        self.level = level
        self.currentxp = currentxp
        self.thresholdxp = thresholdxp


class UserNotFoundException(Exception):
    pass


class ExitCode(Enum):
    SELENIUM_TIMEOUT = 1
    COULDNT_LOAD_HTML = 2
    USERNAME_NOT_FOUND = 3
