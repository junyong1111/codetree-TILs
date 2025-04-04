import sys
from collections import deque
sys.setrecursionlimit(10**5)
input = sys.stdin.readline

dxs = [1, 0, -1, 0]
dys = [0, 1, 0, -1]

ddxs = [1, 1, -1, -1]
ddys = [-1, 1, 1, -1]

SIZE, YEAR, AREA, REMAIN = map(int, input().split())
REMAIN += 1  # 제초제 지속 기간 (문제에 따라 +1 또는 그대로 사용)
ANSWER = 0

GRID = [list(map(int, input().split())) for _ in range(SIZE)]

def is_possible(nx, ny):
    return 0 <= nx < SIZE and 0 <= ny < SIZE

def growup_tree():
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] > 0:  # 나무가 있는 칸
                cnt = 0
                for dx, dy in zip(dxs, dys):
                    nx, ny = j + dx, i + dy
                    if is_possible(nx, ny) and GRID[ny][nx] > 0:
                        cnt += 1
                GRID[i][j] += cnt

def expand_tree():
    growth = [[0] * SIZE for _ in range(SIZE)]
    
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] <= 0:  # 나무가 없는 칸은 무시
                continue
                
            tree_power = GRID[i][j]
            empty_cells = []
            
            # 상하좌우 빈 칸 찾기
            for dx, dy in zip(dxs, dys):
                nx, ny = j + dx, i + dy
                if is_possible(nx, ny) and GRID[ny][nx] == 0:
                    empty_cells.append((nx, ny))
            
            # 번식할 빈 칸이 없으면 넘어감
            if not empty_cells:
                continue
                
            # 각 빈 칸에 나무 번식
            growth_per_cell = tree_power // len(empty_cells)
            for nx, ny in empty_cells:
                growth[ny][nx] += growth_per_cell
    
    # 동시에 번식 적용
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] == 0:  # 빈 칸에만 번식
                GRID[i][j] += growth[i][j]

def _get_area(x, y):
    cnt = GRID[y][x]  # 현재 위치의 나무 수
    affected_cells = [(x, y)]  # 제초제 영향받는 칸
    
    # 4개 대각선 방향으로 탐색
    for ddx, ddy in zip(ddxs, ddys):
        nx, ny = x, y
        for k in range(1, AREA + 1):  # 1칸부터 k칸까지 (0번째는 시작점이므로 제외)
            nx, ny = nx + ddx, ny + ddy
            
            # 범위를 벗어나면 해당 방향 탐색 중단
            if not is_possible(nx, ny):
                break
                
            # 벽을 만나면 해당 방향 탐색 중단
            if GRID[ny][nx] == -1:
                break
                
            affected_cells.append((nx, ny))
            
            # 나무가 있는 경우 제거할 나무 수에 추가
            if GRID[ny][nx] > 0:
                cnt += GRID[ny][nx]
                
            # 빈 칸을 만나면 해당 방향 탐색 중단
            if GRID[ny][nx] == 0:
                break
    
    return cnt, affected_cells

def find_area():
    max_trees = 0
    best_point = None
    best_cells = []
    
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] > 0:  # 나무가 있는 칸에만 제초제 뿌림
                trees, affected_cells = _get_area(j, i)
                if trees > max_trees:
                    max_trees = trees
                    best_point = (j, i)
                    best_cells = affected_cells
    
    if best_point is None:  # 나무가 없는 경우
        return (0, 0), []
        
    return best_point, best_cells

def remove_tree(affected_cells):
    removed = 0
    
    for x, y in affected_cells:
        if GRID[y][x] > 0:  # 나무가 있는 칸
            removed += GRID[y][x]
        GRID[y][x] = -REMAIN  # 제초제 표시
    
    return removed

def decrease_herbicide():
    for i in range(SIZE):
        for j in range(SIZE):
            if GRID[i][j] < 0 and GRID[i][j] != -1:  # 제초제가 있고 벽이 아닌 칸
                GRID[i][j] += 1  # 제초제 수명 감소
                
# 시뮬레이션 시작
for _ in range(YEAR):
    # 1. 나무 성장
    growup_tree()
    
    # 2. 나무 번식
    expand_tree()
    
    # 3. 제초제 위치 결정 및 뿌리기
    point, affected_cells = find_area()
    ANSWER += remove_tree(affected_cells)
    
    # 4. 제초제 수명 감소
    decrease_herbicide()

print(ANSWER)