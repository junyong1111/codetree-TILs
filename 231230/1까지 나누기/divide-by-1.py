import sys
n = int(sys.stdin.readline())

cnt = 0
start = 1
while n>1:
    n = n//start
    cnt+=1
    start+=1

print(cnt)