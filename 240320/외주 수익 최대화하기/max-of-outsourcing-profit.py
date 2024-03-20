import sys
# sys.stdin = open("input.txt")

MAX_SIZE = 16
input = sys.stdin.readline
N = int(input())

numbers = []
for _ in range(N):
    a, b = map(int, input().split())
    numbers.append([a,b])

dp = [0] * MAX_SIZE

if numbers[0][0] <= N:
    dp[1] = numbers[0][1]
else:
    dp[1] = 0

def dynamic(n):
    if n <= 0:
        return 0
    if dp[n] != 0:
        return dp[n]
    dp[n] = max(dynamic(n-1), (dynamic(n - (numbers[n-1][0]+1))+ numbers[n-1][1]))
    return dp[n]
    
dynamic(N)
print(dp[N])