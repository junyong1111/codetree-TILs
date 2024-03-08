import sys
n, p = map(int, sys.stdin.readline().split())
INF = int(1e9)

markets = []
for _ in range(p):
    a,b = map(int, sys.stdin.readline().split())
    markets.append((a,b))

minValue = INF

for market in markets:
    number, price = market
    if n%number == 0:
        minValue = min(minValue, (n//number) * price)
print(minValue)