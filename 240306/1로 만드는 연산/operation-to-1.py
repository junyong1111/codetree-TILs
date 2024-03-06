import sys

n = int(sys.stdin.readline())
INF = int(1e9)

dp = [INF] * (n+1)
dp[1] = 0
dp[2] = 1
dp[3] = 1

for i in range(4, n+1):
    if i%3 == 0:
        dp[i] = min(dp[i], dp[i//3])
    if i%2 == 0:
        dp[i] = min(dp[i], dp[i//2])
    dp[i] = min(dp[i], dp[i-1])+1

print(dp[n])