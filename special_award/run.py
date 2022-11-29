import json
from award import get_award

if __name__ == "__main__":
    with open("./handle_to_id.json", "r") as f:
        handle2id = json.load(f)
    with open("./contest_info.json", "r") as f:
        info = json.load(f)
    contestants = info["contestants"]
    users = dict()
    for contestant in contestants:
        handle, name, group = contestant.split()
        users[handle.lower()] = [name, group]
    id2handle = dict()
    for i in handle2id:
        id2handle[handle2id[i]] = i
    rank = get_award()
    winner = []
    for idx, info, award in rank:
        winner.append((idx, id2handle[idx], award))
    data = []

    for i, (idx, user, award) in enumerate(winner):
        d = {"id": idx, "rank": award,
             "name": users[user][0], "group": users[user][1]}
        if award == "대상":
            d["icon"] = "crown_gold"
        elif award == "금상":
            d["icon"] = "medal_gold_blue"
        elif award == "은상":
            d["icon"] = "medal_silver_green"
        elif award == "동상":
            d["icon"] = "medal_bronze_red"
        else:
            d["icon"] = "thumb_up"
        data.append(d)

    with open("award_slide.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent="\t", ensure_ascii=False)
