import sys
# sys.stdin = open("input.txt")

n = int(sys.stdin.readline())

elemetns = list(map(int, sys.stdin.readline().split()))

dp = [[0 for _ in range(n+1)] for _ in range(4)]

dp[0][1] = elemetns[0] #-- 원소 선택
dp[1][1] = elemetns[0] #-- 원소 노선택
dp[2][1] = elemetns[0] #-- 선택한 경우 노드 값
dp[3][1] = elemetns[0] #-- 선택안한 경우 노드 값


for i in range(2, n+1):
    if elemetns[i-1]>=dp[2][i-1]:
        dp[0][i] = dp[0][i-1] + elemetns[i-1]
        dp[2][i] = elemetns[i-1]
        
        dp[1][i] = dp[1][i-1]
        dp[3][i] = dp[3][i-1]
    elif elemetns[i-1] >= dp[3][i-1]:
        dp[0][i] = dp[0][i-1]
        dp[2][i] = dp[2][i-1]
        
        dp[1][i] = dp[1][i-1] + elemetns[i-1]
        dp[3][i] = elemetns[i-1]
    else:
        dp[0][i] = dp[0][i-1]
        dp[1][i] = dp[1][i-1]
        dp[2][i] = dp[2][i-1]
        dp[3][i] = dp[3][i-1]


print(max(dp[0][n], dp[1][n]))