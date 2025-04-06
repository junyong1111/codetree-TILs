"""
4 <= N, M <= 10
1 <= K <= 1,000
0 <= 공격력 <= 5,000
"""
import sys
from collections import deque
from math import trunc

sys.setrecursionlimit(10**5)
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Distance():
    def __init__(self):
        self.point = Point(0, 0),
        self.dis = -1

    def __repr__(self):
        return(
f"""[최단 경로 INFO]
직전 좌표 y : {self.point.y} x : {self.point.x}
이동 거리 : {self.dis} 
""")

class Turret():
    def __init__(
            self,
            point,
            power,
            last_turn = 0,
            effected = False
    ):
        self.point = point
        self.power = power
        self.last_turn = last_turn
        self.effected = effected

    def __repr__(self):
        return(
f"""[MY TURRET INFO]
    좌표 y : {self.point.y} x : {self.point.x}
    파워 : {self.power}
    마지막 공격 순서 : {self.last_turn}
    현재 공격으로 인해 영향 받은 여부 : {self.effected} 
"""
        )

    def __lt__(self, other):
        #공격력 낮고 마지막 공격 턴이 높고 좌표의 합이 높고 열이 높고
        if self.power == other.power:
            if self.last_turn == other.last_turn:
                if self.point == other.point:
                    return self.point.x > other.point.x
                return (self.point.x + self.point.y) > (other.point.x + other.point.y)
            return self.last_turn > other.last_turn
        return self.power < other.power


N, M, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
TURRET_LIST = []
BROKEN_TURRET_LIST = []

def my_print(arr):
    for data in arr:
        print(*data)

    print("== [MY PRINT] ==")

def init():
    for i in range(N):
        for j in range(M):
            if grid[i][j] > 0: #포탑이 있는 경우 리스트에 삽입
                TURRET_LIST.append(
                    Turret(
                        point=Point(j, i),
                        power=grid[i][j],
                    )
                )
            elif grid[i][j] == 0:
                BROKEN_TURRET_LIST.append(
                    Point(
                        j,
                        i
                    )
                )

def my_t_print():
    print("[포탑 정보 전체 출력")
    for turret in TURRET_LIST:
        print(turret)



init()

def select_attack_turret(
        turn,
        debugger = False
):
    TURRET_LIST.sort()
    weak_turret = TURRET_LIST[0]  # 공격자 포탑 선정
    target_turret = TURRET_LIST[-1]  # 공격당할 포탑

    weak_turret.effected = True
    weak_turret.last_turn = turn

    target_turret.effected = True

    if debugger:
        print("[공격자 터렛 선정 완료]")
        print(weak_turret)
        print("[공격 당할 터렛 선정 완료]")
        print(target_turret)

    # 1. 공격자 포탑 공격력 강화
    weak_turret.power += (N + M)
    if debugger:
        print(
    f"""[공격 터렛 공격력 증가] : {weak_turret.power}
    """
        )
    return weak_turret,target_turret


def is_possible(nx, ny):
    if nx < 0:
        return M-1, ny
    if nx >= M:
        return 0, ny
    if ny < 0:
        return nx, N-1
    if ny >=N:
        return nx , 0
    return nx, ny

def get_shortest_path_with_laser(
    start,
    target
):
    #우 하 좌 상
    dxs = [1, 0, -1, 0]
    dys = [0, 1, 0, -1]

    distance = [[Distance() for _ in range(M)] for _ in range(N)]
    q = deque()
    x, y = start.x, start.y
    distance[y][x].dis = 0
    distance[y][x].point = Point(x, y)
    q.append((x, y))

    while q:
        x, y = q.popleft()
        for dx, dy in zip(dxs, dys):
            nx  = x + dx
            ny = y  + dy

            nx, ny = is_possible(nx, ny) # 현재 통과 여부에 따라 샐보게 좌표를 갱신
            # 해당 위치에 죽은 포탑이 있으면 안됨
            if Point(nx, ny) not in BROKEN_TURRET_LIST and distance[ny][nx].dis == -1: #부서진 포탑에 없고 첫 방문이면 진행
                distance[ny][nx].dis = distance[y][x].dis +1
                distance[ny][nx].point = Point(x, y) #이전 위치 확이
                q.append((nx,ny))

                if Point(nx, ny) == target:
                    return distance
    return None

def attack_with_laser(
    weak_turret,
    target_turret,
    debugger =False
):
    # 레이저를 이용한 최단 경로 확인
    shortest_path = get_shortest_path_with_laser(
        start = weak_turret.point,
        target = target_turret.point
    )

    if not shortest_path:
        if debugger:
            print("현재 최단 경로가 없습니다.")
        return False

    # 그러한 경로가 있는 경우 해당 경로를 따라 공격
    # 우선 공격자는 원래 데미지에 맞게 공격
    target_turret.power = max(target_turret.power - weak_turret.power, 0)
    attack_power = weak_turret.power//2 # 나머지 경로에는 절반만

    if debugger:
        print(
f"""[타겟 포탑 공격 받음]
{target_turret.power}
[절반 공격력 변환]
{attack_power}
""")
    dis = shortest_path[target_turret.point.y][target_turret.point.x] #여기에는 경로들에 대한 좌표가 있음
    while True:
        if dis.point == weak_turret.point: #만약 현재가 공격자 터렛이면 중지
            break
        #그게 아니라면 현재 위치에 터렛도 공격
        for turret in TURRET_LIST:
            if turret.point == dis.point:
                turret.power = max(turret.power - attack_power,  0)
                turret.effected = True
                break
        #공격 했으면 다음 위치로 이동
        dis = shortest_path[dis.point.y][dis.point.x]
    return True


def is_possible_with_missile(nx, ny):
    if nx < 0 :
        nx = M-1
    if ny < 0:
        ny = N-1
    if nx >= M:
        nx = 0
    if ny >=N:
        ny = 0
    return nx, ny
def get_attack_area(
    weak_turret,
    target_turret,
    debugger=False
):
    # 상, 우상, 우, 우하, 하, 좌하, 좌, 좌상
    dxs = [0, 1, 1, 1, 0, -1 ,-1 ,-1]
    dys = [-1, -1, 0, 1, 1, 1, 0, -1]

    target_list = []
    x, y = target_turret.point.x, target_turret.point.y


    for dx, dy in zip(dxs, dys):
        nx = x + dx
        ny = y + dy

        nx, ny =  is_possible_with_missile(nx ,ny) # 넘어가는 부분 모두 맞춰주도록 설정
        if Point(nx, ny) not in BROKEN_TURRET_LIST and Point(nx ,ny) != weak_turret.point : #부서진 곳에 없고 공격자 포탑이 아니라면 부숴 버리기
            if debugger:
                print("[타겟 지정]")
            target_list.append(Point(nx ,ny))
    return target_list



def attack_with_missile(
    weak_turret,
    target_turret,
    debugger=False
):
    #포탄 공격은 최단 경로 상관없이 해당 위치에서 8방향 만약 인덱스를 초과한다면 넘어가도록 설정
    # 우선 공격자는 원래 데미지에 맞게 공격
    target_turret.power = max(target_turret.power - weak_turret.power, 0)
    attack_power = weak_turret.power // 2  # 나머지 경로에는 절반만

    # 나머지 경로 계산
    attack_area = get_attack_area(
        weak_turret,
        target_turret,
        debugger
    )

    for area in attack_area:
        for turret in TURRET_LIST:
            if area == turret.point and area not in BROKEN_TURRET_LIST:
                if debugger:
                    print("[목표 발견]")
                    print(turret)
                turret.effected = True
                turret.power = max (turret.power - attack_power, 0)


def attack_turret(
    weak_turret,
    target_turret,
    debugger=False
):

    #1. 먼저 레이저 공격을 해야함
    if debugger:
        print("[레이저 공격 준비]")
    is_attack = attack_with_laser(
        weak_turret = weak_turret,
        target_turret = target_turret,
        debugger = debugger
    )

    if is_attack: #레이저 공격을 했으면 포탑 공격은 패스
        if debugger:
            print("공격을 완료했습니다.")
        return

    #공격을 못했으면 이제 포탑 공격을 해야함
    attack_with_missile(
        weak_turret=weak_turret,
        target_turret=target_turret,
        debugger=debugger
    )

def update_turret():
    for i in reversed(range(len(TURRET_LIST))):
        turret = TURRET_LIST[i]
        if turret.power == 0 and turret.point not in BROKEN_TURRET_LIST:
            BROKEN_TURRET_LIST.append(turret.point)
            TURRET_LIST.pop(i)

def repair_turret():
    for turret in TURRET_LIST:
        if turret.effected == True:
            turret.effected = False
            continue
        turret.power +=1
turn = 0
while K:
    K-=1
    turn +=1

    # 공격자 포탑을 선정 이후 공격력 증가
    weak_turret,target_turret = select_attack_turret(turn, debugger=False)

    attack_turret(
        weak_turret,
        target_turret,
        debugger=False
    )
    update_turret()
    repair_turret()

    if len(TURRET_LIST) <= 1:
        break

TURRET_LIST.sort()
print(TURRET_LIST[-1].power)


# 622 turn