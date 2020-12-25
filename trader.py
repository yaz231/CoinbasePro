import cbpro
from Coinbase.Keys import pro_coinbase_API_passphrase as passphrase, b64secret as secret, pro_coinbase_key as key
public_client = cbpro.PublicClient()
# print(public_client.get_products())

# Get the order book at the default level.
# print(public_client.get_product_order_book('BTC-USD'))
# Get the order book at a specific level.
# print(public_client.get_product_order_book('BTC-USD', level=1))

# Get the product ticker for a specific product.
# print(public_client.get_product_ticker(product_id='BTC-USD'))

# Get the product trades for a specific product.
# Returns a generator
# print(public_client.get_product_trades(product_id='BTC-USD'))\

# print(public_client.get_product_historic_rates('BTC-USD'))
# To include other parameters, see function docstring:
# print(public_client.get_product_historic_rates('BTC-USD', granularity=3600))

# print(public_client.get_product_24hr_stats('BTC-USD'))

auth_client = cbpro.AuthenticatedClient(key, secret, passphrase)
print(auth_client.get_accounts())