class WeaponClass:
    def __init__(self, name, level, currentxp, thresholdxp):
        self.name = name
        self.level = level
        self.currentxp = currentxp
        self.thresholdxp = thresholdxp


class UserNotFoundException(Exception):
    pass