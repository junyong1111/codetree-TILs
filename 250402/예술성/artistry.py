import sys
from collections import deque
from getpass import fallback_getpass

from setuptools.command.rotate import rotate

sys.setrecursionlimit(10*5)
# sys.stdin = open('input.txt', "r")
input = sys.stdin.readline

N = int(input())
grid = [list(map(int, input().split())) for _ in range(N)]
dxs = [1, 0, -1, 0]
dys = [0, 1, 0, -1]
def my_print(arr):
    for data in arr:
        print(*data)


""""
1. 그룹 만들기
"""

def is_possible(nx, ny, N):
    if nx < 0 or nx >= N :
        return False
    if ny < 0 or ny >=N:
        return False
    return True
def bfs(p, target, visit):
    q = deque()
    q.append(p)

    visit[p[1]][p[0]] = True
    point_set = set()
    point_set.add(p)

    while q:
        x, y = q.popleft()

        for dx, dy in zip(dxs, dys):
            nx = x + dx
            ny = y + dy

            if is_possible(nx, ny ,N) and visit[ny][nx] == False and grid[ny][nx] == target:
                visit[ny][nx] = True
                q.append((nx, ny))
                point_set.add((nx, ny))
    return point_set


def find_number(start, target, start_group, target_group):
    q = deque()
    visit = [[False for _ in range(N)] for _ in range(N)]
    q.append(start_group)
    visit[start_group[1]][start_group[0]] = True

    cnt = 0
    while q:
        x, y = q.popleft()
        for dx, dy in zip(dxs, dys):
            nx = x + dx
            ny = y + dy

            if is_possible(nx, ny ,N) :
                if (nx, ny) in target_group:
                    cnt +=1
                if visit[ny][nx] == False:
                    visit[ny][nx] = True
                    if grid[ny][nx] == start:
                        q.appendleft((nx, ny))
    return cnt




def get_score(number1, number2, cnt):
    ret = (number1[1] + number2[1]) *  number1[0] * number2[0] * cnt
    return ret

def _rotate(x, y, n, t):
    new_arr = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_arr[i][j] = grid[t-1-j][i]

    for i in range(n):
        for j in range(n):
            grid[i+y][j+x] = new_arr[i][j]

def _rotate_2(x, y, n, t):
    new_arr = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_arr[i][j] = grid[t-j-1][i+n+1]

    for i in range(n):
        for j in range(n):
            grid[i+y][j+x] = new_arr[i][j]


def rotate_arr():

    xarr = []
    yarr = []
    for i in range(N):
        xarr.append(grid[N//2][i])
        yarr.append(grid[i][N//2])

    for i in range(N):
        grid[N//2][i] = yarr[i]
        grid[i][N//2] = xarr[-(i+1)]

    n = N//2
    _rotate(0, 0, n, N//2)
    _rotate(0, n+1, n, N)
    #
    _rotate_2(n+1, 0, n, N // 2)
    _rotate_2(n+1,n+1, n, N)

#TODO 추후 업데이트 3으로
number_of_rotate = 4
ANSWER = 0
while number_of_rotate:
    number_of_rotate-=1
    group_list = []
    number_list = []
    visit = [[False for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if visit[i][j] == False:
                group_list.append(bfs((j, i), grid[i][j], visit))
                number_list.append([grid[i][j], 0])

    for i in range(len(group_list)):
        number_list[i][1] = len(group_list[i])
    # 모든 그룹을 순회
    for i in range(len(group_list)-1):
        for j in range(i+1, len(group_list)):
            #맞닿아 있는지 어케 확인하냐 ? 이것도 bfs
            start = number_list[i][0]
            target = number_list[j][0]


            cnt = find_number(start, target, list(group_list[i])[0], group_list[j])
            if cnt != 0:
                ANSWER += get_score(number_list[i], number_list[j], cnt)

    # 회전
    rotate_arr()




print(ANSWER)

