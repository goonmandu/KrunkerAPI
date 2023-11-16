def index_of_first_number(string):
    for i, c in enumerate(string):
        if c.isdigit():
            return i


def index_of_first_alpha(string):
    for i, c in enumerate(string):
        if c.isalpha():
            return i


def hours_played(string):
    ret = 0
    units = string.split()
    for unit in units:  # O(n^2) horrible efficiency, but who cares there's only gonna be 3 units anyway
        if "d" in unit:
            ret += 24 * int(unit[:-1])
        elif "h" in units:
            ret += int(unit[:-1])
        elif "m" in units:
            ret += int(unit[:-1]) / 60
    return ret


def get_class_name_of(string):
    keywords = (
        "triggerman",
        "hunter",
        "run n gun",
        "spray n pray",
        "vince",
        "detective",
        "marksman",
        "rocketeer",
        "agent",
        "runner",
        "bowman",
        "commando",
        "trooper",
        "infiltrator"
    )
    for keyword in keywords:
        if keyword in string.lower():
            return keyword.replace(" ", "_")
