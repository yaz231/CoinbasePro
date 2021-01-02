import websocket, json
import dateutil.parser
import cbpro
from CoinbasePro.Keys import sandbox_b64secret, sandbox_key as key, sandbox_secret as passphrase

minutes_processed = {}
minute_candlesticks = []
current_tick = None
previous_tick = None

in_position = False
test_fund = 100.0

BTC_id = 'ecd6a272-670b-4453-aa19-2e9617ac2087'
USD_id = '93a22eef-7d25-43de-8f3c-cce834bd6c06'


def get_balance(id):
    return auth_client.get_account(id)['balance']


def three_soldiers_check():
    last_candle = minute_candlesticks[-2]
    previous_candle = minute_candlesticks[-3]
    first_candle = minute_candlesticks[-4]

    print("== Let's compare the last 3 candle closes ==")
    if last_candle['close'] > previous_candle['close'] and previous_candle['close'] > first_candle['close']:
        print("=== Three green candlesticks in a row, let's make a trade! ===")
        distance = last_candle['close'] - first_candle['open']
        print("Distance is {}".format(distance))
        profit_price = last_candle['close'] + (distance * 2)
        print("I will take profit at {}".format(profit_price))
        loss_price = first_candle['open']
        print("I will sell for a loss at {}".format(loss_price))
        return True, profit_price, loss_price
    return False


def on_open(ws):
    print("Opened connection")

    subscribe_message = {
        "type": "subscribe",
        "channels": [
            {
                "name": "ticker",
                "product_ids": [
                    "BTC-USD"
                ]
            }
        ]
    }
    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    global current_tick, previous_tick, in_position
    profit_price = 0
    loss_price = 0
    previous_tick = current_tick
    current_tick = json.loads(message)
    # print(message)
    # print(current_tick)

    # print("=== Received Tick ===")
    # print("{} @ {}".format(current_tick['time'], current_tick['price']))

    tick_datetime_object = dateutil.parser.parse(current_tick['time'])
    tick_dt = tick_datetime_object.strftime("%m/%d/%Y %H:%M")
    # print(tick_datetime_object.minute)
    # print(tick_dt)

    if not tick_dt in minutes_processed:
        # print("Starting new candlestick")
        minutes_processed[tick_dt] = True
        # print(minutes_processed)

        if len(minute_candlesticks) > 0:
            minute_candlesticks[-1]['close'] = previous_tick['price']
            if minute_candlesticks[-1]['open'] > minute_candlesticks[-1]['close']:
                minute_candlesticks[-1]['NET'] = 'Loss'
            elif minute_candlesticks[-1]['open'] < minute_candlesticks[-1]['close']:
                minute_candlesticks[-1]['NET'] = 'Profit'
            else:
                minute_candlesticks[-1]['NET'] = 'Same'

        minute_candlesticks.append({
            "minute": tick_dt,
            "open": current_tick['price'],
            "high": current_tick['price'],
            "low": current_tick['price']
        })

    if len(minute_candlesticks) > 0:
        current_candlestick = minute_candlesticks[-1]
        if current_tick['price'] > current_candlestick['high']:
            current_candlestick['high'] = current_tick['price']
        if current_tick['price'] < current_candlestick['low']:
            current_candlestick['low'] = current_tick['price']

        print("=== CandleSticks ===")
        for candlestick in minute_candlesticks:
            print(candlestick)

        if len(minute_candlesticks) > 4:
            print("== There are too many candlesticks ==")
            print("== Removing a candlesticks ==")
            minute_candlesticks.pop(0)

        if len(minute_candlesticks) > 3:
            print("== There are more than 3 candlesticks, checking for pattern ==")
            last_candle = minute_candlesticks[-2]
            previous_candle = minute_candlesticks[-3]
            first_candle = minute_candlesticks[-4]
            # print(type(last_candle['close']))

            print("== Let's compare the last 3 candle closes ==")
            if float(last_candle['close']) > float(previous_candle['close']) and float(previous_candle['close']) > float(first_candle['close']):
                print("=== Three green candlesticks in a row, let's make a trade! ===")

                distance = float(last_candle['close']) - float(first_candle['open'])
                if distance >= 0:
                    print("Distance is {}".format(distance))
                    profit_price = float(last_candle['close']) + (distance * 2)
                    print("I will take profit at {}".format(profit_price))
                    loss_price = float(first_candle['open'])
                    print("I will sell for a loss at {}".format(loss_price))

                if not in_position:
                    print("== Placing order and setting in position to true")
                    in_position = True
                    # place_order(profit_price, loss_price)
                    print("=== PLACED ORDER ===")
                    auth_client.place_market_order(product_id='BTC-USD', side='buy', funds='100.0')
                    auth_client.place_limit_order(product_id='BTC-USD', side='sell', price=profit_price, size=get_balance(BTC_id))
                    auth_client.place_limit_order(product_id='BTC-USD', side='sell', price=loss_price, size=get_balance(BTC_id))

                if in_position:
                    exit()




# socket = "wss://ws-feed.pro.coinbase.com"
socket = 'wss://ws-feed-public.sandbox.pro.coinbase.com'

###Authenticated Client###
auth_client = cbpro.AuthenticatedClient(key, sandbox_b64secret, passphrase,
                                        api_url="https://api-public.sandbox.pro.coinbase.com")
# print(auth_client.get_account(BTC_id))
# print("The amount of USD: {}".format(get_balance(USD_id)))
# print("The amount of BTC: {}".format(get_balance(BTC_id)))
# auth_client.buy(product_id='BTC-USD', order_type='market', funds='100.0')
# auth_client.sell(product_id='BTC-USD', order_type='stop', funds='100.0')
# print("The amount of USD: {}".format(get_balance(USD_id)))
# print("The amount of BTC: {}".format(get_balance(BTC_id)))

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()
# wsClient = cbpro.WebsocketClient(url=socket,
#                                 products=["BTC-USD"],
#                                 channels=["ticker"])
# wsClient.start()


# print(auth_client.get_accounts())
# print(get_balance(USD_id))
