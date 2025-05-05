import requests

from_currency = input("Input base currency: ")
from_currency = from_currency.upper()
amount = input("Input amount:")
to_currency = input("Input final currency: ")
to_currency = to_currency.upper()

print(from_currency + to_currency)


response = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}")

try:
    response.raise_for_status() == 200
    data = response.json()
    print(data)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
