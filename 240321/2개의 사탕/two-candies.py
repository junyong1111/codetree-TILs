import sys
from collections import deque

# sys.stdin = open("SAMSUNG/input.txt")
input = sys.stdin.readline


grid = [[0 for _ in range(11)] for _ in range(10)]
N, M = map(int, input().split())
MAX_SIZE = 10

Red = []
Blue = []

for i in range(N):
    data = input().split()
    for j in range(M):
        grid[i][j] = data[0][j]
        if grid[i][j] == "R":
            Red.append(j)
            Red.append(i)
        if grid[i][j] == "B":
            Blue.append(j)
            Blue.append(i)

def myprint():
    for i in range(N):
        for j in range(M):
            print(grid[i][j], end=" ")
        print()        

    
def bfs():
    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    
    visit = [[[[0 for _ in range(MAX_SIZE)] for _ in range(MAX_SIZE)] for _ in range(MAX_SIZE)] for _ in range(MAX_SIZE)]
    
    queue = deque()
    queue.append([Red, Blue, 0])    
    visit[Red[1]][Red[0]][Blue[1]][Blue[0]] = 1
    
    ret = -1
    while queue:
        currRed, currBlue, currmove = queue.popleft()        
        if currmove > 10:
            break
        if grid[currRed[1]][currRed[0]] == "O" and grid[currBlue[1]][currBlue[0]] != "O":
            ret = currmove
            break
            
        for dir in range(4):
            next_rx, next_ry = currRed[0], currRed[1]
            next_bx, next_by = currBlue[0], currBlue[1]
            
            #-- red 먼저 이동
            while True:
                if grid[next_ry][next_rx] != "#" and grid[next_ry][next_rx] != "O":
                    next_rx += dx[dir]
                    next_ry += dy[dir]
                
                else:
                    if grid[next_ry][next_rx] == "#":
                        next_rx -= dx[dir]
                        next_ry -= dy[dir]
                    break
            #-- blue 이동
            
            while True:
                if grid[next_by][next_bx] != "#" and grid[next_by][next_bx] != "O":
                    next_bx += dx[dir]
                    next_by += dy[dir]
                else: 
                    if grid[next_by][next_bx] == "#":
                        next_bx -= dx[dir]
                        next_by -= dy[dir]
                    break
            
            #-- 겹친 경우 제외
            if next_rx == next_bx and next_ry == next_by and grid[next_ry][next_rx] != "O":
                r_dis = abs(next_rx - currRed[0]) + abs(next_ry - currRed[1])
                b_dis = abs(next_bx - currBlue[0]) + abs(next_by - currBlue[1])
                
                if r_dis > b_dis:
                    next_rx -= dx[dir]
                    next_ry -= dy[dir]
                else:
                    next_bx -= dx[dir]
                    next_by -= dy[dir]
            if visit[next_ry][next_rx][next_by][next_bx] == 0: #-- 최초 방문
                visit[next_ry][next_rx][next_by][next_bx] = 1
                move = currmove+1
                queue.append([[next_rx, next_ry],[next_bx, next_by], move])
    return ret            
ret = bfs()
print(ret)