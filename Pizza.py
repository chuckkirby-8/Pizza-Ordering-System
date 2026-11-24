import tkinter as tk
from tkinter import ttk, messagebox

pizza_prices = {
    "Triple Cheese": 250,
    "BBQ Chicken": 280,
    "Spicy Garlic Beef": 240,
    "Overload": 300
}

size_prices = {
    "Regular": 0,
    "Duo": 50,
    "Party": 100
}

topping_prices = {
    "Chili": 30,
    "Garlic": 40,
    "Mozarella": 50
}

window = tk.Tk()
window.title("Pizza Ordering System")
window.geometry("650x850")
window.resizable(True, True)
window.configure(bg="#16241d")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TerracottaForest.TCombobox",
    fieldbackground="#f7f3e8",
    background="#d96b38",
    foreground="#1b1f1d",
    arrowcolor="#1b1f1d"
)

pizza_var = tk.StringVar(value="Triple Cheese")
size_var = tk.StringVar(value="Small")
quantity_var = tk.IntVar(value=1)

topping_vars = {
    topping: tk.BooleanVar(value=False)
    for topping in topping_prices
}

title = tk.Label(
    window,
    text="EL Zabroso",
    font=("Arial", 15, "bold"),
    bg="#16241d",
    fg="#f2a679"
)
title.pack(pady=20)

order_frame = tk.Frame(
    window,
    bg="#23382e",
    padx=25,
    pady=20,
    highlightbackground="#2e4a3d",
    highlightthickness=1
)
order_frame.pack(padx=25, fill="x")

flavor_header = tk.Frame(order_frame, bg="#23382e")
flavor_header.pack(fill="x")

tk.Label(
    flavor_header,
    text="Select Pizza Flavor:",
    font=("Arial", 12, "bold"),
    bg="#23382e",
    fg="#f7f3e8"
).pack(side="left")

pizza_price_label = tk.Label(
    flavor_header,
    text=f"₱{pizza_prices[pizza_var.get()]}",
    font=("Arial", 12, "bold"),
    bg="#23382e",
    fg="#f2a679"
)
pizza_price_label.pack(side="right")


def update_pizza_price(*args):
    selected = pizza_var.get()
    if selected in pizza_prices:
        pizza_price_label.config(text=f"₱{pizza_prices[selected]}")


pizza_var.trace_add("write", update_pizza_price)

pizza_dropdown = ttk.Combobox(
    order_frame,
    textvariable=pizza_var,
    values=list(pizza_prices.keys()),
    state="readonly",
    style="TerracottaForest.TCombobox",
    font=("Arial", 11)
)
pizza_dropdown.pack(fill="x", pady=8)

tk.Label(
    order_frame,
    text="Select Pizza Size:",
    font=("Arial", 12, "bold"),
    bg="#23382e",
    fg="#f7f3e8"
).pack(anchor="w", pady=(12, 5))

for size, price in size_prices.items():
    tk.Radiobutton(
        order_frame,
        text=f"{size} (+₱{price})",
        variable=size_var,
        value=size,
        font=("Arial", 11),
        bg="#23382e",
        fg="#f7f3e8",
        selectcolor="#16241d",
        activebackground="#23382e",
        activeforeground="#f2a679"
    ).pack(anchor="w")

tk.Label(
    order_frame,
    text="Select Extra Toppings:",
    font=("Arial", 12, "bold"),
    bg="#23382e",
    fg="#f7f3e8"
).pack(anchor="w", pady=(12, 5))

for topping, price in topping_prices.items():
    tk.Checkbutton(
        order_frame,
        text=f"{topping} (+₱{price})",
        variable=topping_vars[topping],
        font=("Arial", 11),
        bg="#23382e",
        fg="#f7f3e8",
        selectcolor="#16241d",
        activebackground="#23382e",
        activeforeground="#f2a679"
    ).pack(anchor="w")

tk.Label(
    order_frame,
    text="Quantity:",
    font=("Arial", 12, "bold"),
    bg="#23382e",
    fg="#f7f3e8"
).pack(anchor="w", pady=(12, 5))

quantity_spinbox = tk.Spinbox(
    order_frame,
    from_=1,
    to=50,
    textvariable=quantity_var,
    font=("Arial", 12),
    bg="#f7f3e8",
    fg="#1b1f1d",
    buttonbackground="#f2a679",
    width=10
)
quantity_spinbox.pack(anchor="w")


def calculate_total():
    pizza = pizza_var.get()
    size = size_var.get()

    try:
        quantity = int(quantity_var.get())

        if quantity < 1 or quantity > 50:
            raise ValueError

    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a quantity between 1 and 50."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Order",
        "Are you sure you want to place this order?"
    )

    if not confirm:
        return

    pizza_price = pizza_prices[pizza]
    size_price = size_prices[size]

    selected_toppings = [
        topping
        for topping, variable in topping_vars.items()
        if variable.get()
    ]

    topping_price = sum(
        topping_prices[topping]
        for topping in selected_toppings
    )

    total_per_pizza = pizza_price + size_price + topping_price
    total = total_per_pizza * quantity

    receipt_text.delete("1.0", tk.END)

    receipt_text.insert(
        tk.END,
        "======== ORDER RECEIPT ========\n\n"
    )

    receipt_text.insert(tk.END, f"Pizza Flavor: {pizza} (₱{pizza_price})\n")
    receipt_text.insert(tk.END, f"Pizza Size: {size} (+₱{size_price})\n")

    if selected_toppings:
        for topping in selected_toppings:
            receipt_text.insert(
                tk.END,
                f"{topping}: ₱{topping_prices[topping]}\n"
            )
    else:
        receipt_text.insert(tk.END, "No extra toppings\n")

    receipt_text.insert(tk.END, "\n")
    receipt_text.insert(tk.END, f"Price per Pizza: ₱{total_per_pizza:,.2f}\n")
    receipt_text.insert(tk.END, f"Quantity: {quantity}\n")
    receipt_text.insert(tk.END, "-----------------------------------\n")
    receipt_text.insert(tk.END, f"TOTAL AMOUNT: ₱{total:,.2f}\n")
    receipt_text.insert(tk.END, "\nThank you come again!\n")


def reset_order():
    pizza_var.set("Pepperoni")
    size_var.set("Small")
    quantity_var.set(1)

    for variable in topping_vars.values():
        variable.set(False)

    receipt_text.delete("1.0", tk.END)


button_frame = tk.Frame(window, bg="#16241d")
button_frame.pack(pady=15)

calculate_button = tk.Button(
    button_frame,
    text="PLACE ORDER",
    font=("Arial", 9, "bold"),
    bg="#d96b38",
    fg="#f7f3e8",
    activebackground="#b85427",
    activeforeground="#f7f3e8",
    width=18,
    command=calculate_total
)
calculate_button.grid(row=0, column=0, padx=8)

reset_button = tk.Button(
    button_frame,
    text="RESET",
    font=("Arial", 9, "bold"),
    bg="#2e4a3d",
    fg="#f7f3e8",
    activebackground="#23382e",
    activeforeground="#f7f3e8",
    width=12,
    command=reset_order
)
reset_button.grid(row=0, column=1, padx=8)

tk.Label(
    window,
    text="ORDER SUMMARY",
    font=("Arial", 14, "bold"),
    bg="#16241d",
    fg="#f2a679"
).pack(pady=5)

receipt_text = tk.Text(
    window,
    height=14,
    width=65,
    font=("Consolas", 11),
    bg="#f7f3e8",
    fg="#1b1f1d",
    insertbackground="#1b1f1d"
)
receipt_text.pack(padx=25, pady=10)

window.mainloop()