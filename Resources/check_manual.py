from typing import List
from decimal import Decimal


def trial6(arr: List[float]=[0.0]):
    """
    :param arr: The list of items as float objects, ordered in the manual slicing order
    """

    order_of_slice: List[str] = [str(x) for x in arr]
    arr = [Decimal(x) for x in order_of_slice]

    material = 12000
    required = 1
    scrap = 0
    excess = 0

    for value in arr:
        if material - value < 0:
            required += 1
            scrap += material
            material = 12000
        
        material -= value

    else:
        excess = material
        
    show_order = []
    summation = 0
    while len(order_of_slice) >= 1:
        item = order_of_slice[0]
        if summation + Decimal(item) > 12000:
            show_order.append(f"|{summation}|")
            summation = 0
        summation += Decimal(item)
        show_order.append(f"{float(item)} ({float(summation)})")
        order_of_slice.pop(0)

    show_order.append(f"|{summation}|")
    print("required:", required)
    print("scrap:", scrap)
    print("excess:", excess)
    print("Order of Slice:", show_order)

trial6()