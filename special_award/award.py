from special_award import *
from get_rank import get_rank

def get_award():
    with open("./final_runs.json", "r") as f:
        data = json.load(f)
    timeline = data["runs"]
    timeline.sort(key=lambda x: x["id"])
    rank = get_rank(timeline)
    # rank = []
    condition1(timeline, rank)
    condition2(timeline, rank)
    condition3(timeline, rank)
    # condition4(timeline, rank)
    condition5(timeline, rank)
    condition6(timeline, rank)
    condition7(timeline, rank)
    condition8(timeline, rank)
    condition9(timeline, rank)
    condition10(timeline, rank)
    return rank
