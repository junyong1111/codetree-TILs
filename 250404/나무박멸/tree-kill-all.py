import sys
sys.setrecursionlimit(10**5)
input = sys.stdin.readline

# 방향: 상우하좌
dxs = [1, 0, -1, 0]
dys = [0, 1, 0, -1]

# 대각선 방향 (제초제 확산용)
ddxs = [1, 1, -1, -1]
ddys = [-1, 1, 1, -1]

SIZE, YEAR, AREA, c = map(int, input().split())
ANSWER = 0

# GRID: 나무 배열 (벽은 -1)
GRID = [list(map(int, input().split())) for _ in range(SIZE)]
# HERB: 제초제 효과 배열 (0이면 제초제 없음)
HERB = [[0]*SIZE for _ in range(SIZE)]

def is_possible(nx, ny):
    return 0 <= nx < SIZE and 0 <= ny < SIZE

def growup_tree():
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] > 0:
                cnt = 0
                for dx, dy in zip(dxs, dys):
                    nx, ny = j + dx, i + dy
                    if is_possible(nx, ny) and GRID[ny][nx] > 0:
                        cnt += 1
                GRID[i][j] += cnt

def bfs(tree):
    visit = [[False]*SIZE for _ in range(SIZE)]
    target = []
    x, y = tree
    visit[y][x] = True
    cnt = 0
    for dx, dy in zip(dxs, dys):
        nx, ny = x + dx, y + dy
        # 번식 가능: 빈 칸(0)이고 제초제 없음 (HERB==0)
        if is_possible(nx, ny) and GRID[ny][nx] == 0 and HERB[ny][nx] == 0 and not visit[ny][nx]:
            visit[ny][nx] = True
            target.append((nx, ny))
            cnt += 1
    return cnt, target

def expand_tree():
    num_list = []
    target_list = []
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] <= 0:
                continue
            pos = (j, i)
            cnt, targets = bfs(pos)
            if cnt == 0:
                continue
            num = GRID[i][j] // cnt
            num_list.append(num)
            target_list.append(targets)
    for idx in range(len(target_list)):
        for (x, y) in target_list[idx]:
            GRID[y][x] += num_list[idx]

def _get_area(p):
    x, y = p
    cnt = GRID[y][x]
    arr_list = [(x, y)]
    for ddx, ddy in zip(ddxs, ddys):
        nx, ny = x, y
        for k in range(AREA):
            nx, ny = nx + ddx, ny + ddy
            if not is_possible(nx, ny):
                break
            if GRID[ny][nx] == -1:  # 벽이면 중단
                break
            arr_list.append((nx, ny))
            if GRID[ny][nx] <= 0:  # 빈 칸 또는 제초제 효과 있는 칸이면 중단
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

def remove_tree(area):
    ret = 0
    for (x, y) in area:
        ret += GRID[y][x]
        GRID[y][x] = 0
        HERB[y][x] = c  # 제초제 효과를 c년 동안 유지
    return ret

# 매 해마다 HERB 배열 업데이트: 남은 제초제 효과를 1씩 감소시킴
def update_herb():
    for i in range(SIZE):
        for j in range(SIZE):
            if HERB[i][j] > 0:
                HERB[i][j] -= 1

# 시뮬레이션 진행
for _ in range(YEAR):
    # 1. 나무 성장
    growup_tree()
    # 2. 나무 번식
    expand_tree()
    # 3. 제초제 효과 업데이트 (번식 후, 제초제 효과 감소)
    update_herb()
    # 4. 제초제 적용: 최대 효과 칸 찾기
    p, area = find_area()
    # 제거할 나무가 없다면 종료
    if not area or all(GRID[y][x] <= 0 for (x, y) in area):
        break
    ANSWER += remove_tree(area)

print(ANSWER)
