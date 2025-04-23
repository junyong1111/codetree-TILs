N = int(input())
dp_table = [-1] * (46)

dp_table[0] = 0
dp_table[1] = 1

def fibo(n):
    if dp_table[n] != -1:
        return dp_table[n]
    dp_table[n] = fibo(n-1) + fibo(n-2)
    return dp_table[n]

print(fibo(N))