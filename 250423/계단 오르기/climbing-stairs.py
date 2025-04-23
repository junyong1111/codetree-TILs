N = int(input())

table = [0] * (1001)
table[2] = 1
table[3] = 1

for i in range(4, N+1):
    table[i] = (table[i-2] + table[i-3]) % 10007

print(table[N])