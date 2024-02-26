import sys
# sys.stdin = open("input.txt")

N = int(sys.stdin.readline())
heights = []
for _ in range(N):
    heights.append(int(sys.stdin.readline()))

def optimized_iceberg_groups(heights):
    unique_heights = sorted(set(heights), reverse=True)  # 고유 높이 정렬
    max_groups = 0
    index = 0  # 현재 높이의 인덱스

    while index < len(unique_heights):
        water_level = unique_heights[index]
        groups = 0
        in_group = False
        for height in heights:
            if height > water_level:
                if not in_group:
                    groups += 1
                    in_group = True
            else:
                in_group = False
        max_groups = max(max_groups, groups)
        index += 1

    return max_groups

# 다시 최적화된 방식으로 최대 빙산 덩어리의 수 계산
print(optimized_iceberg_groups(heights))