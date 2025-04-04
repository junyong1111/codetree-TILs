import sys
from collections import deque
sys.setrecursionlimit(10**5)
# sys.stdin = open('input.txt', "r")
input = sys.stdin.readline

dxs = [1, 0, -1, 0]
dys = [0, 1, 0, -1]

ddxs = [1, 1, -1, -1]
ddys = [-1, 1, 1, -1]

SIZE, YEAR, AREA, REMAIN = map(int, input().split())
REMAIN += 100
ANSWER = 0


GRID = [list(map(int, input().split())) for _ in range(SIZE)]

def pprint(arr):
    for data in arr:
        print(*data)



def is_possible(nx, ny):
    if nx < 0 or nx >= SIZE:
        return False
    if ny < 0 or ny >= SIZE:
        return False
    return True
def growup_tree():
    for i in range(SIZE):
        for j in range(SIZE):
            cnt = 0
            if GRID[i][j] > 0 :
                for dx, dy in zip(dxs, dys):
                    nx = j + dx
                    ny = i + dy
                    if is_possible(nx, ny) and GRID[ny][nx] > 0:
                        cnt +=1
                GRID[i][j] += cnt

def bfs(tree):
    visit = [[False] * SIZE for _ in range(SIZE)]
    target = []
    x, y = tree
    visit[y][x] = True
    cnt = 0

    for dx, dy in zip(dxs, dys):
        nx = x + dx
        ny = y + dy
        if is_possible(nx, ny) and GRID[ny][nx] == 0 and visit[ny][nx] == False :
            visit[ny][nx] = True
            target.append((nx ,ny))
            cnt +=1
    return cnt, target

def expand_tree():
    num_list = []
    target_list = []
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] <= 0:
                continue
            tree = (j, i)
            cnt, target = bfs(tree)
            if cnt == 0:
                continue
            num = GRID[i][j] // cnt

            num_list.append(num)
            target_list.append(target)

    for  ii in range(len(target_list)):
        target = target_list[ii]
        for t in target:
            x, y = t
            GRID[y][x] += num_list[ii]




def _get_area(p):
    x, y = p
    cnt = GRID[y][x]
    arr_list =[(x, y)]

    for ddx, ddy in zip(ddxs, ddys):
        nx, ny = x, y
        for k in range(AREA):
            nx, ny = nx + ddx, ny + ddy
            if is_possible(nx, ny):
                if GRID[ny][nx] == -1:
                    break
                arr_list.append((nx, ny))
                if GRID[ny][nx]  == 0:
                    break
                cnt += GRID[ny][nx]

    return cnt, arr_list




def find_area():
    max_area = 0
    point = (0, 0)
    area_list = []
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] > 0:
                cnt, temp = _get_area((j, i))
                if cnt > max_area:
                    max_area = cnt
                    point = (j, i)
                    area_list = temp
    return point, area_list


def remove_tree(arr):
    ret = 0
    for i in range(len(arr)):
        x, y =  arr[i]
        ret += GRID[y][x]
        GRID[y][x] = -REMAIN
    return ret




def remove_arr():
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] < -2:
                GRID[i][j] +=1

            if GRID[i][j] > -100 and GRID[i][j] < -2:
                GRID[i][j] = 0

while YEAR:
    YEAR-=1
    #1.
    growup_tree()

    #2. 번식
    expand_tree()
    #3.제초제 위치 찾기
    p, arr = find_area()

    # 제초제 뿌리기
    ANSWER += remove_tree(arr)

    # 제초제 수명 감소
    remove_arr()

print(ANSWER)

