import requests
import tkinter as tk
from tkinter import ttk

def main():

    def get_history():
        global to_history
        global history_pointer
        try:
            currencies_menu_from.set(history[history_pointer][0])
            currencies_menu_to.set(history[history_pointer][1])
            amount_entry.delete(0, tk.END)
            amount_entry.insert(0, history[history_pointer][2])
            to_history = False
            history_pointer = history_pointer - 1
            update_output()
        except IndexError as e:
            rates_to_1_label.config(text="No previous values!")
            final_rates_label.config(text="")



    def switch_currencies():
        try:
            handy = currencies_menu_to.get()
            currencies_menu_to.set(currencies_menu_from.get())
            currencies_menu_from.set(handy)
            update_output()
        except ValueError:
            rates_to_1_label.config("No values!")

    def update_output():
        currency_from = currencies_menu_from.get().strip().upper()
        currency_to = currencies_menu_to.get().strip().upper()

        # try if amount value is a number
        try:
            amount = float(amount_entry.get())
        except ValueError:
            rates_to_1_label.config(text="Invalid entry!")
            return

        # send request to API and update labels
        try:
            response = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={currency_from}&to={currency_to}")
            data = response.json()  # check if website status is valid - 200
            final_rates = float(data["rates"][currency_to])
            rate = f"1 {currency_from} = {final_rates / float(amount)} {currency_to}"
            rates_to_1_label.config(text=rate)
            final_rates_label.config(text=(f"{amount} {currency_from} = {str(final_rates)} {currency_to}"))
            write_to_history(currency_from, currency_to, amount)
            print(data)
            print(history)
        except requests.exceptions.RequestException as e:
            rates_to_1_label.config(text="Invalid input!")

    def write_to_history(from_cur, to_cur, amount):
        global to_history
        global history_pointer
        if to_history:
            history.append([from_cur, to_cur, amount])
            history_pointer = -2
        else:
            to_history = True

    #main window
    window = tk.Tk()
    window.title("Currency Calculater")
    window.geometry("300x200")
    window.resizable(False, False)

    # create frames
    main_input_frame = tk.Frame(window)
    main_input_frame.pack(pady=5)

    input_frame = tk.Frame(main_input_frame)
    input_frame.grid(row=0, column=0)

    amount_frame = tk.Frame(window)
    amount_frame.pack()

    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=3)

    # drop down options
    currencies = [
        "JPY", "CZK", "EUR", "USD"
    ]

    # dropdown menus
    tk.Label(input_frame, text="From:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    currencies_menu_from = (ttk.Combobox(input_frame, values=currencies, width=7))
    currencies_menu_from.grid(row=0, column=1, padx=5, pady=5, sticky="e")
    currencies_menu_from.set("JPY")

    tk.Label(input_frame, text="To:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    currencies_menu_to = (ttk.Combobox(input_frame, values=currencies, width=7))
    currencies_menu_to.grid(row=1, column=1, padx=5, pady=5, sticky="e")
    currencies_menu_to.set("EUR")

    # amount entry
    tk.Label(amount_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    amount_entry = tk.Entry(amount_frame, width=15)
    amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    # button to switch currencies
    switch_button = tk.Button(main_input_frame, text="⇄", command=switch_currencies)
    switch_button.grid(row=0, column=1, rowspan=1, padx=5, pady=5, sticky="ns")

    # button to get values from history
    history_button = tk.Button(buttons_frame, text="Previous", command=get_history)
    history_button.grid(row=0, column=0, padx=5)

    # button to trigger update_output
    calculate = tk.Button(buttons_frame, text="Calculate", command=update_output)
    calculate.grid(row=0, column=1, padx=5)

    # output data label
    rates_to_1_label = tk.Label(window, text="")
    rates_to_1_label.pack(pady=3)

    final_rates_label = tk.Label(window, text="")
    final_rates_label.pack(pady=3)

    # pointer which points at previous in history
    global history_pointer
    history_pointer = int(-2)
    global to_history
    to_history = True

    # history
    history = []



    window.mainloop()

if __name__ == "__main__":
    main()
