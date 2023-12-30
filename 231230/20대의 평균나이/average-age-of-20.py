import sys
import math

ages = []
while cnt:
    n = int(sys.stdin.readline())
    if n>=20 and n<=29:
        ages.append(n)
    else:
        break
mean = sum(ages) / len(ages)

print("%.2f"%mean)