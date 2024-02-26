import sys
# sys.stdin = open("input.txt")

N = int(sys.stdin.readline())
heights = []
for _ in range(N):
    heights.append(int(sys.stdin.readline()))

heights_sort = sorted(set(heights), reverse=True)
    
def Iceberg(target):
    flag = False
    cnt = 0
    for height in heights:
        if target < height and flag == False:
            cnt+=1
            flag = True
        elif target >= height and flag == True:
            flag = False
    return cnt     

answer = 0
for height_sort in heights_sort:
    answer = max(answer, Iceberg(height_sort))
print(answer)