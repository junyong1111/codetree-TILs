import sys
from collections import deque

# 우상좌하
dxs= [1, 0, -1, 0]
dys =[0, -1, 0, 1]

class Guide():
    def __init__(self, p, sub_p, main_p):
        self.point = p
        self.main_p = main_p
        self.sub_p = sub_p


sys.setrecursionlimit(10**6)
input = sys.stdin.readline

N, M, K = map(int, input().split())


grid = [list(map(int, input().split())) for _ in range(N)]
guides =[
    # x, y
    Guide((0, 0), (1, 0), (0, 1)),
    Guide((0, N-1), (0, -1), (1, 0)),
    Guide((N-1, 0), (-1, 0), (0, 1)),
    Guide((N-1, 0), (0, 1), (1, 0)),
]

def pprint(arr):
    for data in arr:
        print(*data)


def is_possible(nx, ny, N):
    if nx < 0 or nx >= N:
        return False
    if ny < 0 or ny >= N:
        return False
    return True

def make_team(p):
    team = deque()
    team.append(p)
    #머리는 미리 등록
    grid[p[1]][p[0]] = 4
    q = deque()
    q.append(p)

    while q:
        x, y = q.pop()

        for dx,dy in zip(dxs, dys):
            nx = x + dx
            ny = y + dy

            if is_possible(nx, ny, N):
                if grid[ny][nx] == 2:
                    team.append((nx, ny))
                    grid[ny][nx] = 4
                    q.append((nx, ny))
                elif grid[ny][nx] ==3:
                    team.append((nx, ny))
                    grid[ny][nx] = 4
                    break
    return team

#1. 팀 만들기
team_list = []
for i in range(N):
    for j in range(N):
        if grid[i][j] == 1:
            team = (make_team((j, i)))
            team_list.append(team)

cnt = -1
_dir = 0
answer = 0
x, y = guides[_dir].point

while K:
    K-=1
    cnt+=1
    # 2. 팀 이동
    for team in team_list:
        head = team[0]

        for dx, dy in zip(dxs, dys):
            nx = head[0] + dx
            ny = head[1] + dy

            if is_possible(nx, ny, N) and grid[ny][nx] == 4 and (nx, ny) not in team:
                team.appendleft((nx, ny))
                team.pop()
    # 공 던지기
    # 기준 좌표
    nx, ny = x, y
    is_hit = False
    for i in range(N):
        #던져
        for team in team_list:
            for ii in range(len(team)):
                if (nx, ny) == team[ii]:
                    answer += ((ii+1) * (ii+1))
                    new_team = reversed(team)
                    teamp = new_team
                    is_hit = True
                    break
            if is_hit:
                break
        if is_hit:
            break
        #맞은애가 잇다면 점수 올리고 머리 방향 체인지

        #한 번 던지고 나면 방향으로 전진
        nx = nx + guides[_dir].sub_p[0]
        ny = ny + guides[_dir].sub_p[1]

    if cnt == N:
        cnt = 0
        _dir = (_dir + 1) %4
        x, y = guides[_dir].point
    else:
        x = x + guides[_dir].main_p[0]
        y = y + guides[_dir].main_p[1]

print(answer)