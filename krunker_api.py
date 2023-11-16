from scraper import scrape
from utils import *


def _main_stat_parser(meta_stats, xpbar_stats, main_stats):
    ret = {}
    for string in main_stats:
        split_index = index_of_first_number(string)
        name = string[:split_index].lower().replace(" ", "_")
        value = string[split_index:]
        if name == "inventory_~":
            name = name[:-2]  # truncate " ~"
        if name == "helpful_reports":
            ratio = {
                "helpful": value.split("/")[0],
                "total": value.split("/")[1]
            }
            ret[name] = ratio
            continue
        if name == "w/l":
            name = "win_loss_ratio"
        if name == "accuracy":
            value = value[:-1]  # truncate "%"
        if name == "time_played":
            value = str(hours_played(value))  # convert to hours played
        ret[name] = value

    ret["current_xp"] = xpbar_stats.split("/")[0]
    ret["threshold_xp"] = xpbar_stats.split("/")[1]

    for k, v in ret.items():  # turn string values into numbers
        if isinstance(v, dict):
            for nk, nv in v.items():
                if "." in nv:
                    v[nk] = float(nv)
                else:
                    v[nk] = int(nv.replace(",", ""))
        elif "." in v:
            ret[k] = float(v)
        else:
            ret[k] = int(v.replace(",", ""))

    ret["partner"] = "verified" in meta_stats
    ret["verified"] = "check_circle" in meta_stats
    ret["clan"] = meta_stats[meta_stats.index("[")+1:meta_stats.index("]")]

    return ret


def _class_stats_parser(class_stats):
    ret = {}
    for string in class_stats:
        split_index = index_of_first_number(string)
        name = get_class_name_of(string[:split_index])
        xpstring = string[split_index:]
        xp_split_index = index_of_first_alpha(xpstring)
        current_xp_progress = xpstring[:xp_split_index]
        current_level_string = xpstring[xp_split_index:]
        current_xp_earned = current_xp_progress.split("/")[0].strip(" ")
        current_xp_threshold = current_xp_progress.split("/")[1].strip(" ")
        current_level = current_level_string.replace("Lvl ", "")
        ret[name] = {
            "level": int(current_level),
            "current_xp": int(current_xp_earned),
            "threshold_xp": int(current_xp_threshold)
        }

    return ret


def krunker_api(username):
    data = scrape(username)
    combined = {
        "name": username,
        "general": _main_stat_parser(data["meta"], data["xpbar"], data["main_stats"]),
        "class_xp": _class_stats_parser(data["class_stats"])
    }
    return combined


if __name__ == "__main__":
    print(krunker_api("goonmandu"))
