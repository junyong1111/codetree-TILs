import sys
# sys.stdin = open("9.알고리즘유형별/input.txt")

n = int(sys.stdin.readline())
carry = []


for _ in range(n):
    carry.append(int(sys.stdin.readline()))


def isCarry(a, b):
    A = list(map(int, str(a)))
    B = list(map(int, str(b)))
    
    while len(A)!= 0 and len(B) !=0:
        if A[-1] + B[-1] > 9:
            return False
        else:
            A.pop()
            B.pop()
    return True

answer = 0
def backtracking(pre, level, index):
    global answer
    if index+1 == n:
        answer = max(answer, level)
        pass
    else:
        for i in range(n):
            if visit[i] == 0:
                if isCarry(pre, carry[i]) == False:
                    continue
                visit[i] = 1 
                answer = max(answer, level)
                backtracking(pre+carry[i], level+1, i)
                visit[i] = 0
        
        
for i in range(n):
    visit = [0] * n
    visit[i] = 1
    backtracking(carry[i], 2, i)
    visit[i] = 0
print(answer)