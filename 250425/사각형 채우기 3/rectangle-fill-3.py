n = int(input())
MOD = 1000000007
MAX_SIZE = 1001

table = [0] * MAX_SIZE
table[1] = 2
table[2] = 7

for i in range(3, n+1):
    table[i] = ((2* table[i-1]) + (table[i-2] * 3) + 2) % MOD

print(table[n])