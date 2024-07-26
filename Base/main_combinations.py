from decimal import Decimal
import gc
import msvcrt

"""
Runs combination method for 200 values else sorting method
Ready to use
"""


def combinations_custom(iterable, r, metal):
    global stopping, x_index, y_index

    pool = [item for item in iterable if Decimal(item) <= metal]
    for item in pool:
        if Decimal(item) >= (metal - Decimal("0.1")) and Decimal(item) <= metal:
            yield [item]
            stopping = True
            return
    n = len(pool)
    if r > n:
        return

    indices = list(range(r))
    combination_sum = sum(list(Decimal(pool[i]) for i in indices))
    if combination_sum >= (metal - Decimal("0.1")) and combination_sum <= metal:
        yield list(pool[i] for i in indices)
        stopping = True
        x_index = (r - 1)
        y_index = -1
        return
    elif combination_sum <= metal:
        yield list(pool[i] for i in indices)

    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
            
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        combination_sum = sum(list(Decimal(pool[i]) for i in indices))
        
        if combination_sum >= (metal - Decimal("0.1")) and combination_sum <= metal:
            yield list(pool[i] for i in indices)
            stopping = True
            x_index = (r - 1)
            y_index = -1
            return
        elif combination_sum <= metal:
            yield list(pool[i] for i in indices)


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


def requirement(arr):
    global stopping, x_index, y_index

    print(f"The length of the list we're working with: {len(arr)}")
    if len(arr) <= 300:
        print("\nUSING COMBINATION METHOD")
        required = 1
        scrap = 0
        order_of_slice = []

        sort_d(arr)
        while len(arr) >= 1:
            gc.collect()

            material = 12
            material -= Decimal(arr[0])
            order_of_slice.append(arr[0])
            arr.pop(0)

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

            if x_index == 0 and y_index == 0:
                total = 0
                for index_list, type_of_combination in enumerate(all_combinations):

                    combination_total = 0
                    y = 0
                    for index, combination in enumerate(type_of_combination):

                        sum_numbers = 0
                        for value in combination:
                            sum_numbers += Decimal(value)

                        if combination_total < sum_numbers and sum_numbers <= 12:
                            combination_total = sum_numbers
                            y = index

                    if total < combination_total and combination_total <= 12:
                        total = combination_total
                        x_index = index_list
                        y_index = y

            for value in all_combinations[x_index][y_index]:
                material -= Decimal(value)
                pop_index = arr.index(value)
                order_of_slice.append(arr[pop_index])
                arr.pop(pop_index)

            if len(arr) >= 1:
                scrap += material
                required += 1
        excess = material

    else:
        print("\nUSING SORTING METHOD")
        sort_d(arr)

        material = 12
        required = 1
        scrap = 0
        order_of_slice = []

        while len(arr) >= 1:
            for index, x in enumerate(arr):
                if material - Decimal(x) < 0:
                    continue
                material -= Decimal(x)
                order_of_slice.append(arr[index])
                arr.pop(index)
                break
            else:
                required += 1
                scrap += material
                material = 12
        excess = material

    show_order = []
    summation = 0
    while len(order_of_slice) >= 1:
        for item in order_of_slice:
            if summation + Decimal(item) > 12:
                show_order.append(f"|{summation}|")
                summation = 0
            summation += Decimal(item)
            show_order.append(float(item))
            order_of_slice.pop(order_of_slice.index(item))
            break
    show_order.append(f"|{summation}|")

    print(f"\033[1;32;40m\n\nrequired raw material: {required}")
    print(f"order of slice: {show_order}")
    print(f"total scrap: {scrap}")
    print(f"excess at the end: {excess}\033[1;37;40m \n")

    with open(r"c:\users\rayya\onedrive\desktop\test.txt", "a") as text:
        text.write(f"order_of_slice: {show_order}\n")


def main():
    items_list = []
    while True:
        length = input(
            "\033[1;34;40m\nEnter the length of required item in m: ")
        quantity = int(input("\033[1;34;40mEnter quantity of this item: "))
        more = input("\033[1;31;40m\nTo stop making entries, type 'Stop': ")

        for _ in range(quantity):
            items_list.append(length)

        if more.lower() == "stop":
            break

    show_list = [float(element) for element in items_list]
    print(f"\nYour items are as follows: {show_list}")

    requirement(items_list)

# wait at the end


def wait():
    print("Press 'Enter' to exit")
    msvcrt.getch()


if __name__ == "__main__":
    main()
    # wait()
