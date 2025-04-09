import sys
from collections import deque
sys.setrecursionlimit(10**5)
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline

LEGACY_NUMBER = 2
ANSWER = [0, 0, 0]
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return(
f"""[좌표]
Y {self.y} X {self.x}
""")
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

N = 5

K, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
WALL = list(map(int, input().split()))

def my_print(arr):
    print("==[INFO 시작]==")
    for data in arr:
        print(*data)
    print("==[INFO 끝]==")

def is_possible(nx, ny):
    if (nx < 0 or nx >=N) or (ny < 0 or ny >=N):
        return False
    return True

def bfs(p, arr, visit):
    dxs = [0, 1, 0, -1]
    dys = [1, 0, -1, 0]

    x, y = p.x, p.y
    q = deque()
    q.append((x, y))
    visit[y][x] = True

    target = arr[y][x]
    cnt = 1
    legacy_list = [Point(x, y)]

    while q:
        x, y = q.popleft()
        for dx, dy in zip(dxs, dys):
            nx, ny = x + dx, y + dy
            if is_possible(nx, ny) and visit[ny][nx] == False and arr[ny][nx] == target:
                visit[ny][nx] = True
                cnt+=1
                legacy_list.append(Point(nx, ny))
                q.append((nx, ny))
    if cnt >= 3:
        return legacy_list
    return None

def replace_legacy(
    remove_list,
    arr,
    de = False,
):
    remove_list.sort(
        key=lambda x : (x.x, -x.y)
    )
    for remove in remove_list:
        x, y = remove.x, remove.y
        arr[y][x] = WALL[ANSWER[LEGACY_NUMBER]]
        ANSWER[LEGACY_NUMBER] = (ANSWER[LEGACY_NUMBER]+1)%M
    return arr

def get_first_legacy(
        arr,
        de = False,
):
    cnt = 0
    visit = [[False for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if visit[i][j] == False:
                ret = bfs(Point(j, i), arr, visit)
                if not ret:
                    if de:
                        print("유물 3개 안됨 ㅋ")
                else:
                    if de:
                        print(f"{len(ret)}개 찾음 ㅋ")
                    cnt += len(ret)
    if de:
        print(f"{cnt}개 유물 점수 획득 삭제함요")
    return cnt

def get_legacy(
    arr,
    de = False
):
    copy_arr = [x[:] for x in arr]
    cnt = 0
    while True:
        visit = [[False for _ in range(N)] for _ in range(N)]
        remove_list = []
        for i in range(N):
            for j in range(N):
                if visit[i][j] == False:
                    ret = bfs(Point(j, i), copy_arr, visit)
                    if not ret:
                        if de:
                            print("유물 3개 안됨 ㅋ")
                    else:
                        if de:
                            print(f"{len(ret)}개 찾음 ㅋ")
                        remove_list.extend(ret)
                        cnt += len(ret)
        if len(remove_list) == 0:
            return cnt, copy_arr
        if de:
            print(f"{cnt}개 유물 점수 획득 삭제함요")
        copy_arr = replace_legacy(de= de, remove_list=remove_list, arr=copy_arr)


def rotate_map(
        p,
        de = False
):
    # 미리 복사
    copy_arr =  [x[:] for x in grid]
    x, y = p.x-1, p.y-1 #(시작 좌표는 왼쪽 대각선으로 가야함)

    new_arr = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            new_arr[i][j] = copy_arr[3 - 1 - j + y][i + x]
    for i in range(3):
        for j in range(3):
            copy_arr[y + i][x + j] = new_arr[i][j]

    #유물 획득
    legacy_cnt= get_first_legacy(copy_arr,  de)
    return legacy_cnt, copy_arr


def find_grid(
        de = False
):
    max_value = -sys.maxsize
    max_rotate_grid = []
    for k in range(3):
        for i in range(1, N-1):
            for j in range(1, N-1):
                center = Point(j, i)
                if de:
                    print(f"[중심좌표 설정]{center}")
                legacy_cnt,  rotate_grid= rotate_map(
                    center,
                    de = de
                )
                if max_value  < legacy_cnt:
                    max_value = legacy_cnt
                    max_rotate_grid = rotate_grid
    return max_value, max_rotate_grid

while K:
    K-=1
    v, rotate_grid = find_grid(
        de = False
    )
    copy_grid = [x[:] for x in rotate_grid]

    cnt, arr = get_legacy(arr=rotate_grid)
    grid = [x[:] for x in arr]
    if cnt != 0:
        print(cnt, end=" ")


