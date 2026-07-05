"""Standalone utility to generate a new Ethereum wallet (address + private key).

Run with: python manage.py shell -c "from API.wallet import generate_wallet; generate_wallet()"
or directly: python API/wallet.py

The generated private key is only ever printed to stdout — it is never
written to disk or logged. Store it securely (e.g. in your local .env file)
and never commit it to version control.
"""

from eth_account import Account


def generate_wallet():
    account = Account.create()
    private_key = account.key.hex()
    address = account.address
    print(f"Address: {address}")
    print(f"Private key: {private_key}")
    return address, private_key


if __name__ == '__main__':
    generate_wallet()
