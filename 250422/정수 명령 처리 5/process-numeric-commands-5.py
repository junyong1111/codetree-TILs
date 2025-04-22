N = int(input())

answer = []
for i in range(N):
    order = input().split()
    if order[0] =='push_back':
        answer.append(int(order[1]))
    elif order[0] =='get':
        try:
            print(answer[int(order[1])-1])
        except:
            pass
    elif order[0] == 'size':
        print(len(answer))
    elif order[0] =='pop_back':
        try:
            answer.pop()
        except:
            pass