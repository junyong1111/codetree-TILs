import sys
from collections import deque

sys.setrecursionlimit(10**5)
# 파일 입력을 사용하는 경우 (제출 시 주석 처리 필요)
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline

N = 5  # 그리드 크기는 항상 5x5

# 입력 처리
K, M = map(int, input().split())  # K: 턴 수, M: 유물 개수
grid = [list(map(int, input().split())) for _ in range(N)]  # 5x5 맵
artifacts = list(map(int, input().split()))  # 추가될 유물 번호 목록

artifact_idx = 0  # 현재 사용할 유물 인덱스

# 좌표 클래스 정의
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# 맵 범위 확인 함수
def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N

# BFS로 연결된 같은 값의 유물 찾기
def bfs(x, y, arr, visited):
    value = arr[y][x]
    queue = deque([(x, y)])
    visited[y][x] = True
    connected = [Point(x, y)]
    
    dx = [0, 1, 0, -1]  # 동, 남, 서, 북
    dy = [1, 0, -1, 0]
    
    while queue:
        cx, cy = queue.popleft()
        
        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            if is_valid(nx, ny) and not visited[ny][nx] and arr[ny][nx] == value:
                visited[ny][nx] = True
                queue.append((nx, ny))
                connected.append(Point(nx, ny))
    
    # 3개 이상 연결된 경우에만 반환
    if len(connected) >= 3:
        return connected
    return None

# 90도 회전 함수
def rotate_90(arr, center_x, center_y):
    # 깊은 복사
    result = [row[:] for row in arr]
    
    # 중심점에서 3x3 영역 회전
    x, y = center_x - 1, center_y - 1  # 회전 영역의 시작점
    
    # 임시 배열에 회전 결과 저장
    temp = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            # 90도 시계방향 회전: (i,j) -> (j,2-i)
            temp[j][2-i] = arr[y+i][x+j]
    
    # 결과 배열에 회전 영역 복사
    for i in range(3):
        for j in range(3):
            result[y+i][x+j] = temp[i][j]
            
    return result

# 특정 각도로 회전 (1: 90도, 2: 180도, 3: 270도)
def rotate_map(arr, center_x, center_y, angle):
    result = [row[:] for row in arr]
    
    for _ in range(angle):
        result = rotate_90(result, center_x, center_y)
        
    return result

# 유물 평가 함수 - 제거 가능한 유물 개수 계산
def evaluate_artifacts(arr):
    count = 0
    visited = [[False for _ in range(N)] for _ in range(N)]
    
    for y in range(N):
        for x in range(N):
            if not visited[y][x]:
                connected = bfs(x, y, arr, visited)
                if connected:
                    count += len(connected)
    
    return count

# 최적의 회전을 찾는 함수
def find_best_rotation(arr):
    max_count = 0
    best_grid = None
    best_angle = 0
    best_center_x = 0
    best_center_y = 0
    
    # 우선순위: 제거 유물 수 > 각도 > 열(col) > 행(row)
    for angle in range(1, 4):  # 1: 90도, 2: 180도, 3: 270도
        for center_y in range(1, 4):  # 중심점 y 좌표 (1~3)
            for center_x in range(1, 4):  # 중심점 x 좌표 (1~3)
                rotated_grid = rotate_map(arr, center_x, center_y, angle)
                count = evaluate_artifacts(rotated_grid)
                
                if (count > max_count or 
                    (count == max_count and angle < best_angle) or
                    (count == max_count and angle == best_angle and center_x < best_center_x) or
                    (count == max_count and angle == best_angle and center_x == best_center_x and center_y < best_center_y)):
                    max_count = count
                    best_grid = rotated_grid
                    best_angle = angle
                    best_center_x = center_x
                    best_center_y = center_y
    
    return max_count, best_grid

# 유물 제거 및 점수 계산 함수
def remove_artifacts(arr):
    global artifact_idx
    
    total_score = 0
    current_grid = [row[:] for row in arr]
    
    while True:
        visited = [[False for _ in range(N)] for _ in range(N)]
        all_connected = []
        
        # 모든 연결된 그룹 찾기
        for y in range(N):
            for x in range(N):
                if not visited[y][x]:
                    connected = bfs(x, y, current_grid, visited)
                    if connected:
                        all_connected.extend(connected)
        
        # 제거할 유물이 없으면 종료
        if not all_connected:
            break
        
        # 점수 계산
        total_score += len(all_connected)
        
        # 유물 제거 및 새 유물로 채우기
        # 열을 기준으로 정렬하여 처리
        all_connected.sort(key=lambda p: (p.x, -p.y))
        
        for point in all_connected:
            x, y = point.x, point.y
            # 제거된 위치에 새 유물 채우기
            current_grid[y][x] = artifacts[artifact_idx]
            artifact_idx = (artifact_idx + 1) % M
    
    return total_score, current_grid

# 메인 함수
def solve():
    global grid, artifact_idx
    
    results = []
    
    for _ in range(K):
        # 1. 최적의 회전 찾기
        _, rotated_grid = find_best_rotation(grid)
        
        # 회전된 맵이 없으면 (모든 회전에서 제거할 유물이 없으면) 그대로 진행
        if rotated_grid is None:
            rotated_grid = [row[:] for row in grid]
        
        # 2. 유물 제거 및 점수 계산
        score, new_grid = remove_artifacts(rotated_grid)
        
        # 3. 결과 저장
        if score > 0:
            results.append(score)
        
        # 4. 다음 턴을 위해 맵 업데이트
        grid = new_grid
    
    # 결과 출력
    print(" ".join(map(str, results)))

# 실행
solve()