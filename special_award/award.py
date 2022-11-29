from special_award import condition1, condition2, condition3, condition4, condition5, condition6, condition7, condition8, condition9, condition10
import json
from get_rank import get_rank

def get_award():
    with open("./final_runs.json", "r") as f:
        data = json.load(f)
    timeline = data["runs"]
    timeline.sort(key=lambda x: x["id"])
    rank = get_rank(timeline)
    # rank = []
    condition9(timeline, rank) # 특별상 특성상 9번이 가장 앞으로 와야 함

    condition1(timeline, rank)
    condition2(timeline, rank)
    condition3(timeline, rank)
    # condition4(timeline, rank)
    condition5(timeline, rank)
    condition6(timeline, rank)
    condition7(timeline, rank)
    condition8(timeline, rank)
    condition10(timeline, rank)
    return rank
