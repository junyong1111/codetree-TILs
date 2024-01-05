import sys
# sys.stdin = open("input.txt")

N, K = map(int, sys.stdin.readline().split())
block = [0] * (N+1)

for _ in range(K):
    a,b = map(int, sys.stdin.readline().split())
    for i in range(a, b+1):
        block[i] +=1
block.sort()
print(block[(N//2)+1])