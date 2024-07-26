import random

def sort_d(item):
    stop = False
    while not stop:
        stop = True
        for x in range(len(item) - 1):
            if item[x] < item[x + 1]:
                item[x], item[x + 1] = item[x + 1], item[x]
                stop = False
        
    return item

count_yes = 0
for _ in range(100):
    l = [random.randint(1, 10) for _ in range(1000)]
    y = [i for i in l]
    sort_d(l)

    if l == sorted(y, reverse=True):
        count_yes += 1
else:
    print(count_yes, "/ 100")