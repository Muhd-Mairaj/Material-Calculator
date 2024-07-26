
from decimal import Decimal
from random import randint
from typing import Callable


def sort_d(item):
    stop = 0
    while True:
        if stop == len(item):
            break
        for x in range(len(item) - 1):
            if item[x] < item[x + 1]:
                item[x], item[x + 1] = item[x + 1], item[x]
        stop += 1
    return item


old = 0
new = 0

def check_better():
    global old, new

    if required1 < required2:
        old += 1

    elif required2 < required1:
        new += 1

    elif required1 == required2:
        if scrap1 + (excess1 - excess2) == scrap2:
            if scrap2 > scrap1 and excess1 > excess2:
                old += 1

            elif scrap1 > scrap2 and excess2 > excess1:
                new += 1

            elif scrap1 == scrap2 and excess1 == excess2:
                old += 1
                new += 1

        else:
            assert scrap1 + (excess1 - excess2) == scrap2, "EXAMINE THE CODE. VALUES DON'T ADD UP *1*"

    else:
        raise Exception("How did we reach this")


def combinations_method(arr, combinations_custom: Callable):
    global stopping, x_index, y_index


    material = 12000
    required = 1
    scrap = 0
    excess = 0
    order_of_slice = []

    sort_d(arr)
    while len(arr) >= 1:
        material = 12000
        material -= Decimal(arr[0])
        order_of_slice.append(arr[0])
        arr.pop(0)

        if len(arr) == 0:
            break

        all_combinations = []
        stopping = False
        x_index = 0
        y_index = 0
        for x in range(1, len(arr) + 1):
            combination = list(combinations_custom(arr, x, material))
            if combination == []:
                break
            all_combinations.append(combination)
            if stopping:
                break

        if len(all_combinations) == 0:
            scrap += material
            required += 1
            continue

        best_combination = best_combination_of(all_combinations)

        for value in best_combination:
            material -= Decimal(value)
            pop_index = arr.index(value)
            order_of_slice.append(arr[pop_index])
            arr.pop(pop_index)

        if len(arr) >= 1:
            scrap += material
            required += 1
        else:
            break
    else:
        required = 0
        material = 0

    excess = material

    return required, excess, scrap


def combinations_custom_old(iterable, r, metal):
    global stopping, x_index, y_index

    pool = [item for item in iterable if Decimal(item) <= metal]
    for item in pool:
        # if Decimal(item) >= (metal - Decimal("100")) and Decimal(item) <= metal:
        if (metal - Decimal("100")) <= Decimal(item) <= metal:
            yield [item]
            stopping = True
            return
    n = len(pool)
    if r > n:
        return

    indices = list(range(r))
    comb_sum = sum(list(Decimal(pool[i]) for i in indices))
    # if comb_sum >= (metal - Decimal("100")) and comb_sum <= metal:
    if (metal - Decimal("100")) <= comb_sum <= metal:
        yield list(pool[i] for i in indices)
        stopping = True
        x_index = r - 1
        y_index = -1
        return
    elif comb_sum <= metal:
        yield list(pool[i] for i in indices)

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return

        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1

        comb_sum = sum(list(Decimal(pool[i]) for i in indices))
        # if comb_sum >= (metal - Decimal("100")) and comb_sum <= metal:
        if (metal - Decimal("100")) <= comb_sum <= metal:
            yield list(pool[i] for i in indices)
            stopping = True
            x_index = r - 1
            y_index = -1
            return
        elif comb_sum <= metal:
            yield list(pool[i] for i in indices)


def combinations_custom_new(iterable, r, metal):
    global stopping, x_index, y_index

    METAL = metal
    METAL_LESS_SOME = (metal - Decimal("100"))


    pool = [item for item in iterable if Decimal(item) <= METAL]
    for item in pool:
        if METAL_LESS_SOME <= Decimal(item) <= METAL:
            yield [item]
            stopping = True
            return

    n = len(pool)
    if r > n:
        return

    indices = list(range(r))
    comb_sum = sum(list(Decimal(pool[i]) for i in indices))
    if METAL_LESS_SOME <= comb_sum <= METAL:
        yield list(pool[i] for i in indices)
        stopping = True
        x_index = r - 1
        y_index = -1
        return
    elif comb_sum <= METAL:
        yield list(pool[i] for i in indices)

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return

        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1

        comb_sum = sum(list(Decimal(pool[i]) for i in indices))
        if METAL_LESS_SOME <= comb_sum <= METAL:
            yield list(pool[i] for i in indices)
            stopping = True
            x_index = r - 1
            y_index = -1
            return
        elif comb_sum <= METAL:
            yield list(pool[i] for i in indices)



def best_combination_of(arr):
    global x_index, y_index

    if y_index != 0:
        return arr[x_index][y_index]

    total = 0
    for index_list, type_of_combination in enumerate(arr):
        combination_total = 0
        y = 0
        for index, combination in enumerate(type_of_combination):
            sum_numbers = 0
            for value in combination:
                sum_numbers += Decimal(value)

            if combination_total < sum_numbers <= 12000:
                combination_total = sum_numbers
                y = index

        if total < combination_total <= 12000:
            total = combination_total
            x_index = index_list
            y_index = y

    return arr[x_index][y_index]



for _ in range(10000):
    arr1 = [str(randint(1000, 12000)) for _ in range(randint(1,300))]
    arr2 = [x for x in arr1]

    required1, excess1, scrap1 = combinations_method(arr1, combinations_custom_old)
    required2, excess2, scrap2 = combinations_method(arr2, combinations_custom_new)

    check_better()

print("old percent:", (old/1000) * 100)
print("new percent:", (new/1000) * 100)
