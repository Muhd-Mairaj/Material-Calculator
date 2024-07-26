#! python39
# %%
from decimal import Decimal
from random import uniform
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")

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

def requirements(lst):
    sort_d(lst)

    material = 12
    required = 1
    scrap = 0
    order_of_slice = []

    while len(lst) >= 1:
        for index, x in enumerate(lst):
            if material - x < 0:
                continue
            material -= x
            order_of_slice.append(Decimal(lst[index]))
            lst.pop(index)
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
                continue
            summation += Decimal(item)
            show_order.append(float(item))
            order_of_slice.pop(order_of_slice.index(item))
            break
    show_order.append(f"|{summation}|")

    print(f"\033[1;32;40m\n\nMinimum raw material required is: {required}")
    print(f"order to slice: {show_order}")
    print(f"\033[1;32;40mTotal scrap: {scrap}")
    print(f"\033[1;32;40mExcess at the end: {excess}\n\033[1;37;40m \n")

    text = open(r"c:\users\rayya\onedrive\desktop\test.txt", "a")
    text.write(f"order_of_slice: {show_order}\n")
    text.close()

items_list = [str(round(uniform(1, 7), 3)) for item in range(100)]
items_list = [Decimal(x) for x in items_list]

"""
items_list = []
while True:
    length = Decimal(input("\033[1;34;40m\nEnter the length of required item in m: "))
    quantity = int(input("\033[1;34;40mEnter quantity of this item: "))
    more = input("\033[1;31;40m\nTo stop making entries, type 'Stop': ")
    
    for _ in range(quantity):
        items_list.append(length)
        
    if more.lower() == "stop":
        break
"""

show_list = [float(element) for element in items_list]
print(f"\033[1;34;40m\nYour items are as follows: {show_list}")

requirements(items_list)