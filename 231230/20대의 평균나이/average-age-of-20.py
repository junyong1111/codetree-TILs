import sys
import math

ages = []
cnt= 100
while cnt:
    cnt-=1
    n = int(sys.stdin.readline())
    if n >= 30:
        break
    else:
        ages.append(n)
mean = sum(ages) / len(ages)

print("%.2f"%mean)