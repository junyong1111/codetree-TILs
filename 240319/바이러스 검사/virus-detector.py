import sys
import math

# sys.stdin = open("input.txt")
input = sys.stdin.readline

N = int(input())
customers = list(map(int, input().split()))
LDR, MBR = map(int, input().split())

answer = 0 
for customer in customers:
    #-- step1. 검사팀장 1명이 먼저 검사
    answer += 1
    customer = customer-LDR 
    
    if customer <= 0: #-- 검사 할 인원이 남아있지 않다면 pass
        pass
    else:
        answer += math.ceil(customer / MBR)
print(answer)