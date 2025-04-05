import sys
from collections import deque


sys.setrecursionlimit(10**6)
input = sys.stdin.readline

N, M = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
person_input =  [list(map(int, input().split())) for _ in range(M)]

CONVENIENCE_STORE = -100
INF = sys.maxsize
def my_print(arr):
    for data in arr:
        print(*data)
    print("============[MY PRINT]==============")

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __repr__(self):
        return (
            f"""
                [현재 Point 정보]
                좌표 [y : {self.y}, x : {self.x}]
            """
        )

class Myclass():
    def __init__(self, x, y, dir, distance):
        self.distance = distance
        self.point = Point(x, y)
        self.dir = dir

    def __repr__(self):
        return(
        f"""
            [현재 distance  정보]
            최단거리 : {self.distance}
            좌표 [y : {self.point.y}, x : {self.point.x}]
            방향 : {self.dir}
        """
        )

class Person():
    def __init__(self, target, number):
        self.number = number
        self.point = Point(-1, -1)
        self.target = target

    def __repr__(self):
        return(
        f"""
            [현재 {self.number}번째 Person 정보]
            좌표 [y : {self.point.y}, x : {self.point.x}]
            목표 편의점 위치 [y : {self.target.y}, x : {self.target.x}]    
        """
        )


BLOCK_LIST = []
PERSON_LIST = []

def init():
    for idx, person in enumerate(person_input, start = 1):
        y, x  = person
        y-=1
        x-=1

        PERSON_LIST.append(Person(Point(person[1]-1, person[0]-1), idx))
        grid[y][x] = CONVENIENCE_STORE #편의점 위치


init()


def find_shortest_path(person):
    dxs = [0, -1, 1, 0]
    dys = [1, 0, 0, -1]
    q = deque()
    x, y = person.point.x, person.point.y
    target = Point(person.target.x, person.target.y)
    distance = [[Myclass(-1, -1, -1, -1) for _ in range(N)] for _ in range(N)]

    q.append((x, y)) #일단 시작
    distance[y][x] = Myclass(x, y, -1, 0)

    while q:
        x, y= q.popleft()

        for i in range(4):
            nx, ny = x + dxs[i], y + dys[i]

            if is_possible(nx, ny) and distance[ny][nx].distance == -1 and Point(nx, ny) not in BLOCK_LIST:
                distance[ny][nx].distance = distance[y][x].distance  + 1
                distance[ny][nx].point = Point(x, y) #이전에 왔던 위치 저장
                distance[ny][nx].dir = i
                q.append((nx, ny))

                if target.x == nx and target.y == ny:
                    return distance
    return None


def target_dir(
        distance,
        person
):
    dis = distance[person.target.y][person.target.x]
    while True:
        if dis.point == person.point:
            return dis.dir
        dis = distance[dis.point.y][dis.point.x]




    

def move_person():
    dxs = [0, -1, 1, 0]
    dys = [1, 0, 0, -1]
    block_list = []
    # 2. 편의점 도착 갱신 -> 이동 불가는 맨 마지막
    for person in PERSON_LIST: #1번 사람부터 차례 대로 이동 이동 조건은 위치가 -1이 아닌 경우
        if (person.point.x == -1 and person.point.y == -1)  or (person.point == person.target):
            continue

        #현재 베이스 캠프에서 목표 편의점까지 bfs로 재 탐색 필요
        shortest_path = find_shortest_path(person)
        if shortest_path == None:
            print("목표지점까지 최단거리가 없습니다!!!! ERROR")
            return

        _target_dir = target_dir(
            shortest_path,
            person
        )

        #이동
        person.point = Point(person.point.x + dxs[_target_dir], person.point.y + dys[_target_dir])
        if person.point == person.target: #편의점에 들어간 경우
            # print(f"{person.number} 목표 지점으로 골인 ")
            block_list.append(Point(person.point.x, person.point.y))

    return block_list

def is_possible(nx, ny):
    if (nx < 0 or nx >= N) or (ny < 0 or ny >=N):
        return False
    return True

def bfs(p, target):
    dxs = [1, 0, -1, 0]
    dys = [0, 1, 0, -1]
    distance = [[-1 for _ in range(N)] for _ in range(N)]
    q = deque()
    x, y = p

    distance[y][x] = 0
    q.append((x, y))

    while q:
        x, y = q.popleft()

        for dx, dy in zip(dxs, dys):
            nx = x + dx
            ny = y + dy

            if is_possible(nx, ny) and distance[ny][nx] == -1 and Point(nx, ny) not in BLOCK_LIST:
                distance[ny][nx] = distance[y][x] + 1
                q.append((nx, ny))

                if Point(nx, ny) == target:
                    return distance[ny][nx]
    return INF

def go_base_camp(idx):
    idx -=1 #0번부터 시작이니까
    person = PERSON_LIST[idx]

    target = person.target
    #반대로 bfs탐색
    max_dis = INF
    max_p = [-1, -1]
    for i in reversed(range(N)):
        for j in reversed(range(N)):
            if Point(j, i) in BLOCK_LIST:
                continue
            if grid[i][j] == 1 and Point(j, i) not in BLOCK_LIST: #base캠프라면 해당 위치에서 target 편의점까지 최단 거리 계산
                dis = bfs((j,i), target)
                if dis <= max_dis:
                    max_dis = dis
                    max_p = [j, i]

    block = Point(-1, -1)
    if max_dis != INF: # 들어갈 곳 있따는거니깐 들가야함
        person.point = Point(max_p[0], max_p[1]) #x, y로 넣어줌
        block = Point(max_p[0], max_p[1]) #x, y로
    return  block

def is_done():
    for person in PERSON_LIST:
        if not (person.point.x == person.target.x and person.point.y == person.target.y):
            return False
    return True


def pprint():
    for person in PERSON_LIST:
        print(person)
time = 0
while True:
    time +=1
    # 1. 이동
    block = move_person()
    if block:
        for b in block:
            BLOCK_LIST.append(b)

    if time <= M:
        block = (go_base_camp(time))
        if block:
            BLOCK_LIST.append(block)

    # 2. 베이스 캠프 이동 -> 이동 불가는 맨 마지막
    if is_done():
        break
print(time)




