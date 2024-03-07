import sys
# sys.stdin = open("input.txt")

n = int(sys.stdin.readline())
MAX_SIZE = 301
elemetns = [0] * (n+1)
for i in range(1, n+1):
    elemetns[i] = int(sys.stdin.readline())
    
dp = [0] * (MAX_SIZE)
dp[1] = elemetns[1]
dp[2] = elemetns[1] + elemetns[2]
dp[3] = elemetns[3] + max(elemetns[2], elemetns[1])

for i in range(4, n+1):
    dp[i] = elemetns[i] + max((dp[i-3] + elemetns[i-1]), dp[i-2])

print(dp[n])