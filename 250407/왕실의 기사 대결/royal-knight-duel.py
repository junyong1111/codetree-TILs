import sys
from collections import deque

sys.setrecursionlimit(10**6)
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline

# 상 우 하 좌
dxs = [0, 1, 0, -1]
dys = [-1, 0, 1, 0]
ANSWER = []
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return(
f"""[좌표 출력]
Y : {self.y} X : {self.x}
""")
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Knight():
    def __init__(self, number, health = 0):
        self.knight_point = []
        self.health = health
        self.number = number
    def add_knight(self, x, y, h, w, health):
        for i in range(y, y + h):
            for j in range(x,  x + w):
                self.knight_point.append(Point(j, i))
        self.health = health

    def add_knight_without_hw(self, x, y, health):
        self.knight_point.append(Point(x, y))
        self.health += health


    def __repr__(self):
        return(
f"""[기사 정보 출력]
위치 : {self.knight_point}
체력 : {self.health}
""")
    def __eq__(self, other):
        return self.knight_point == other.knight_point

EMPTY = 0
TRAP = 1
WALL = 2

L, N, Q = map(int, input().split())
# 0 : 빈칸, 1: 함정, 2: 벽

grid = [list(map(int, input().split())) for _ in range(L)]
KNIGHT_LIST = {}

def my_print(arr):
    for data in arr:
        print(*data)
    print("[INFO]")

# my_print(grid)
knignt_input = [list(map(int, input().split())) for _ in range(N)]
# r c h w k


def init():
    for idx, knight in enumerate(knignt_input, start = 1):
        y, x, h, w, k = knight
        my_knight = Knight(number=idx)
        my_knight.add_knight(x-1, y-1, h, w, k)

        KNIGHT_LIST[idx] = my_knight
        ANSWER.append(0)

init()

def my_kn_print():
    for k, v in KNIGHT_LIST.items():
        print(f"{k}번째 기사 {v}")
# my_kn_print()

def is_possible(nx, ny):
    if (nx < 0 or nx >= L) or (ny < 0 or ny >= L):
        return False
    return True

def check_move(
    debugger,
    knight,
    dir,
    first
):
    new_knight = Knight(number=knight.number, health=knight.health)
    mat_knight_list = []
    for p in knight.knight_point:
        if debugger:
            print(f"[MOVE 전]")
            print(f"{p}")
        nx = p.x + dxs[dir]
        ny = p.y + dys[dir]

        if debugger:
            print(f"[MOVE 후]")
            print(f"{Point(nx, ny)}")
        if is_possible(nx, ny):
            if grid[ny][nx] == WALL:
                if debugger:
                    print("[벽 만남 수고]")
                return False #벽이면 종료

            if grid[ny][nx] == EMPTY:
                if debugger:
                    print("[빈공간]")
                new_knight.add_knight_without_hw(nx, ny, 0)

            elif grid[ny][nx] == TRAP:
                if debugger:
                    print("[트랩 밟음]")
                health = -1
                if first:
                    if debugger:
                        print("[시작이라 괜춘]")
                    health = 0
                new_knight.add_knight_without_hw(nx, ny, health)

            for k,v in KNIGHT_LIST.items():
                #만약 만난게 있으면
                if Point(nx, ny) in v.knight_point and  Point(nx, ny) not in knight.knight_point:
                    if debugger:
                        print(f"{k} 번째 기사 만났음")
                    mat_knight_list.append(k) #해당 기사 인덱스 저장
        else:
            #애초에 이동 못하면 빠임
            if debugger:
                print("범위 나감요 수고")
                return False
    return new_knight, mat_knight_list


def clean_up_knight(
    debugger,
):
    remove_idx = []
    for k, v in KNIGHT_LIST.items():
        if v.health == 0:
            if debugger:
                print(f"{k}번째 기사 빠이용")
            remove_idx.append(k)
            ANSWER[v.number-1] = 0
    
    
    for idx in remove_idx:
        del KNIGHT_LIST[idx]


def move_knight(
    debugger,
    idx,
    dir
):
    #우선 처음 시작하는 기사는 데미지 없이 밀어내기 가능
    new_knight_list = []
    knight = KNIGHT_LIST[idx]
    first = True
    knight_queue = deque()
    knight_queue.append(knight)

    while knight_queue:
        knight = knight_queue.popleft()
        if debugger:
            print(f"{knight.number}번쨰 기사 이동 시작")
        ret = check_move(
                debugger=debugger,
                knight = knight,
                dir=dir,
                first=first
        )
        if not ret:
            if debugger:
                print("[아무도 못가]")
            return
        first = False #한 번하고나면 트랩 면제 노노
        new_knight, mat_knight_list = ret
        new_knight_list.append(new_knight)

        for point in mat_knight_list:
            knight_queue.append(
                KNIGHT_LIST[point]
            )

    #여기 까지 온건 살아남았다는 듯
    if debugger:
        print("[교체 시작]")
    for new_knight in new_knight_list:
        before = KNIGHT_LIST[new_knight.number].health
        if debugger:
            print("[교체 전]")
            print(KNIGHT_LIST[new_knight.number])

        KNIGHT_LIST[new_knight.number] = new_knight
        ret = before - KNIGHT_LIST[new_knight.number].health
        if debugger:
            print("[교체 후]")
            print(KNIGHT_LIST[new_knight.number])
        ANSWER[new_knight.number-1] += ret
    clean_up_knight(
        debugger=debugger
    )


turn = 0
while Q:
    Q-=1
    turn+=1
    # print(f"{turn} 번째 겜 시작이요")
    idx,dir = map(int, input().split())

    move_knight(
        idx = idx,
        dir = dir,
        debugger = False
    )


answer = 0
for ans in ANSWER:
    answer += ans

print(answer)