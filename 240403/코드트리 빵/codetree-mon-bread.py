import sys
from collections import deque
# sys.stdin = open("SAMSUNG/input.txt")
input = sys.stdin.readline

N, M = map(int, input().split())
INF = int(1e9)
def myprint(arr, n, m):
    for i in range(n):
        for j in range(m):
            print(arr[i][j], end=" ")
        print()
    print("== My Data Print ==")

grid = []
basecampList = []
for _ in range(N):
    grid.append(list(map(int, input().split())))
    
for i in range(N):
    for j in range(N):
        if grid[i][j] == 1:
            basecampList.append([j, i])

ready = deque()
start = deque()
finish = deque()

for i in range(1, M+1):
    y, x = map(int, input().split())
    ready.append([i, x-1, y-1, -1, -1]) #-- -1 -1 위치에 있는 i번째 사람이 가고싶은 편의점 방향 x, y

#-- init() 확인
#-- U L R D
dx = [0, -1, 1, 0]
dy = [-1, 0, 0, 1]

def shortestPathToBaseCamp(X, Y):
    queue = deque()
    distance = [[INF for _ in range(N)] for _ in range(N)]
    
    queue.append([X, Y])
    distance[Y][X] = 0
    
    while queue:
        x, y = queue.popleft()
        
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < N and 0 <= ny < N and distance[ny][nx] == INF and grid[ny][nx] != -1:
                distance[ny][nx] = distance[y][x] +1
                queue.append([nx, ny])
    
    # print("BASECAMPE")
    # myprint(distance, N, N)
    # print("BASECAMPE")
    
    shortestBase = []
    for basecamp in basecampList:
        x, y = basecamp
        shortestBase.append([distance[y][x], x, y])
    shortestBase.sort()
    
    #-- 해당 베이스 캠프 삭제
    for basecamp in basecampList:
        if shortestBase[0][1] == basecamp[0] and shortestBase[0][2] == basecamp[1]:
            basecampList.remove(basecamp)
    # print(shortestBase[0][1], shortestBase[0][2])
    return shortestBase[0][1], shortestBase[0][2]
            
def shortestPath(X, Y, target_x, target_y):
    queue = deque()
    distance = [[INF for _ in range(N)] for _ in range(N)]
    trace = [[INF for _ in range(N)] for _ in range(N)]
    
    queue.append([X, Y])
    distance[Y][X] = 0
    trace[Y][X] = -2
    
    while queue:
        x, y = queue.popleft()
        
        for i in range(4):
            flag = False
            nx = x + dx[i]
            ny = y + dy[i]
            
            if 0 <= nx < N and 0 <= ny < N and distance[ny][nx] == INF and grid[ny][nx] != -1:
                distance[ny][nx] = distance[y][x] +1
                trace[ny][nx] = i
                if nx == target_x and ny == target_y:
                    flag = True
                    break
                queue.append([nx, ny])
        if flag == True:
            break
    #-- 최단 경로 추적
    prev_x = target_x
    prev_y = target_y
    
    while True:
        if trace[prev_y][prev_x] == -2:
            break
        dir = trace[prev_y][prev_x]
        if dir == 0:
            prev_y +=1        
        elif dir == 1:
            prev_x+=1
        elif dir == 2 :
            prev_x-=1
        elif dir == 3:
            prev_y -=1
    
    # myprint(trace, N, N)
    # print(X+dx[dir], Y+dy[dir])
    return X+dx[dir], Y+dy[dir]
    
    
            
time = 0
while True:
    time+=1
    # print("tiem : {} 경과".format(time))
    
    # myprint(grid, N, N)
    # print(ready)
    # print(start)
    # print(finish)
    # print("===========")
    
    """ #step1
    격자에 있는 모든 인원은 본인이 가고 싶은 편의점 방향으로 1칸 움직인다.
    이 때 최단거리로 이동해야 하며 최단경로가 여러개인 경우 U L R D순으로 움직인다.
    """
    size = len(start)
    while size != 0:
        size-=1
        target_x, target_y, x, y = start.popleft()
        x, y = shortestPath(x, y, target_x, target_y) #-- 최단거리로 이동 후 
        
        if x == target_x and y == target_y:
            # print("도착지 도착!!")
            finish.append([target_x, target_y])
        else:
            start.append([target_x, target_y, x, y])
        
        
    """ #step2
    편의점 도착 시 편의점에서 멈추며  (도착 queue로 넘김)
    
    (도착 Queue를 순회하면서 아래 로직을 수행하면 될듯)
    해당 편의점은 못지나가게 된다.(-1로 벽을 표시)    
    해당 로직은 격자에 있는 모든 인원이 움직인 후 발동한다.
    """
    while finish:
        target_x, target_y = finish.popleft()
        grid[target_y][target_x] = -1
    
    """ #step3
    현재 시간이 t분이고 t<=m를 만족한다면
    t번째 사람은 자신이 가고싶어 하는 편의점 가장 가까운 베이스 캠프로 이동한다(이동시간 소모 X)
    이 때부터는 해당 베캠은 사용이 불가능하다.
    """
    
    #-- 대기중인 사람 한 명을 꺼내옴
    if len(ready) != 0:
        i, target_x, target_y, x, y = ready.popleft()
    
        if time <= i:
            #== 자신이 가고 싶어하는 편의점 가강 가까운 베이스 캠프로 이동한다.
            x, y = shortestPathToBaseCamp(target_x, target_y)
            #-- 해당 베이스 캠프는 더 이상 사용이 불가
            grid[y][x] = -1

        #-- 가고싶은 편의점 위치 + 자신의 위치 전송
        start.append([target_x, target_y, x, y])
    if len(start) == 0:
        break
print(time)