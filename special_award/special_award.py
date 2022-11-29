import json
import bisect
from collections import defaultdict

# 이미 상 받은 사람인지 체크한다.


def is_already_award(status, user):
    for u, _, _ in status:
        if u == user:
            return True
    return False


FREEZE = 120
CONTEST_TIME = 180
NUM_PROBLEM = 10

# 프리즈 이후 첫 solve


def condition1(data, status):
    # 시간순 정렬
    data.sort(key=lambda x: x["id"])
    ret = []
    check = defaultdict(bool)

    # 이미 시간순으로 저장된 데이터
    for item in data:
        submissionTime = item["submissionTime"]
        if submissionTime > CONTEST_TIME:
            continue
        user = item["team"]
        # 프리즈 이전이라면 선택하지 않음
        if submissionTime < FREEZE:
            continue
        # 정답일경우 선택
        if item["result"] == "Yes":
            # 선택되지 않은 유저만 선택
            if not check[user]:
                check[user] = True
                ret.append((user, submissionTime))

    for user, time in ret:
        # 이미 선택되지 않은 사람 선택
        if is_already_award(status, user):
            continue
        status.append((user, time, "프리즈 이후 가장 첫 solve"))
        break

# 각 문제 제출 수로 만쥬의 식사를 풀었을 때 답이 가장 작은 사람 (동점자는 합이 가장 작은 사람 + 마지막 제출이 빠른 사람)


def condition2(data, status):
    # 시간순 정렬
    data.sort(key=lambda x:x["id"])
    num = dict() # 각 인원별 제출 수
    ret = []
    for item in data:
        user = item["team"]
        problem = item["problem"]
        idx = item["id"] # 마지막 제출
        if user not in num:
            num[user] = [[0]*NUM_PROBLEM, idx]
        num[user][0][problem]+=1

    for user in num:
        arr = num[user][0]
        ret.append((user, max(arr) - min(arr), sum(arr), num[user][1]))
    # 1. 결과가 가장 작은 사람
    # 2. 합이 가장 작은 사람
    # 3. 마지막 제출이 빠른 사람
    ret.sort(key=lambda x:(x[1], x[2], x[3]))
    for user, info, _, _ in ret:
        # 이미 선택되지 않은 사람 선택
        if is_already_award(status, user):
            continue
        status.append((user, info, "각 문제 제출 수로 만쥬의 식사를 풀었을 때 답이 가장 작은 사람"))
        break



# 첫 제출과 마지막 제출의 시간 차이가 가장 큰 사람

def condition3(data, status):
    data.sort(key=lambda x: x["id"])
    start = dict()
    end = dict()
    ret = []
    for item in data:
        submissionTime = item["submissionTime"]
        user = item["team"]
        if submissionTime > CONTEST_TIME:
            continue
        if user not in start:
            start[user] = submissionTime
        end[user] = submissionTime
    for user in start:
        ret.append((user, end[user] - start[user], end[user], start[user]))
    # 1. 차이가 가장 큰 사람
    # 2. 마지막 제출이 가장 늦은 사람
    # 3. 첫 제출이 가장 빠른사람
    ret.sort(key=lambda x: (-x[1], -x[2], x[3]))
    for user, value, _, _ in ret:
        if is_already_award(status, user):
            continue
        status.append((user, value, "첫 제출과 마지막 제출의 시간 차이가 가장 큰 사람"))
        break



def lis(memory):
    arr = list(map(int, list(str(memory))))
    n = len(arr)
    brr = [-9876543210]

    for i in range(n):
        if arr[i] > brr[-1]:
            brr.append(arr[i])
            continue
        t = bisect.bisect_left(brr, arr[i])
        brr[t] = arr[i]

    return len(brr) - 1

# 제출 메모리의 합의 LIS가 가장 긴 사람


def condition4(data, status):
    data.sort(key=lambda x: x["id"])
    memory = defaultdict(int)
    ret = []
    for item in data:
        memoryConsumed = item["memoryConsumed"]
        user = item["team"]
        submissionTime = item["submissionTime"]
        if submissionTime > CONTEST_TIME:
            continue
        # 정답 상관없이 메모리 사용량 더함
        memory[user] += memoryConsumed

    for user in memory:
        ret.append((user, lis(memory[user]), memory[user]))
    ret.sort(key=lambda x: (-x[1], -x[2]))

    for user, lis_value, _ in ret:
        if is_already_award(status, user):
            continue
        status.append((user, lis_value, "제출 메모리의 합의 LIS가 가장 긴 사람"))
        break


# 가장 많이 제출한 사람
def condition5(data, status):
    data.sort(key=lambda x: x["id"])
    ret = []
    # 제출 횟수
    count = defaultdict(int)
    # 마지막 제출
    rank = defaultdict(int)
    for item in data:
        user = item["team"]
        idx = item["id"]
        submissionTime = item["submissionTime"]
        if submissionTime > CONTEST_TIME:
            continue
        # 마지막 제출 업데이트
        rank[user] = idx
        count[user] += 1

    for user in rank:
        ret.append((user, count[user], rank[user]))

    # 갯수 내림차순, 동점자는 마지막 제출이 빠른 순서
    ret.sort(key=lambda x: (-x[1], x[2]))

    for user, count, _ in ret:
        if is_already_award(status, user):
            continue
        status.append((user, count, "가장 많이 제출한 사람"))
        break


# 제출 실행시간 합을 1203으로 나눈 나머지가 가장 작은 사람
def condition6(data, status):
    data.sort(key=lambda x: x["id"])
    mod = 1203  # Contest Date
    totalTime = defaultdict(int)
    ret = []
    for item in data:
        submissionTime = item["submissionTime"]
        if submissionTime > CONTEST_TIME:
            continue
        timeConsumed = item["timeConsumed"]
        user = item["team"]
        # 정답 상관 없이 시간 더함
        totalTime[user] += timeConsumed
    for user in totalTime:
        ret.append((user, totalTime[user] % mod, totalTime[user]))
    # 나머지 오름차순, 동점일시 전체 오름차순
    ret.sort(key=lambda x: (x[1], x[2]))
    for user, elapsed, _ in ret:
        if is_already_award(status, user):
            continue
        status.append((user, elapsed, "제출 실행시간 합을 1203으로 나눈 나머지가 가장 작은 사람"))
        break

# 가장 많이 틀린 뒤에 맞은 사람


def condition7(data, status):
    data.sort(key=lambda x: x["id"])
    # 푸는데 얼마나 걸렸는지
    count = defaultdict(int)
    # 풀었는지
    is_solved = defaultdict(bool)
    # 마지막 제출 시간
    time = defaultdict(int)
    ret = []
    for item in data:
        submissionTime = item["submissionTime"]
        if submissionTime > CONTEST_TIME:
            continue
        problem = item["problem"]
        user = item["team"]
        result = item["result"]
        submissionTime = item["id"]
        # 이미 풀었으면 통과
        if is_solved[(user, problem)]:
            continue
        if result == "Yes":
            # 맞았으면 풀었다고 체크
            is_solved[(user, problem)] = True
            time[(user, problem)] = submissionTime
            count[(user, problem)] += 1
        else:
            time[(user, problem)] = submissionTime
            count[(user, problem)] += 1
    for user, problem in is_solved:
        # 못 풀었다면 통과
        if not is_solved[(user, problem)]:
            continue
        x = (user, problem)
        ret.append((user, count[x], problem, time[x]))
    # 1. 가장 많이 틀리고 맞은 사람
    # 2. 더 어려운 문제
    # 3. 더 빨리 푼 사람
    ret.sort(key=lambda x: (-x[1], -x[2], x[3]))

    for user, cnt, _, _ in ret:
        if is_already_award(status, user):
            continue
        status.append((user, cnt, "가장 많이 틀린 뒤에 맞은 사람"))
        break

# 마지막 오답이후 정답이 가장 빠른 사람


def condition8(data, status):
    data.sort(key=lambda x: x["id"])
    wrong = defaultdict(bool)
    last = defaultdict(int)
    is_solved = defaultdict(int)
    diff = defaultdict(int)
    time = defaultdict(int)
    ret = []

    for item in data:
        user = item["team"]
        submissionTime = item["submissionTime"]
        idx = item["id"]
        result = item["result"]
        problem = item["problem"]
        x = (user, problem)

        if submissionTime > CONTEST_TIME:
            continue
        if is_solved[x]:
            continue

        if result == "Yes":
            # 틀린 적이 없으면 통과
            if not wrong[x]:
                continue
            diff[x] = submissionTime - last[x]
            time[x] = idx
        else:
            wrong[x] = True
            last[x] = submissionTime
    for user, problem in diff:
        ret.append((user, diff[(user, problem)], time[(user, problem)]))

    # 1. 정답과 오답간 시간 차이
    # 2. 더 빨리 푼 사람
    ret.sort(key=lambda x: (x[1], x[2]))

    for user, diff, _ in ret:
        if is_already_award(status, user):
            continue
        status.append((user, diff, "마지막 오답이후 정답이 가장 빠른 사람"))
        break


# 킥보드로 통학하기를 가장 빨리 맞힌 사람
def condition9(data, status):
    pass # 구현해야 됨

# 정답 제출 시간간격이 가장 큰 사람(동점자는 마지막 제출이 가장 느린 사람)


def condition10(data, status):
    data.sort(key=lambda x: x["id"])
    ret = []
    is_solved = defaultdict(bool)
    users = defaultdict(list)
    for item in data:
        problem = item["problem"]
        user = item["team"]
        result = item["result"]
        time = item["submissionTime"]

        time = item["submissionTime"]
        if time > CONTEST_TIME:
            continue
        x = (user, problem)
        # 이미 풀린 상태면 통과
        if is_solved[x] == 1:
            continue

        if result == "Yes":
            is_solved[x] = 1
            # 해결했을 경우 해당 유저의 해결 시간을 추가한다.
            users[user].append(time)

    for user in users:
        arr = users[user]
        # 해결 수가 2 미만이면 계산하지 않음
        if len(arr) < 2:
            continue
        m = 0
        # 정답 제출 시간 간격이 가장 큰 값을 배열에 넣음
        for i in range(len(arr)-1):
            m = max(m, arr[i+1] - arr[i])
        ret.append((user, m, arr[-1]))
    # 1. 정답 제출 간격이 가장 큰 순서대로 정렬
    # 2. 마지막 제출이 가장 느린 순서대로 정렬
    ret.sort(key=lambda x: (-x[1], -x[2]))
    for user, m, _ in ret:
        if is_already_award(status, user):
            continue
        status.append((user, m, "정답 제출 시간간격이 가장 큰 사람"))
        break


if __name__ == "__main__":
    with open("./runs.json", "r") as f:
        data = json.load(f)
    timeline = data["runs"]
    timeline.sort(key=lambda x: x["id"])
    # print(timeline)
    print(condition1(timeline))
