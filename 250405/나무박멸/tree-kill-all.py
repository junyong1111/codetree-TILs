import sys
from ast import increment_lineno

sys.setrecursionlimit(10**6)
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline

dxs = [1, 0, -1 ,0]
dys = [0, 1, 0, -1]

tdxs = [1, 1, -1, -1 ]
tdys = [-1, 1, 1, -1]

N, M, K, c = map(int, input().split())
WALL_LIST = []

grid = [list(map(int , input().split())) for _ in range(N)]

def my_print(arr):
    for data in arr:
        print(*data)
    print(" ---------  print ---------")


def map_print(arr):
    for i in range(len(arr)):
        for ii in range(len(arr)):
            if grid[i][ii] == -1 and (ii, i) in WALL_LIST:
                print(f"{grid[i][ii]} 벽임", end= " ")
            else:
                print(grid[i][ii], end= " ")
        print()

def init():
    for i in range(N):
        for ii in range(N):
            if grid[i][ii] == -1:
                WALL_LIST.append((ii, i))

def is_possible(nx ,ny):
    if (nx < 0 or nx >= N) or (ny < 0 or ny>=N):
        return False
    return True

def grow_up_tree():
    narr = [x[::] for x in grid]
    for i in range(N):
        for ii in range(N):
            cnt = 0
            if grid[i][ii] > 0: #해당 위차가 나무라면 4방향에서 몇 개가 있는지 확인
                for dx, dy in zip(dxs, dys):
                    nx = ii + dx
                    ny = i + dy

                    if is_possible(nx, ny) and grid[ny][nx] > 0: # 근처에 나무라면
                        cnt +=1
            narr[i][ii] += cnt
    return narr


def increment_tree():
    narr = [x[::] for x in grid]
    for i in range(N):
        for ii in range(N):
            cnt = 0
            target_list = []
            if grid[i][ii] > 0:
                for dx, dy in zip(dxs, dys):
                    nx = dx + ii
                    ny = dy + i

                    if is_possible(nx ,ny) and grid[ny][nx] == 0: #빈 자리라면
                        target_list.append((nx, ny))
                        cnt +=1
            if cnt == 0:
                continue
            val = grid[i][ii] // cnt
            for target in target_list:
                x, y = target
                narr[y][x] += val
    return narr

def get_area(p):
    nx, ny = p
    cnt = grid[ny][nx] # 자기 자신 더해주고
    target_list = [(nx, ny)]

    # x, y = 1, 0

    for tdx, tdy in zip(tdxs, tdys):
        nx ,ny = p
        for k in range(K):
            nx = nx + tdx
            ny = ny + tdy

            if is_possible(nx, ny):
                #1. 나무인 경우 추가
                if grid[ny][nx] > 0 :
                    target_list.append((nx, ny))
                    cnt += grid[ny][nx]
                elif grid[ny][nx] == -1 and (nx ,ny) in WALL_LIST:
                    #벽인경우 종료
                    break
                elif grid[ny][nx]  == 0 : #벽인 경우 제초제 뿌리고 종료
                    target_list.append((nx, ny))
                    break
                elif grid[ny][nx] < 0 : #만약 제초제가 있는 경우에는 ? 마찬가지로
                    target_list.append((nx, ny))
                    break
            else:
                break
    return cnt, target_list


def get_location():
    max_cnt = 0
    target_list = []
    for i in range(N):
        for ii in range(N):
            if grid[i][ii] > 0 : #나무 위치라면 제초제 뿌려보잡
                cnt, target = get_area((ii, i))
                if cnt != 0 and max_cnt < cnt:
                    max_cnt = cnt
                    target_list = target
    return target_list


def update_tree(target_list):
    ret = 0
    for target in target_list:
        x, y = target
        if grid[y][x] > 0: #만약 나무라면 박멸
            ret += grid[y][x]
            grid[y][x] = -(c+1) #제초제 뿌리기
        elif grid[y][x] <= 0 and (x, y) not in WALL_LIST: # 땅이거나, 이미 제초제가 있는 곳이라면 갱신
            grid[y][x] = -(c+1)
    return ret

def update_year():
    for i in range(N):
        for ii in range(N):
            if grid[i][ii] < 0 and (ii, i) not in WALL_LIST:
                grid[i][ii] +=1


init()
answer = 0
while M:
    M-=1
    # 1. 성장
    grid = grow_up_tree()
    # 2. 번식
    grid = increment_tree()

    # 3 .제초제 위치 찾기
    target_list = get_location()

    #4. 제초제 확산
    answer += update_tree(target_list)
    #5 제초제 남은 기간 감소
    update_year()
print(answer)



