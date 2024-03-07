import sys
# sys.stdin = open("input.txt")

n = int(sys.stdin.readline())
MAX_SIZE = 301
elemetns = [0] * (n+1)
for i in range(1, n+1):
    elemetns[i] = int(sys.stdin.readline())

dp = [[0 for _ in range(MAX_SIZE)] for _ in range(3)]
dp[0][1] = elemetns[1] #-- 1개 선택
dp[1][1] = elemetns[1] #-- 2개 선택

for i in range(2, n+1):
    dp[0][i] = dp[2][i-1] + elemetns[i]
    dp[1][i] = dp[0][i-1] + elemetns[i]
    dp[2][i] = max(dp[0][i-1], dp[1][i-1])

print(max(dp[0][n], dp[1][n]))