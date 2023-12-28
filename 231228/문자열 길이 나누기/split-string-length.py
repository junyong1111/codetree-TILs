import sys
n = int(sys.stdin.readline())

answer =''

for _ in range(n):
    answer += sys.stdin.readline().strip()
first = answer[0:7]
second = answer[7:]

print(first)
print(second)