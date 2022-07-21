import copy
import random
from tkinter import *
from tkinter import messagebox


def evaluation_horner(coefficient_list, my_val):
    output_val = coefficient_list[0]
    for it in range(1, len(coefficient_list)):
        output_val = coefficient_list[it] + output_val * my_val
    return output_val


def method_dehghan(coefficient_list, r):
    x = random.uniform(-r, r)
    delta_x = 10 ** 7
    iteration = 0
    eps = 10 ** (-6)
    max_value = 10 ** 8
    while max_value > abs(delta_x) > eps and iteration < 500:
        px = evaluation_horner(coefficient_list, x)
        if abs(px) <= eps / 10:
            delta_x = 0
        else:
            px_plus = evaluation_horner(coefficient_list, (x + px))
            px_minus = evaluation_horner(coefficient_list, (x - px))
            py = evaluation_horner(coefficient_list, (x - (px * px * 2) / (px_plus - px_minus)))
            delta_x = (2 * px * (px + py)) / (px_plus - px_minus)
        x = x - delta_x
        iteration += 1
    if abs(delta_x) < eps:
        return x
    else:
        return None


def big_algo(coefficient_list, iterations):
    my_list = []
    a = coefficient_list[0]
    for it_val in coefficient_list:
        abs_val = abs(it_val)
        if abs_val > a:
            a = copy.deepcopy(abs_val)
    r = (abs(coefficient_list[0]) + a) / abs(coefficient_list[0])
    for current in range(iterations):
        result = method_dehghan(coefficient_list, r)
        if result is not None and round(result) not in my_list and -r <= round(result) <= r:
            my_list.append(result)
    print(my_list)


if __name__ == '__main__':
    TOP = Tk()
    TOP.bind("<Return>", big_algo)
    TOP.geometry("800x800")
    TOP.configure(background="#8c52ff")
    TOP.title("Lab7 CN")
    TOP.resizable(width=False, height=False)
    coefficient = [8, -38, 49, -22, 3]
    LABLE = Label(TOP, bg="#8c52ff", fg="#ffffff", text="Laborator7 CN", font=("Helvetica", 15, "bold"), pady=10)
    LABLE.place(x=55, y=0)

    BUTTON2 = Button(bg="#000000", fg='#ffffff', bd=12, text="Exercitiu", padx=33, pady=10,
                     command=big_algo(coefficient, 100),
                     font=("Helvetica", 20, "bold"))
    BUTTON2.grid(row=5, column=0, sticky=W)
    BUTTON2.place(x=55, y=151)
    TOP.mainloop()
