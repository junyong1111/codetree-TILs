import sys
# sys.stdin = open("input.txt")

n = int(sys.stdin.readline())
elemetns = list(map(int, sys.stdin.readline().split()))

maxValue = 0
def backtracking(node, index, level, sumValue):
    global maxValue
    maxValue = max(maxValue, sumValue)
    if level == n:
        return
    else:
        for i in range(index, n):
            if elemetns[i] >= node: #-- 다음 노드의 값이 더 크다면(증가하는 부분이라면)
                sumValue += elemetns[i]
                backtracking(elemetns[i], i+1, level+1, sumValue)
                sumValue -= elemetns[i]
     
for i in range(n):
    sumValue = elemetns[i]
    backtracking(elemetns[i], i+1, 0, sumValue) 

print(maxValue)