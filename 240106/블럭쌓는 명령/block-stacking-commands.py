import sys
# sys.stdin = open("input.txt")

N, K = map(int, sys.stdin.readline().split())
diff = [0] * (N + 1)  # 누적 합을 계산하기 위한 차분 배열

for _ in range(K):
    a, b = map(int, sys.stdin.readline().split())
    diff[a-1] += 1
    diff[b] -= 1

# 누적 합 계산
block = [0] * (N)
current = 0
for i in range(N):
    current += diff[i]
    block[i] = current
# 블록 배열 정렬
block.sort()
# 중간 값 출력
print(block[N // 2])