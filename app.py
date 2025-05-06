import requests
import tkinter as tk
from tkinter import ttk

def main():

    #main window
    window = tk.Tk()
    window.title("Currency Calculater")
    window.geometry("300x200")
    window.resizable(False, False)

    # drop down options
    currencies = [
        "JPY", "CZK", "EUR", "USD"
    ]

    # dropdown menu
    currencies_menu_from = ttk.Combobox(window, values=currencies)
    currencies_menu_from.set("Select base currency:")
    currencies_menu_from.pack(pady=5)

    currencies_menu_to = ttk.Combobox(window, values=currencies)
    currencies_menu_to.set("Select final currency:")
    currencies_menu_to.pack(pady=5)

    # information entry
    amount_entry = tk.Entry(window, width=15)
    amount_entry.pack(pady=5)

    def update_output():
        currency_from = currencies_menu_from.get()
        currency_to = currencies_menu_to.get()
        amount = amount_entry.get()
        print(currency_from + currency_to + amount_entry.get())
        response = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={currency_from}&to={currency_to}")

        try:
            response.raise_for_status() == 200
            data = response.json()
            final_rates = float(data["rates"][currency_to])
            rate = f"1 {currency_from} = {final_rates/float(amount)} {currency_to}"
            rates_to_1_label.config(text=rate)
            final_rates_label.config(text=(f"{amount} {currency_from} = {str(final_rates)} {currency_to}"))
            print(data)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    # button to trigger update_output
    refresh_button = tk.Button(window, text="Calculate", command=update_output)
    refresh_button.pack(pady=5)

    # output data label
    rates_to_1_label = tk.Label(window, text="")
    rates_to_1_label.pack(pady=5)

    final_rates_label = tk.Label(window, text="")
    final_rates_label.pack(pady=5)


    window.mainloop()

if __name__ == "__main__":
    main()
