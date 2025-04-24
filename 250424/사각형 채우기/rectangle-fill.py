N = int(input())
MAX_SIZE = 1001

table = [0] * MAX_SIZE
table[1] = 1
table[2] = 2

for i in range(3, N+1):
    table[i] = table[i-2] + table[i-1]
print(table[N])