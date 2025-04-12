import sys
import threading

MAXN = 20
MAXM = 20
MAXF = 400
MAXP = MAXF*6

INF = int(1e9+10)

SpaceMap = [[0 for _ in range(MAXN+10)] for _ in range(MAXN+10)]  # 미지의 공간의 평면도
SpaceMapCellId = [[0 for _ in range(MAXN+10)] for _ in range(MAXN+10)]  # 평면도의 각 셀에 대응하는 그래프 정점의 번호를 저장하는 배열
TimeWall = [[[0 for _ in range(MAXM+10)] for _ in range(MAXM+10)] for _ in range(6)]  # 시간의 벽의 단면도
TimeWallCellId = [[[0 for _ in range(MAXM+10)] for _ in range(MAXM+10)] for _ in range(6)]  # 시간의 벽의 단면도의 각 셀에 대응하는 그래프 정점의 번호를 저장하는 배열

# 시간 이상 현상에 대한 정보를 저장할 클래스
class AbnormalTimeEvent:
    # 시간 이상 현상이 시작점의 행번호, 열번호, 방향, 확장 주기, 시간 이상 현상의 진행여부를 차례로 저장합니다
    def __init__(self, xpos=0, ypos=0, direction=0, cycle=0, alive=0):
        self.xpos = xpos
        self.ypos = ypos
        self.direction = direction
        self.cycle = cycle
        self.alive = alive

events = [AbnormalTimeEvent() for _ in range(MAXF+10)]

# 그래프를 저장할 인접리스트
Graph = []

# 그래프 생성 함수
def build_graph(N, M):
    global Graph, SpaceMapCellId, TimeWallCellId
    cnt = 0

    # 각 셀에 대해 대응될 번호를 차례로 부여합니다
    # 평면도 중 시간의 벽이 아닌 부분의 셀들을 순회한 후,
    # 단면도에 속하는 셀들을 단면도의 동쪽 -> 남쪽 -> 서쪽 -> 북쪽 -> 위쪽 순으로 셀들을 순회하면서 번호를 부여합니다
    for i in range(N):
        for j in range(N):
            if SpaceMap[i][j] != 3:  # 시간의 벽이 있는 셀이 아닌 경우에만 번호를 부여합니다
                cnt += 1
                SpaceMapCellId[i][j] = cnt

    # 단면도의 동쪽, 남쪽, 서쪽, 북쪽, 위쪽 순으로 순회하며 셀에 번호를 부여합니다
    for t in range(5):
        for i in range(M):
            for j in range(M):
                cnt += 1
                TimeWallCellId[t][i][j] = cnt

    # 부여한 번호의 정점들로 구성된 그래프
    # 정점의 번호에 대응되는 셀과 인접한 셀의 번호를 가지는 정점과 간선으로 연결합니다
    # 최대 4개의 정점과 연결될 수 있습니다
    # 평면도(단면도)에서, 오른쪽으로 인접한 경우 0, 아래쪽으로 인접한 경우 1, 왼쪽으로 인접한 경우 2, 위쪽으로 인접한 경우 3의 인덱스에 저장합니다
    Graph = [[-1 for _ in range(4)] for _ in range(cnt+1)]

    # 간선을 추가하는 작업을 위해 사용할 dx, dy 배열
    # 동, 남, 서, 북에 대응되는 순서로 채워져 있습니다
    dx = [0, 1, 0, -1]  # 동, 남, 서, 북
    dy = [1, 0, -1, 0]

    # 평면도에 속하는 셀에 대응되는 번호의 정점 쌍에 대해 간선을 추가합니다
    for i in range(N):
        for j in range(N):
            if SpaceMap[i][j] != 3:  # 현재 셀에 장애물이 없는 경우
                idx = SpaceMapCellId[i][j]
                # 동, 남, 서, 북 순으로 인접한 셀들을 탐색합니다
                for dd in range(4):
                    nx = i + dx[dd]
                    ny = j + dy[dd]
                    # 범위를 벗어나면 넘어갑니다
                    if nx < 0 or ny < 0 or nx >= N or ny >= N:
                        continue
                    # 셀에 장애물이 있는 경우 넘어갑니다
                    if SpaceMap[nx][ny] == 3:
                        continue
                    # 그렇지 않은 경우, 이어줍니다
                    Graph[idx][dd] = SpaceMapCellId[nx][ny]

    # 단면도의 동쪽, 남쪽, 서쪽, 북쪽에 있는 셀들이 인접할 경우
    # 대응되는 번호의 정점들을 이어줍니다
    for t in range(4):
        for i in range(M):
            for j in range(M):
                idx = TimeWallCellId[t][i][j]
                # 위와 비슷하게 4방향 탐색
                for dd in range(4):
                    nx = i + dx[dd]
                    ny = j + dy[dd]
                    # 행 범위가 넘어갔을 경우 통과
                    if nx < 0 or nx >= M:
                        continue
                    # 열 번호가 0보다 작아질 경우, 시계방향순으로 하나 앞에 있는 단면도의 가장 오른쪽 열의 셀과 인접합니다
                    if ny < 0:
                        Graph[idx][dd] = TimeWallCellId[(t+1)%4][nx][M-1]
                    elif ny >= M:
                        Graph[idx][dd] = TimeWallCellId[(t+3)%4][nx][0]
                    else:
                        Graph[idx][dd] = TimeWallCellId[t][nx][ny]

    # 위쪽 단면도에 속하는 셀들에 대응되는 번호의 정점 쌍에 대해 간선을 추가합니다
    for i in range(M):
        for j in range(M):
            idx = TimeWallCellId[4][i][j]
            for dd in range(4):
                nx = i + dx[dd]
                ny = j + dy[dd]
                # 범위를 벗어날 경우 넘어갑니다
                if nx < 0 or ny < 0 or nx >= M or ny >= M:
                    continue
                # 그렇지 않을 경우 이어줍니다
                Graph[idx][dd] = TimeWallCellId[4][nx][ny]

    # 위쪽 단면도와 인접한 동쪽, 남쪽, 서쪽, 북쪽 단면도의 셀들에 대해
    # 대응되는 번호의 정점을 잇는 간선을 추가합니다
    # 동쪽 단면도와 인접한 셀들의 경우
    for i in range(M):
        idx = TimeWallCellId[4][i][M-1]  # 인접한 위쪽 단면도의 셀의 번호
        idy = TimeWallCellId[0][0][M-1 - i]  # 인접한 동쪽 단면도의 셀의 번호
        Graph[idx][0] = idy
        Graph[idy][3] = idx
    # 남쪽 단면도와 인접한 셀들의 경우
    for i in range(M):
        idx = TimeWallCellId[4][M-1][i]  # 인접한 위쪽 단면도의 셀의 번호
        idy = TimeWallCellId[1][0][i]  # 인접한 남쪽 단면도의 셀의 번호
        Graph[idx][1] = idy
        Graph[idy][3] = idx
    # 서쪽 단면도와 인접한 셀들의 경우
    for i in range(M):
        idx = TimeWallCellId[4][i][0]  # 인접한 위쪽 단면도의 셀의 번호
        idy = TimeWallCellId[2][0][i]  # 인접한 서쪽 단면도의 셀의 번호
        Graph[idx][2] = idy
        Graph[idy][3] = idx
    # 북쪽 단면도와 인접한 셀들의 경우
    for i in range(M):
        idx = TimeWallCellId[4][0][i]  # 인접한 위쪽 단면도의 셀의 번호
        idy = TimeWallCellId[3][0][M-1 - i]  # 인접한 북쪽 단면도의 셀의 번호
        Graph[idx][3] = idy
        Graph[idy][3] = idx

    # 평면도에서 시간의 벽이 시작하는 셀의 행 번호, 열 번호
    timewallStartx = -1
    timewallStarty = -1

    # 평면도에서 시간의 벽이 시작하는 셀의 위치를 탐색
    for i in range(N):
        for j in range(N):
            if SpaceMap[i][j] == 3:
                timewallStartx = i
                timewallStarty = j
                break
        if timewallStartx != -1:
            break

    # 평면도와 인접하는 단면도 셀들에 대응되는 번호의 정점을 잇는 간선 추가
    # 동쪽 단면도의 경우
    if timewallStarty + M < N:
        for i in range(M):
            idx = TimeWallCellId[0][M-1][i]
            idy = SpaceMapCellId[timewallStartx + (M - 1) - i][timewallStarty + M]
            Graph[idx][1] = idy
            Graph[idy][2] = idx
    # 남쪽 단면도의 경우
    if timewallStartx + M < N:
        for i in range(M):
            idx = TimeWallCellId[1][M-1][i]
            idy = SpaceMapCellId[timewallStartx + M][timewallStarty + i]
            Graph[idx][1] = idy
            Graph[idy][3] = idx
    # 서쪽 단면도의 경우
    if timewallStarty > 0:
        for i in range(M):
            idx = TimeWallCellId[2][M-1][i]
            idy = SpaceMapCellId[timewallStartx + i][timewallStarty - 1]
            Graph[idx][1] = idy
            Graph[idy][0] = idx
    # 북쪽 단면도의 경우
    if timewallStartx > 0:
        for i in range(M):
            idx = TimeWallCellId[3][M-1][i]
            idy = SpaceMapCellId[timewallStartx - 1][timewallStarty + (M -1) - i]
            Graph[idx][1] = idy
            Graph[idy][1] = idx

    return cnt

N, M, E = map(int, input().split())

# 공간의 평면도 입력
for i in range(N):
    SpaceMap[i][:N] = list(map(int, input().split()))

# 시간의 벽의 동쪽 단면도 입력
for i in range(M):
    TimeWall[0][i][:M] = list(map(int, input().split()))

# 시간의 벽의 서쪽 단면도 입력
# 구현의 편의를 위해서 TimeWall[2][][]에 서쪽 단면도 정보 저장
for i in range(M):
    TimeWall[2][i][:M] = list(map(int, input().split()))

# 시간의 벽의 남쪽 단면도 입력
# 구현의 편의를 위해서 TimeWall[1][][]에 남쪽 단면도 정보 저장
for i in range(M):
    TimeWall[1][i][:M] = list(map(int, input().split()))

# 시간의 벽의 북쪽 단면도 입력
for i in range(M):
    TimeWall[3][i][:M] = list(map(int, input().split()))

# 시간의 벽의 위쪽 단면도 입력
for i in range(M):
    TimeWall[4][i][:M] = list(map(int, input().split()))

# 시간 이상 현상에 대한 정보 입력
for i in range(1, E+1):
    x, y, direction, cycle = map(int, input().split())
    events[i].xpos = x
    events[i].ypos = y
    events[i].direction = direction
    events[i].cycle = cycle
    if events[i].direction == 1:
        events[i].direction = 2
    elif events[i].direction == 2:
        events[i].direction = 1
    events[i].alive = 1

cnt = build_graph(N, M)
dist = [-1] * (cnt + 1)

# 장애물인 경우 도달할 수 없으므로 미리 아주 큰 값으로 세팅합니다
# 평면도에 있는 장애물의 경우
for i in range(N):
    for j in range(N):
        if SpaceMap[i][j] == 3:
            continue
        if SpaceMap[i][j] == 1:
            idx = SpaceMapCellId[i][j]
            dist[idx] = INF

# 평면도에서 시간 이상 현상의 시작점도 도달 불가능하므로 장애물과 같이 처리합니다
for i in range(1, E+1):
    x = events[i].xpos
    y = events[i].ypos
    idx = SpaceMapCellId[x][y]
    dist[idx] = INF

# 단면도 위에 있는 장애물의 경우 역시 똑같이 처리합니다
for t in range(5):
    for i in range(M):
        for j in range(M):
            if TimeWall[t][i][j] ==1:
                idx = TimeWallCellId[t][i][j]
                dist[idx] = INF

from collections import deque
que = deque()

cell_start = -1
cell_end = -1

# 탈출구 위치 탐색
for i in range(N):
    for j in range(N):
        if SpaceMap[i][j] == 4:
            cell_end = SpaceMapCellId[i][j]
            break
    if cell_end != -1:
        break

# 타임머신의 시작점 탐색
for i in range(M):
    for j in range(M):
        if TimeWall[4][i][j] ==2:
            cell_start = TimeWallCellId[4][i][j]
            break
    if cell_start != -1:
        break

que.append(cell_start)
dist[cell_start] = 0

runs = 1
while True:
    # 현재 턴에 확장하는 이상현상이 있으면 영향을 받는 셀을 업데이트합니다
    for i in range(1, E+1):
        if not events[i].alive:
            continue
        if runs % events[i].cycle:
            continue
        nx = events[i].xpos
        ny = events[i].ypos
        # 이상현상의 방향에 따라 영향을 받는 셀의 좌표를 구합니다
        steps = runs // events[i].cycle
        if events[i].direction == 0:
            ny += steps
        elif events[i].direction == 1:
            nx += steps
        elif events[i].direction == 2:
            ny -= steps
        else:
            nx -= steps
        if nx < 0 or ny < 0 or nx >= N or ny >= N:
            events[i].alive = 0
            continue
        if SpaceMap[nx][ny]:
            events[i].alive = 0
            continue
        idx = SpaceMapCellId[nx][ny]
        dist[idx] = INF

    # 이번턴에 도달 가능한 셀들의 번호를 저장할 리스트
    next_cells = []
    size = len(que)
    for _ in range(size):
        idx = que.popleft()
        for i in range(4):
            idy = Graph[idx][i]
            if idy == -1:
                continue
            if dist[idy] != -1:
                continue
            dist[idy] = runs
            next_cells.append(idy)

    if not next_cells:
        break
    que.extend(next_cells)
    if dist[cell_end] != -1:
        break
    runs += 1

# 정답을 출력합니다.
# 불가능하면 -1이 출력됩니다
if dist[cell_end] == -1 or dist[cell_end] >= INF:
    print(-1)
else:
    print(dist[cell_end])
