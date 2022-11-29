import json
from collections import defaultdict

NUM = 7  # 문제수
PENALTY_TIME = 20  # 패널티 시간

BEST = 1
GOLD = 2
SILVER = 3
BRONZE = 5


def get_rank(timeline):
    timeline.sort(key=lambda x: x["id"])

    # m = 123 # 참가자수 알 경우

    # 참가자수 계산
    m = 0
    for item in timeline:
        m = max(m, item["team"])

    is_solved = [[0]*NUM for i in range(m+1)]
    penalty = [[0]*NUM for i in range(m+1)]

    for item in timeline:
        problem = item["problem"]
        team = item["team"]
        result = item["result"]
        submissionTime = item["submissionTime"]
        # 이미 푼 문제면 패널티를 더하지 않음
        if is_solved[team][problem]:
            continue
        if result == "Yes":
            # 맞았으면 시간만큼 추가
            is_solved[team][problem] = 1
            penalty[team][problem] += submissionTime
        else:
            # 틀렸으면 패널티 추가
            penalty[team][problem] += PENALTY_TIME

    # [인덱스, 맞은 수, 패널티]
    total = [[i, 0, 0] for i in range(m+1)]
    for i in range(1, m+1):
        total[i][1] = sum(is_solved[i])
        for j in range(NUM):
            total[i][2] += penalty[i][j] * is_solved[i][j]

    total.sort(key=lambda x: (-x[1], x[2]))
    # print(total)
    ret = []
    for i in range(len(ret), len(ret) + BEST):
        user, _, p = total[i]
        ret.append((user, p, "대상"))
    for i in range(len(ret), len(ret) + GOLD):
        user, _, p = total[i]
        ret.append((user, p, "금상"))
    for i in range(len(ret), len(ret) + SILVER):
        user, _, p = total[i]
        ret.append((user, p, "은상"))
    for i in range(len(ret), len(ret) + BRONZE):
        user, _, p = total[i]
        ret.append((user, p, "동상"))
    return ret


if __name__ == "__main__":
    with open("./runs.json", "r") as f:
        data = json.load(f)

    # 제출번호기준 정렬
    timeline = data["runs"]
    print(get_rank(timeline))
