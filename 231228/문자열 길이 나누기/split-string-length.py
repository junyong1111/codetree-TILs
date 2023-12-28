import sys
n = int(sys.stdin.readline())

answer =''

for _ in range(n):
    answer += sys.stdin.readline().strip()
half = len(answer)//2
first = answer[0:half]
second = answer[half:]

print(first)
print(second)