import sys
n = int(sys.stdin.readline())

classRoom = []
className = ['A', 'B', 'C', 'D']
maxVal = 0
maxIdx = 0
for i in range(4):
    data = sys.stdin.readline().split()
    data = data[1:]
    classRoom.append(list(map(int, data)))
    if sum(classRoom[i]) >= maxVal:
        maxVal = sum(classRoom[i])
        maxIdx = i
        
for i in range(4):
    print('{} - {}'.format(className[i], sum(classRoom[i])))
print('Class {} is winner!'.format(className[maxIdx]))