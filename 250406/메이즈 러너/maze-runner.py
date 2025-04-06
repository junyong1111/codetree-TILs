import sys
sys.setrecursionlimit(10**5)
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline

N, M, K = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(N)]
player_input = [list(map(int, input().split())) for _ in range(M)]
exity, exitx  = map(int, input().split())
EXIT = -100000
PLAYER_LIST = []
ANSWER = [0]
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return (
f"""[좌표 출력]
현재 좌표 Y : {self.y} X : {self.x}"""
        )
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Plyaer():
    def __init__(self, point, dis):
        self.point = point
        self.dis = dis
    def __repr__(self):
        return(
f"""[현재 플레이어 정보]
{self.point}
이동한 거리 : {self.dis}""")

    def __eq__(self, other):
        return self.point == other
def my_print(arr):
    for data in arr:
        print(*data)
    print("[MY PRINT]")


def init():
    grid[exity-1][exitx-1] = EXIT
    for player in player_input:
        y, x= player
        PLAYER_LIST.append(
            Plyaer(
                point = Point(x-1, y-1),
                dis = 0
            )
        )

def pprint():
    print("[플레이어 전체 리스트 조회]")
    for player in PLAYER_LIST:
        print(player)



init()
# my_print(grid)
# pprint()

def get_shortest_path(point):
    _exit = get_exit_point()
    return abs(point.x - _exit.x) + abs(point.y - _exit.y)


def is_possible(nx ,ny):
    if (nx < 0 or nx >= N) or (ny < 0 or ny>=N):
        return False
    return True

def move_player(
    debugger = False
):
    #상하좌우
    dxs = [0, 0, -1, 1]
    dys = [-1, 1, 0, 0]

    update_list = []
    for idx, player in enumerate(PLAYER_LIST):
        # 우선 현재 위치에서 출구 까지 최단 경로를 가져옴
        shortest_path = get_shortest_path(player.point)
        shortest_point = player.point

        x, y = player.point.x, player.point.y

        for dx, dy in zip(dxs, dys):
            nx = x + dx
            ny = y + dy

            if is_possible(nx, ny) == False or grid[ny][nx] > 0:
                continue
            # 더 최단 경로 인지 확인
            n_shortest_path = get_shortest_path(Point(nx, ny))

            if shortest_path > n_shortest_path: #더 최단 경로가 있는지 확인
                if debugger:
                    print(
f"""[최단 경로 갱신]
새로운 최단 경로 거리 {n_shortest_path}
이동 할 위치 {Point(nx, ny)}""")
                shortest_path = n_shortest_path
                shortest_point = Point(nx, ny)

        if shortest_point != player.point: #이동할 가치가 있는 경우
            update_list.append([shortest_point, idx])
        else:
            if debugger:
                print(
f"""[움직이지 않는게 좋겠다 .. ㄷㄷ]
최단 경로 거리 {shortest_path}
이동 할 위치 {shortest_point}""")
    return update_list


def update_player(
    update_list,
    debugger = False
):
    if debugger:
        print(f"[유저 위치 정보 업데이트 시작 {len(update_list)}]")

    for u_player in update_list:
        point = u_player[0]
        idx = u_player[1]

        for i in range(len(PLAYER_LIST)):
            player = PLAYER_LIST[i]
            if idx == i: #업데이트 할 유저라면
                player.point = point
                player.dis +=1

    _exit = get_exit_point()
    for i in reversed(range(len(PLAYER_LIST))):
        player = PLAYER_LIST[i]

        if player.point == _exit:
            ANSWER[0] += player.dis
            PLAYER_LIST.pop(i)


def get_exit_point():
    for i in range(N):
        for j in range(N):
            if grid[i][j] == EXIT:
                return Point(j, i)

def get_rec_area(
    point,
    size,
    debugger = False
):
    _exit = get_exit_point()
    x, y = point.x, point.y

    player_flag = False
    exit_flag = False

    for i in range(size):
        for j in range(size):
            #현재 좌표에 출구랑 플레이어가 포함되어 있는지 확인
            if Point(x+j, y+i) in PLAYER_LIST:
                if debugger:
                    print(f"[현재 좌표에 일치하는 유저 발견]")
                player_flag = True
            if Point(x+j, y+i) == _exit:
                if debugger:
                    print(f"[현재 좌표에 일치하는 출구 발견]")
                exit_flag = True
    return player_flag and exit_flag

def get_minimum_rec(
    debugger = False
):
    #최소 정사각형을 찾아야 함
    for rec in range(2, N+1):
        if debugger:
            print(f"{rec} 크기의 정사각형 찾는중....")
        for i in range(0, N-rec):
            for j in range(0, N-rec):
                if debugger:
                    print(f"{i, j} 위치에서 {rec}크기의 정사각형 찾아봄")
                if get_rec_area(
                    Point(j, i),
                    rec,
                    debugger=debugger
                ):
                    if debugger:
                        print(f"[{rec}크기의 사각형 찾음]")
                    return Point(j, i), rec
                    #그러한 사각형을 찾았다면
    if debugger:
        print("최소 사각형을 찾지 못함!!! 에러!!")
    return None



def rotate_grid(
    ret,
    debugger = False
):
    point, size = ret
    new_arr = [[0 for _ in range(size)] for _ in range(size)]
    new_player = []
    for i in range(size):
        for j in range(size):
            tx, ty = i+point.x, size-1-j+point.y
            new_arr[i][j] = grid[ty][tx]

            for idx, player in enumerate(PLAYER_LIST):
                if player.point == Point(tx, ty):
                    new_player.append([Point(j+point.x, i+point.y), idx])


    for i in range(size):
        for j in range(size):
            if new_arr[i][j] > 0:
                new_arr[i][j] -=1
            grid[i+point.y][j+point.x] = new_arr[i][j]


    for np in new_player:
        point, idx = np
        for i in range(len(PLAYER_LIST)):
            player = PLAYER_LIST[i]
            if i == idx:
                player.point = point


def debbuger_print(
        grid
):
    new_arr = [x[:] for x in grid]

    for player in PLAYER_LIST:
        new_arr[player.point.y][player.point.x] = -99


    for data in new_arr:
        print(*data)
    print()

while K:
    K-=1
    #참가자는 모두 동시에 이동한다.
    update_list = move_player(debugger=False)

    if update_list:
        update_player(
            update_list,
            debugger=False
        )

    if len(PLAYER_LIST) == 0:
        break
    #회전
    ret = get_minimum_rec()
    if not ret:
        print("로직이 잘못 되었습니다. 점검하세요")
        break

    rotate_grid(
        ret = ret,
        debugger = False
    )
if PLAYER_LIST:
    for player in PLAYER_LIST:
        ANSWER[0] += player.dis

_exit = get_exit_point()
print(ANSWER[0])
print(_exit.y+1, _exit.x+1)
