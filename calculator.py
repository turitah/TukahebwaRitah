import tkinter as tk

# Functions
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

 
operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}

 
def calculate():
    try:
        num1 = int(entry1.get())
        num2 =  int(entry2.get())
        operator = operation.get()

        result = operations[operator](num1, num2)

        result_label.config(text=f"Result: {result}")

    except ZeroDivisionError:
        result_label.config(text="Cannot divide by zero!")

    except ValueError:
        result_label.config(text="Enter valid numbers!")

 
def clear():
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    result_label.config(text="Result:")

 
window = tk.Tk()
window.title("Calculator")
window.geometry("350x300")

 
title = tk.Label(window, text="Calculator", font=("Arial", 12))
title.pack(pady=10)

 
tk.Label(window, text="First Number").pack()
entry1 = tk.Entry(window, width=25)
entry1.pack()
 
tk.Label(window, text="Operation").pack()

operation = tk.StringVar()
operation.set("+")

menu = tk.OptionMenu(window, operation, "+", "-", "*", "/")
menu.pack()
 
tk.Label(window, text="Second Number").pack()
entry2 = tk.Entry(window, width=25)
entry2.pack()

 
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

calculate_button = tk.Button(
    button_frame,
    text="Calculate",
    command=calculate
)
calculate_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear
)
clear_button.grid(row=0, column=1, padx=5)

 
result_label = tk.Label(
    window,
    text="Answer:",
    font=("Arial", 12)
)
result_label.pack(pady=10)

window.mainloop()