import sys


sys.setrecursionlimit(10**6)
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline


## 상 우 하 좌
dxs = [0, 1, 0, -1]
dys = [-1, 0, 1, 0]

N, M, K = map(int, input().split())


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Gun():
    def __init__(self, x, y, p):
        self.point = Point(x, y)
        self.power = p

    def __eq__(self, other):
        return self.point == other.point



class Player():
    def __init__(self, x, y, d, ability, gun, score):
        self.point = Point(x, y)
        self.dir = d
        self.ability = ability
        self.gun = gun
        self.score = score

    def reverse_player(self):
        if self.dir == 0:
            self.dir = 2
        elif self.dir == 1:
            self.dir = 3
        elif self.dir == 2:
            self.dir = 0
        elif self.dir == 3:
            self.dir = 1

    def rotate_player(self):
        self.dir = (self.dir + 1) % 4


    def __eq__(self, other):
        return self.point == other.point

def remove_gun(p, power):
    remove_index = -1
    for i in range(len(GUN_LIST)):
        gun_info = GUN_LIST[i]
        if Point(gun_info.point.x, gun_info.point.y) == p and gun_info.power == power:
            remove_index = i
            break
    if remove_index != -1:
        GUN_LIST.pop(remove_index)


grid = [list(map(int, input().split())) for _ in range(N)]
player_input = [list(map(int, input().split())) for _ in range(M)]

GUN_LIST = []
PLAYER_LIST = []

def my_print(arr):
    for data in arr:
        print(*data)
    print("================================[print]==================================")


def init():
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] != 0:
                GUN_LIST.append(Gun(j, i, grid[i][j]))


    for i in range(M):
        PLAYER_LIST.append(
            Player(
                player_input[i][1] -1 ,  # x
                player_input[i][0] - 1,  # y
                player_input[i][2],  # dir
                player_input[i][3],  # stat
                0,  # 총 여부
                0  # 점수
            )
        )

def game_info():
    # my_print(grid)

    for player in PLAYER_LIST:
        print(f"{player.point.x}, {player.point.y}, 방향 : {player.dir}, 능력치 : {player.ability}, 총 : {player.gun}, 점수 {player.score}")

    for gun in GUN_LIST:
        print(f"{gun.point.x}, {gun.point.y},  총 : {gun.power}")

def is_possible(nx, ny):
    if (nx < 0 or nx >=N) or (ny < 0 or ny >= N):
        return False
    return True


def remove_all_zero_gun():
    for i in reversed(range(len(GUN_LIST))):
        if GUN_LIST[i].power <= 0:
            GUN_LIST.pop(i)

def move_player():
    for p in range(len(PLAYER_LIST)):
        player = PLAYER_LIST[p]
        x, y = player.point.x, player.point.y
        is_fight = False

        nx, ny = x + dxs[player.dir], y+ dys[player.dir]
        #막히면 반대로 움직이고 그게 아니면 바라보는 방향으로 이동
        if is_possible(nx, ny) == False:
            #위치 바꾸기
            player.reverse_player()
            nx, ny = x + dxs[player.dir], y + dys[player.dir]

        player.point = Point(nx, ny) #이동했으니까 갱신
        #1. 이동한 방향에 플레이어가 있는지 확인
        for i in range(len(PLAYER_LIST)):
            target = PLAYER_LIST[i]
            if (nx, ny) == (target.point.x, target.point.y) and i != p:
                is_fight = True
                # 두 플레이어는 싸운다
                a_total_power = (player.ability + player.gun)
                b_total_power = (target.ability + target.gun)

                # 두 플레이어의 총점이 같다면 초기가 더 높은쪽
                if a_total_power == b_total_power:
                    winner = target if player.ability < target.ability else player
                    loser = target if player.ability > target.ability else player
                else:
                    winner = target if a_total_power < b_total_power else player
                    loser = target if a_total_power > b_total_power else player

                score = abs(a_total_power - b_total_power)
                winner.score += score

                #진플레이어 먼저 진행
                #본인이 가진 총을 내려놓기
                if loser.gun > 0:
                    GUN_LIST.append(
                        Gun(
                            loser.point.x,
                            loser.point.y,
                            loser.gun
                        )
                    )
                loser.gun = 0 #공격력은 0으로
                #자기가 가려던 방향으로 한 칸 이동
                for ii in range(4):
                    nx, ny = loser.point.x + dxs[loser.dir], loser.point.y + dys[loser.dir]
                    if is_possible(nx ,ny) == False or Player(nx, ny, -1, -1, -1, -1) in PLAYER_LIST: #격자 밖이거나 다른 플레이어가 있는 경우 회전
                        loser.rotate_player()
                    else:
                        # 새로운 공간을 온 경우
                        # 근데 거기에 총도 있는 경우 졌으니깐 총은 없음 가장 큰 총 좌표 하나만 따서 거기만 가져가자
                        loser.point = Point(nx, ny) #위치갱신
                        max_power_gun = -sys.maxsize
                        max_gun_point = Point(-1, -1)

                        for iii in range(len(GUN_LIST)):
                            gun_iii = GUN_LIST[iii]
                            if Gun(nx, ny, -1) == gun_iii: #같은 위치에 총이 있으면 최댓값 갱신
                                if max_power_gun < gun_iii.power:
                                    max_power_gun = gun_iii.power
                                    max_gun_point = gun_iii.point
                        #그러한 총이 하나라도 있다면 총 가져가지
                        if max_power_gun != -sys.maxsize:
                            loser.gun = max_power_gun
                            remove_gun(max_gun_point, max_power_gun)
                        break


                #이긴 플레이어 진행
                # 현재 칸에 있는 총들 중 가장 공격력 높은 총 획득
                w_max_gun_power = -sys.maxsize
                w_max_gun_point = Point(-1, -1)
                for ii in range(len(GUN_LIST)):
                    w_gun_ino = GUN_LIST[ii]
                    if winner == w_gun_ino: #위너가 있는 칸에 총이 있으면 맥스 총 가져옴
                        if w_max_gun_power < w_gun_ino.power:
                            w_max_gun_power = w_gun_ino.power
                            w_max_gun_point = w_gun_ino.point
                if w_max_gun_power != -sys.maxsize:
                    if w_max_gun_power > winner.gun:
                        #자기가 가지고 있던 총은 내려놔야 함
                        GUN_LIST.append(
                            Gun(
                                winner.point.x,
                                winner.point.y,
                                winner.gun
                            )
                        )
                        winner.gun = w_max_gun_power
                        remove_gun(w_max_gun_point, w_max_gun_power)


        if is_fight == False: #아무고 안만났으면 총 획득하러 가자
            current_gun = player.gun
            for i in range(len(GUN_LIST)):
                gun_info = GUN_LIST[i]
                if gun_info == player: #해당 위치에 총이 있는 경우
                    #더 파워가 쌔다면 스왑
                    if current_gun < gun_info.power:
                        temp = gun_info.power
                        gun_info.power = current_gun
                        current_gun = temp
            if current_gun != 0:
                player.gun = current_gun
        remove_all_zero_gun()



init()
# game_info()

# game_info()
# print("[TURN 시작 전]")
turn = 0
while K:
    K-=1
    turn +=1
    move_player()

    # print(f"[TURN {turn}회 후]")
    # game_info()


for player in PLAYER_LIST:
    print(player.score, end=" ")