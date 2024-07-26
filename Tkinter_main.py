from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from decimal import Decimal
from random import randint, randrange, uniform
import re, openpyxl, os, time
from typing import Literal



USER = os.getlogin()
BASE_DIR = os.path.abspath(os.sep)
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
ONEDRIVE_DESKTOP_PATH = os.path.join(BASE_DIR, "users", USER, "onedrive", "desktop")
# USER_DESKTOP_PATH = os.path.join(cur_dir, "users", user_name, "desktop")
USER_DESKTOP_PATH = os.path.join(BASE_DIR, "onedrive", "desktop")

# Required variable initiations

log_file_path = ""
excel_file_path = ""


items_list1 = []
items_list2 = []
leaving1 = False  # For main function to distinguish app just launched from 'return' to frame1
leaving2 = False  # For main function to distinguish app just launched from 'return' to frame2



def get_info_file():
    """
    Return the contents of the info file as a list of lines
    """
    with open(os.path.join(CUR_DIR, "Resources", "info.txt"), "a+") as f:
        f.seek(0, 0)
        lines = f.read().split("\n")

    if len(lines) == 1 and lines[0] == "":
        return []

    print(repr(lines))
    return lines


def find_attr_in_info_file(attr: str):
    """
    return the required value if found else return 'False'
    """
    lines = get_info_file()

    for line in lines:
        attribute, value = line.split("=", maxsplit=1)
        if attr == attribute:
            return value
    return False


def add_or_replace_attr_in_info_file(attr: str, value: str):
    """
    Rewrite every line in the info file with the following rules:\n
        - if the attr already exists, replaces the attr
        - else, adds the attribute in the rewritten file
    
    :param attr: The attribute to add or replaces
    :param value: The required new value of the chosen attribute

    """
    lines = get_info_file()

    add_attr = True
    rewritten_lines = []
    for line in lines:
        attribute = line.split("=", maxsplit=1)[0]

        if attr == attribute:
            add_attr = False
            rewritten_lines.append(f"{attr}={value}")
        else:
            rewritten_lines.append(line)

    if add_attr:
        rewritten_lines.append(f"{attr}={value}")

    with open(os.path.join(CUR_DIR, "Resources", "info.txt"), "w") as f:
        f.write("\n".join(rewritten_lines))


# Function for finding the best combinations


def combinations_custom(iterable, r, metal):
    global stopping, x_index, y_index

    metal_less_some = (metal - Decimal("100"))

    pool = [item for item in iterable if Decimal(item) <= metal]
    for item in pool:
        # if Decimal(item) >= (METAL - Decimal("100")) and Decimal(item) <= METAL:
        if metal_less_some <= Decimal(item) <= metal:
            yield [item]
            stopping = True
            return
    n = len(pool)
    if r > n:
        return

    indices = list(range(r))
    comb_sum = sum(list(Decimal(pool[i]) for i in indices))
    # if comb_sum >= METAL_LESS_SOME and comb_sum <= METAL:
    if metal_less_some <= comb_sum <= metal:
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
        # if comb_sum >= METAL_LESS_SOME and comb_sum <= METAL:
        if metal_less_some <= comb_sum <= metal:
            yield list(pool[i] for i in indices)
            stopping = True
            x_index = r - 1
            y_index = -1
            return
        elif comb_sum <= metal:
            yield list(pool[i] for i in indices)


# Function for sorting items in descending order


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


# Function to find the best combination from all combinations


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


# Function to simplify the order of slicing


def find_and_log_show_order(order_of_slice):

    show_order = find_show_order(order_of_slice)

    log_order_of_slice(show_order)

    return show_order


def log_order_of_slice(show_order):
    global log_file_path


    log_file_path = find_attr_in_info_file("log_file_path")

    # Fixes the issue where log file path is not chosen. and the program is still intitiated.
    # This situtation should not arise, and this bit is reduntant, 
    # but is included for the safety of the functioning of the program
    # and also to not have a different default location than the one chose by the user
    while not log_file_path:
        messagebox.showinfo("No Log File Selected", "Please choose the directory for your log file")
        user_choose_log_path()

    # if log_file_path:
    log_file = os.path.join(log_file_path, "log.txt")
    # elif os.path.exists(ONEDRIVE_DESKTOP_PATH):
    #     log_file = os.path.join(ONEDRIVE_DESKTOP_PATH, "log.txt")
    # else:
    #     log_file = os.path.join(USER_DESKTOP_PATH, "log.txt")

    # with open(log_file, "a") as f:
    #     f.write(f"order_of_slice: {show_order}\n\n")


def find_show_order(order_of_slice):
    show_order = []
    summation = 0
    while len(order_of_slice) >= 1:
        item = order_of_slice[0]
        if summation + Decimal(item) > 12000:
            show_order.append(f"|{summation}|")
            summation = 0
        summation += Decimal(item)
        # show_order.append(float(item))
        show_order.append(f"{float(item)} ({float(summation)})")
        # order_of_slice.pop(order_of_slice.index(item))
        order_of_slice.pop(0)

    show_order.append(f"|{summation}|")

    return show_order  # Returns simplified order, with total used per material in 'pipe' character
    # ["a", "b", "c", "x", "y", "z"] --> [a, b, c, |sum|, x, y, z, |sum|]


# Function for Combinations Method


def combinations_method(arr):
    global show_order1, required1, scrap1, excess1
    global stopping, x_index, y_index

    print(f"The length of the list we're working with: {len(arr)}")
    print(arr)
    print("\nUSING COMBINATION METHOD")

    material = 12000
    required1 = 1
    scrap1 = 0
    excess1 = 0
    order_of_slice = []

    # sort_d(arr)
    arr.sort()
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
            scrap1 += material
            required1 += 1
            continue

        best_combination = best_combination_of(all_combinations)

        for value in best_combination:
            material -= Decimal(value)
            pop_index = arr.index(value)
            order_of_slice.append(arr[pop_index])
            arr.pop(pop_index)

        if len(arr) >= 1:
            scrap1 += material
            required1 += 1
        else:
            break
    else:
        required1 = 0
        material = 0

    excess1 = material

    show_order1 = find_and_log_show_order(order_of_slice)

    print(f"\033[1;32;40m\n\nrequired raw material: {required1}")
    print(f"order of slice: {show_order1}")
    print(f"total scrap: {scrap1}")
    print(f"excess at the end: {excess1}\033[1;37;40m \n")


# Function for Sorting Method


def sort_method(arr):
    global show_order2, required2, scrap2, excess2

    print("\nUSING SORTING METHOD")
    # sort_d(arr)
    arr.sort()

    material = 12000
    required2 = 1
    scrap2 = 0
    order_of_slice = []

    while len(arr) >= 1:
        for index, i in enumerate(arr):
            if material - Decimal(i) < 0:
                continue
            material -= Decimal(i)
            order_of_slice.append(arr[index])
            arr.pop(index)
            break
        else:
            required2 += 1
            scrap2 += material
            material = 12000

        if len(arr) == 0:   # Unnecesary ???
            break
    else:
        required2 = 0
        material = 0
    excess2 = material

    show_order2 = find_and_log_show_order(order_of_slice)

    print(f"\033[1;32;40m\n\nrequired raw material: {required2}")
    print(f"order of slice: {show_order2}")
    print(f"total scrap: {scrap2}")
    print(f"excess at the end: {excess2}\033[1;37;40m \n")


# Function to add entries to the treeview in enter values tab

iid_count1 = 0

def add_values():
    global iid_count1, items_list1, items_list2

    # items_list1 = [str(round(uniform(1, 7), 3)) for _ in range(100)]
    # items_list2 = [item for item in items_list1]

    quantity = quantity_entry.get().strip()
    values = values_entry.get().strip()

    if not quantity.isdigit() or not values.isdigit():
        raise Exception("Quantity or Values not given")

    for _ in range(int(quantity)):
        items_list1.append(values)
        items_list2.append(values)

    iid_count1 += 1

    tree1.insert(
        parent="",
        index=END,
        iid=iid_count1,
        text="",
        values=(values, quantity),
    )

    values_entry.delete(0, END)
    quantity_entry.delete(0, END)

    show_list = [float(element) for element in items_list1]
    print(f"\nYour items are as follows: {show_list}")


# Function to remove entry from the treeview in enter values tab


def remove_value():
    rem_iid = tree1.focus()       # gives iid of treeview row
    rem_values = tree1.item(rem_iid, "values")  # gives 'values' of the selected row
                                                    # --> ("item length", "quantity")
    tree1.delete(rem_iid)  # deletes row from treeview

    for _ in range(int(rem_values[1])):  # deletes corresponding values from the items lists
        items_list1.remove(rem_values[0])
        items_list2.remove(rem_values[0])

    show_list = [float(element) for element in items_list1]
    print(f"\nYour items are as follows: {show_list}")


# function to check which did better


def check_which_better(
    better: Label,
) -> Literal["Combination method", "Sort method", "Same"]:
    """Checks which method did better and modifies the required label to show it"""
    return_value = ""

    if required1 == required2:

        if scrap1 + (excess1 - excess2) == scrap2:
            if scrap2 > scrap1 and excess1 > excess2:
                better.config(text="Combination method was better")
                return_value = "Combination method"

            elif scrap1 > scrap2 and excess2 > excess1:
                better.config(text="Sort method was better")
                return_value = "Sort method"

            elif scrap1 == scrap2 and excess1 == excess2:
                better.config(text="Both methods are the exact same")
                return_value = "Same"

            else:
                better.config(text="EXAMINE THE CODE. VALUES DON'T ADD UP *1*")
                assert (
                    scrap1 + (excess1 - excess2) == scrap2
                ), "EXAMINE THE CODE. VALUES DON'T ADD UP *1*"

        else:
            better.config(text="EXAMINE THE CODE. VALUES DON'T ADD UP *2*")
            assert (
                scrap1 + (excess1 - excess2) == scrap2
            ), "EXAMINE THE CODE. VALUES DON'T ADD UP *2*"

    elif required1 < required2:
        better.config(text="Combination method")
        return_value = "Combination method"

    elif required1 > required2:
        better.config(text="Sort method is better")
        return_value = "Sort method"

    return return_value


# Function that handles all requirements when 'Done' is pressed


def run():
    # add_values()
    global show_order1, required1, scrap1, excess1
    global show_order2, required2, scrap2, excess2
    global frame1, frame2, my_notebook
    global root, window
    global leaving1, leaving2

    # Defines True that Output window has been activated
    if root.tk_focusPrev().winfo_parent() == frame1.__str__():
        leaving1 = True
    elif root.tk_focusPrev().winfo_parent() == frame2.__str__():
        leaving2 = True


    # Remove unnecessary widgets

    root.destroy()

    window = Tk()
    window.title("MATERIAL COUNTER")
    window.config(bg="black")
    window.bind("<Alt-F4>", lambda event: window.destroy())

    ##### ---------- Make Widgets ---------- #####

    # Textbox for better method

    display_textbox = Text(
        master=window,
        bg="#A9A9A9",
        fg="black",
        font="consolas 11 bold",
        spacing1=0,
        spacing2=2,
        height=10,
        width=100,
        wrap=WORD,
    )

    # Label for which did better

    better_label = Label(
        master=window,
        bg="black",
        fg="green",
        text="",
        font="consolas 16",
    )

    # Button to return back to main menu or exit

    back_button = Button(
        master=window,
        bg="green",
        fg="white",
        text="Return",
        font="helvetica 12",
        pady=2,
        padx=7,
        command=main,
    )

    ########## -------------------- Output -------------------- ##########

    # Use the two methods

    combinations_method(items_list1)
    sort_method(items_list2)

    # Check which did better and display it on the required label

    which_better = check_which_better(better_label)

    # Add text about combinations method

    if (which_better == "Combination method") or (which_better == "Same"):
        required = required1
        scrap = scrap1
        excess = excess1
        show_order = show_order1

    elif which_better == "Sort method":
        required = required2
        scrap = scrap2
        excess = excess2
        show_order = show_order2

    display_textbox.insert(END, f"required: {required}\n")
    display_textbox.insert(
        END,
        "---------------------------------------------------------------------------------------------------\n",
    )
    display_textbox.insert(END, f"Total scrap: {scrap}\n")
    display_textbox.insert(
        END,
        "---------------------------------------------------------------------------------------------------\n",
    )
    display_textbox.insert(END, f"Excess: {excess}\n")
    display_textbox.insert(
        END,
        "---------------------------------------------------------------------------------------------------\n",
    )
    display_textbox.insert(END, f"order of slice: {show_order}\n")
    display_textbox.config(state=DISABLED)

    display_textbox.pack(padx=5, pady=(8, 0))

    better_label.pack(padx=2, pady=(5, 0), anchor=CENTER)
    back_button.pack(padx=5, pady=5, anchor=W)

    # Additional Information for me

    window.update()
    app_width = window.winfo_reqwidth()
    app_height = window.winfo_reqheight()
    window.geometry(f"{app_width}x{app_height}+{100}+{50}")

    window.mainloop()


# Regular expression to find "path of the file/file.xlsx"

regex = re.compile(r".*.xlsx")

# Define Functions to get file path

def get_path():
    global excel_file_path

    # filename = ""
    excel_file_path = filedialog.askopenfilename()
    print("file_path:", excel_file_path)

    if len(excel_file_path) >= 1:
        mo = regex.search(excel_file_path)
        print(mo)
        if mo is None:
            selected_path_label.config(fg="red", text="Please select Excel File")
            excel_file_path = ""
        else:
            print(mo.group())
            display_filename = mo.group().split("/")[-1]  # gets "file.xlsx" from "path to file/file.xlsx"
            selected_path_label.config(fg="green", text=f"File selected: {display_filename}")


# Find the row no. with values, column no. of profiles, quantities and lenghts
# as well as which rows to skip and when to stop


def find_rows_and_columns(sheet):
    global start_row, stop_row, skip_rows
    global profile_column, length_column, qty_column

    start_row = 1
    profile_column = 0
    length_column = 0
    qty_column = 0
    for row in range(1, 1001):
        for column in range(1, 51):
            cell_value = sheet.cell(row=row, column=column).value

            if cell_value == None:
                continue
            elif cell_value.lower() == "profile":
                profile_column = column
            elif cell_value.lower() == "qty.":
                qty_column = column
            elif cell_value.lower() == "length":
                length_column = column

        start_row += 1
        if profile_column and length_column and qty_column != 0:
            break

    stop_row = 1001
    skip_rows = []
    for row in range(start_row, 1001):
        cell_value = sheet.cell(row=row, column=profile_column).value
        if cell_value == None:
            stop_row = row
            break
        elif "pl" in cell_value.lower():
            skip_rows.append(row)
            continue
            # stop_row = row
            # break
    print(skip_rows)


iid_count2 = 0

def add_values2():
    global excel_file_path
    global iid_count2
    global items_list1, items_list2
    global skip_rows

    wb = openpyxl.load_workbook(excel_file_path)
    sheets = wb.sheetnames
    sheet = wb[sheets[0]]

    # finds the row, and the required columns

    find_rows_and_columns(sheet)

    print(f"start row: {start_row}")
    print(f"profile column: {profile_column}")
    print(f"length_column: {length_column}")
    print(f"qty column: {qty_column}")
    print(f"stop row: {stop_row}")

    # Extract values from the correct rows and columns

    for row in range(start_row, stop_row):
        if row in skip_rows:
            continue

        iid_count2 += 1
        length_value = sheet.cell(row=row, column=length_column).value
        qty_value = sheet.cell(row=row, column=qty_column).value

        if length_value == None or qty_value == None:
            raise Exception("I am not supposed to reach here")
            # break      # this prolly should be continue but we'll find out once the exception is raised

        tree2.insert(
            parent = "",
            index  = END,
            iid    = iid_count2,
            text   = "",
            values = (length_value, qty_value),
        )

        for _ in range(qty_value):
            items_list1.append(Decimal(length_value))
            items_list2.append(Decimal(length_value))


def user_choose_log_path(master: Tk=None, label=None):
    global log_file_path


    log_file_path = filedialog.askdirectory()

    if (master is not None) and (label is not None):
        if len(log_file_path) == 0:     # i.e. No file selected
            label.config(fg="red", font="helvetica 12 bold", text=f"NO FILE SELECTED")

            return

        label.config(
            fg="green",
            font="helvetica 12 bold",
            text=f"Path selected: {log_file_path}\n\nProcessing...",
        )
        master.update()

        width = master.winfo_reqwidth()
        master.geometry(f"{width}x300")
        master.update()

    else:
        if len(log_file_path) == 0:     # i.e. No file selected
            return

    print(log_file_path)
    # if not find_attr_in_info_file("log_file_path"):

    #     with open(os.path.join(CUR_DIR, "Resources", "info.txt"), "a+") as f:
    #         f.write(f"log_file_path={log_file_path}\n")

    # else:
    add_or_replace_attr_in_info_file("log_file_path", log_file_path)


# Main Function - Shows tkinter view


def main():
    global frame1, frame2, my_notebook, tree1, tree2
    global values_entry, quantity_entry
    global root, leaving1, leaving2
    global selected_path_label

    if leaving1 or leaving2:
        window.destroy()

    root = Tk()
    root.title("MATERIAL COUNTER")
    root.geometry("340x407")
    root.config(bg="black")
    root.bind("<Alt-F4>", lambda event: root.destroy())

    my_menu = Menu(root)  # , cnf={"font": "times 12"})
    root.config(menu=my_menu)

    # file_menu = Menu(my_menu, tearoff=0, bg="#dddddd", font="times 12")
    my_menu.add_command(label="Choose log file path", command=user_choose_log_path)
    # my_menu.add_cascade(label="   File   ", menu=file_menu)


    # Create Notebook

    my_notebook = ttk.Notebook(root)
    my_notebook.pack(pady=(3, 0))

    # Make frames for each tab

    frame1 = Frame(my_notebook, width=400, height=400, bg="black")
    frame2 = Frame(my_notebook, width=400, height=400, bg="black")

    # Make tabs

    my_notebook.add(frame1,text="Enter Values")
    my_notebook.add(frame2, text="Choose Excel File")

    tab_id = frame2.__str__() if leaving2 else frame1.__str__()  # focus tab2 if return from tab2 else focus tab1 -> implies default tab1
    my_notebook.select(tab_id=tab_id)

    leaving1, leaving2 = False, False

    ##########------------------- FRAME1 ------------------- ##########

    # Defining style for treeview

    style = ttk.Style()
    style.theme_use("alt")
    style.configure(
        "Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=20,
        fieldbackground="#D3D3D3",
    )
    style.map("Treeview", background=[("selected", "#1338bb")])


    ###### ---------- Make Widgets ---------- #####

    values_label = Label(frame1, text="Enter length of item: ", anchor=W, font="times 14")
    values_label.grid(row=1, column=1, padx=(3, 0), pady=(3, 0), sticky="news")

    values_entry = Entry(frame1, width=15, justify="center", font="times 12")
    values_entry.bind("<Return>", lambda event: quantity_entry.focus())
    values_entry.grid(row=1, column=2, padx=(3, 2), pady=(3, 0), ipady=3)

    quantity_label = Label(frame1, text="Enter quantity of this item: ", font="times 14")
    quantity_label.grid(row=2, column=1, padx=(3, 0), pady=(3, 0), sticky="news")

    quantity_entry = Entry(frame1, width=15, justify="center", font="times 12")
    quantity_entry.bind("<Return>", lambda event: add_values())
    quantity_entry.bind("<Return>", lambda event: values_entry.focus(), add="+")
    quantity_entry.grid(row=2, column=2, padx=(3, 2), pady=(3, 0), ipady=3)

    add_button = Button(frame1, text="Add Values", font="times 13", pady=2, command=add_values)
    add_button.bind("<Return>", lambda event: add_values())
    add_button.bind("<Return>", lambda event: values_entry.focus(), add="+")
    add_button.grid(row=3, column=2, padx=(0, 15), pady=(5, 0), sticky=E)

    remove_button = Button(frame1, text="Remove Value", font="times 13", pady=2, command=remove_value)
    remove_button.grid(row=3, column=1, columnspan=2, padx=(10, 4), pady=(5, 0))

    # Treeview

    tree1 = ttk.Treeview(frame1)
    tree1["columns"] = ("Item", "Quantity")
    tree1.column("#0", width=0, minwidth=0)
    tree1.column("Item", width=120, minwidth=25)
    tree1.column("Quantity", width=120, minwidth=25)

    # Treeview Headings

    tree1.heading("Item", text="Item Length", anchor=W)
    tree1.heading("Quantity", text="Quantity", anchor=W)
    tree1.grid(row=4, column=1, columnspan=2, padx=(3, 3), pady=(5, 0), sticky=W)
    tree1.bind("<KeyPress-Delete>", lambda event: remove_value())
    tree1.bind("<KeyPress-Delete>", lambda event: values_entry.focus(), add="+")

    done_button = Button(frame1, text="Done", font="times 13", padx=20, pady=2, command=run    )
    done_button.grid(row=5, column=2, padx=3, pady=(5, 0), sticky=E)

    # Bindings

    ##########------------------- FRAME2 ------------------- ##########

    # Make widgets

    choose_path_label = Label(
        master=frame2,
        bg="black",
        fg="white",
        text="Select the path of the Excel File",
        font="helvetica 12",
    )

    choose_path_button = Button(
        master=frame2,
        bg="green",
        fg="white",
        text="Select",
        font="times 12",
        padx=17,
        command=get_path,
    )

    selected_path_text = "No file selected" if not excel_file_path else excel_file_path
    selected_path_colour = "red" if not excel_file_path else "green"
    selected_path_label = Label(
        master=frame2,
        bg="black",
        fg=selected_path_colour,
        text=selected_path_text,
        font="helvetica 12 bold",
    )

    extract_button = Button(
        frame2,
        bg="green",
        fg="white",
        text="Get values",
        font="times 12",
        padx=3,
        command=add_values2,
    )

    done_button2 = Button(
        frame2,
        bg="green",
        fg="white",
        text="Done",
        font="times 12",
        padx=15,
        command=run,
    )

    # # Making treeview number 2

    # check_box_frame = Frame(frame2)

    # tree2

    tree2 = ttk.Treeview(frame2)
    tree2["columns"] = ("Item", "Quantity")
    tree2.column("#0", width=0, minwidth=0, stretch=NO)
    tree2.column("Item", width=105, minwidth=25)
    tree2.column("Quantity", width=105, minwidth=25)

    # Treeview number 2 Headings

    tree2.heading("Item", text="Item Length", anchor=W)
    tree2.heading("Quantity", text="Quantity", anchor=W)

    # Place Widgets

    choose_path_label.grid(row=1, column=1, padx=(3, 0), pady=(3, 0), sticky="news")
    choose_path_button.grid(row=2, column=1, padx=(3, 0), pady=(3, 0))
    selected_path_label.grid(row=3, column=1, padx=(3, 0), pady=(3, 0))
    extract_button.grid(row=4, column=1, padx=(3, 0), pady=(5, 0))
    tree2.grid(row=5, column=1, padx=(3, 3), pady=(5, 0), sticky=W)
    done_button2.grid(row=5, column=2, padx=(3, 3), sticky=S + E)

    # Additional info for me

    root.update()
    app_width = root.winfo_reqwidth()
    app_height = root.winfo_reqheight()
    print(f"width x height = {app_width} x {app_height}")

    root.mainloop()


def initial_dialog():

    def initial_dialog_done():
        if log_file_path:
            root.destroy()
        else:
            display_path_label.config(text="Please choose log file path!!!", fg="red")

    log_file_path = find_attr_in_info_file("log_file_path")

    if log_file_path:
        return

    root = Tk()
    root.geometry("350x300")
    root.config(bg="black")
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=10)
    root.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=5)

    frame0 = Frame(root, bg="black")
    frame0.grid(row=0, column=0, sticky="news", padx=5)
    frame1 = Frame(root, bg="black")
    frame1.grid(row=1, column=0, sticky="news", padx=5)
    frame2 = Frame(root, bg="black")
    frame2.grid(row=2, column=0, sticky="news", padx=5)

    frame1.rowconfigure(0, weight=1)
    frame1.rowconfigure(1, weight=1)
    frame1.columnconfigure(0, weight=1)
    frame2.rowconfigure(0, weight=1)
    frame2.columnconfigure(0, weight=1)
    frame2.columnconfigure(1, weight=1)

    title_label = Label(
        master=frame0,
        bg="black",
        fg="white",
        text="Select the path of the Log File",
        font="helvetica 14 bold",
    )
    title_label.pack(fill="x", expand=True)

    display_path_label = Label(
        master=frame1,
        bg="black",
        fg="red",
        text="No file selected",
        font="helvetica 12 bold",
    )
    display_path_label.pack(fill="both", expand=True)

    done_button = Button(
        master=frame2,
        bg="green",
        fg="white",
        text="Done",
        font="times 12",
        padx=17,
        command=initial_dialog_done,
    )
    done_button.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    select_button = Button(
        master=frame2,
        bg="green",
        fg="white",
        text="Select",
        font="times 12",
        padx=17,
        command=lambda: user_choose_log_path(master=root, label=display_path_label),
    )
    select_button.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":

    initial_dialog()

    main()
