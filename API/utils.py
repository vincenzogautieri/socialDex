from django.conf import settings
from web3 import Web3


def send_transaction(message: str) -> str:
    """Writes `message` on-chain as the data payload of a zero-value
    transaction sent to the null address, and returns the transaction hash.

    Credentials and the RPC endpoint are read from Django settings, which in
    turn load them from environment variables (see .env.example). Never
    hardcode a private key or an RPC URL with an embedded project ID here.
    """
    if not settings.INFURA_URL or not settings.ETH_ADDRESS or not settings.ETH_PRIVATE_KEY:
        raise RuntimeError(
            "Blockchain credentials are not configured. Set INFURA_URL, "
            "ETH_ADDRESS and ETH_PRIVATE_KEY in your .env file."
        )

    w3 = Web3(Web3.HTTPProvider(settings.INFURA_URL))

    nonce = w3.eth.get_transaction_count(settings.ETH_ADDRESS)
    gas_price = w3.eth.gas_price

    signed_tx = w3.eth.account.sign_transaction(
        dict(
            nonce=nonce,
            gasPrice=gas_price,
            gas=100000,
            to='0x0000000000000000000000000000000000000000',
            value=w3.to_wei(0, 'ether'),
            data=message.encode('utf-8'),
            chainId=w3.eth.chain_id,
        ),
        settings.ETH_PRIVATE_KEY,
    )

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return w3.to_hex(tx_hash)
