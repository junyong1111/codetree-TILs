import sys
# sys.stdin = open("input.txt")
N, L = map(int, sys.stdin.readline().split())

points = []
for _ in range(N):
    points.append(int(sys.stdin.readline()))
points.sort()

def makeLeftList(target, arr):
    left_list = []
    for i in range(len(arr)):
        if target < arr[i]:
            left_list.append(arr[i])
    return left_list

def makeRightList(target, arr):
    right_list = []
    for i in reversed(range(len(arr))):
        if target > arr[i]:
            right_list.append(arr[i])
    return right_list
     
            
max_value = max(points)
answer = 0
for target in range(1, max_value):
    #-- Step1. target 지정
    #-- target보다 크면 왼쪽 리스트에 저장
    left_list = makeLeftList(target, points)
    #-- target보다 작다면 오른쪽 리스트에 저장
    right_list = makeRightList(target, points)
    
    #-- 모두 겹쳤는지 확인
    flag = True
    min_len = min(len(right_list), len(left_list))
    for i in range(min_len):
        if target - right_list[i] != left_list[i]-target:
            flag = False
            break
    if flag:
        answer +=1
print(answer)