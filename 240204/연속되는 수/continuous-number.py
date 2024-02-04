import sys
# sys.stdin = open("input.txt")

'''
N개의 숫자들이 주어졌을 때, 
적절하게 숫자 K를 선택하여 입력으로 주어진 숫자들 중 숫자 K를 전부 제외했을 때 
연속하여 동일한 숫자가 나오는 횟수가 최대가 되도록 하는 프로그램을 작성해보세요. 
단, 숫자 K는 반드시 입력으로 주어진 숫자들 중에 하나로 결정되어야 합니다.
입력 형식
첫 번째 줄에 N이 주어집니다.
두 번째 줄부터 N개의 줄에 걸쳐 각 숫자들이 한 줄에 하나씩 주어집니다.
1 ≤ N ≤ 1,000
0 ≤ 입력으로 주어지는 숫자 ≤ 1,000,000
'''

n = int(sys.stdin.readline())
numbers = []
for _ in range(n):    
    numbers.append(int(sys.stdin.readline()))
dic = set(sorted(numbers))

def delteTarget(target, arr):
    returnArr = []
    for i in range(len(arr)):
        if arr[i] != target:
            returnArr.append(arr[i])
    return returnArr
   
def findThat(arr):
    if len(arr) == 0:
        return 0
    target = arr[0]
    cnt = 1
    answer = 1
    for i in range(1, len(arr)):
        if target == arr[i]:
            cnt+=1
            answer = max(answer, cnt)
        else:
            target = arr[i]
            cnt = 1
    return answer
        
answer = 0         
for data in dic:
    cp = delteTarget(data, numbers)
    cnt = findThat(cp)
    answer = max(answer, cnt)
print(answer)