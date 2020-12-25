from coinbase.wallet.client import Client
from Coinbase.Keys import coinbase_API_key, coinbase_API_passphrase
from coinbase.wallet.error import AuthenticationError

client = Client(coinbase_API_key, coinbase_API_passphrase)

total = 0
message = []

try:
    accounts = client.get_accounts()
    for wallet in accounts.data:
        message.append(str(wallet['name']) + ' ' + str(wallet['native_balance']))
        value = str(wallet['native_balance']).replace('USD', '')
        total += float(value)
    message.append('Total Balance: ' + 'USD ' + str(total))
    print('\n'.join(message))
except AuthenticationError:
    print('Could not authenticate with your Coinbase API')

