import sys
# sys.stdin = open("input.txt")

N, K = map(int, sys.stdin.readline().split())
numbers = list(map(int, sys.stdin.readline().split()))

def windowSum(start, K):
    ret = 0
    for i in range(K):
        ret += numbers[start + i]
    return ret

start = 0
maxvalue = windowSum(start, K)
pre = maxvalue
for i in range(K, N):
    start +=1
    addSum = pre + numbers[i]
    newSum = windowSum(start, K)
    
    if addSum >= newSum:
        pre = addSum
        if addSum >= maxvalue:
            maxvalue= addSum
    else:
        pre = newSum
        if newSum >= maxvalue:
            maxvalue = newSum
        
print(maxvalue)