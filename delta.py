import hashlib
import hmac
import base64
import requests
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
# Testing
# import time
# from pprint import pprint

# Don't forget to create a .env file with this content:
#   api_key = "YOUR KEY FROM DELTA"
#   api_secret = "YOUR SECRET FROM DELTA"
# You can get these on delta.exchange
api_key = os.environ.get("api_key")
api_secret = os.environ.get("api_secret")

def generate_signature(secret, message):
    message = bytes(message, "utf-8")
    secret = bytes(secret, "utf-8")
    hash = hmac.new(secret, message, hashlib.sha256)
    return hash.hexdigest()

def internal_get_time_stamp():
    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970,1,1)
    return str(int((d - epoch).total_seconds()))

def generate_signature_data(url, path, payload, method, query_string):
    timestamp = internal_get_time_stamp()
    signature_data = method + timestamp + path + query_string + payload
    signature = generate_signature(api_secret, signature_data)
    return signature, timestamp

# DELTA EXCHANGE CALLS START HERE

def get_balance(asset):
    signature, timestamp = generate_signature_data("https://api.delta.exchange/v2/wallet/balances", "/v2/wallet/balances", "", "GET", "")
    headers = {
        "Accept": "application/json",
        "api-key": api_key,
        "signature": signature,
        "timestamp": internal_get_time_stamp()
    }

    r = requests.get("https://api.delta.exchange/v2/wallet/balances", params={}, headers = headers)
    response = r.json()
    result = response["result"]

    # This should be tweaked to enumerate the JSON as currently the positions are hardcoded, not ideal.
    # But unless Delta introduces a breaking change, it should work.
    if asset == "ETH":
        return result[0]["available_balance"]
    elif asset == "BTC":
        return result[1]["available_balance"]
    elif asset == "XRP":
        return result[2]["available_balance"]
    elif asset == "USDT":
        return result[3]["available_balance"]
    elif asset == "USDC":
        return result[4]["available_balance"]
    elif asset == "DAI":
        return result[5]["available_balance"]
    elif asset == "DETO":
        return result[6]["available_balance"]

def get_user_id():
    signature, timestamp = generate_signature_data("https://api.delta.exchange/v2/wallet/balances", "/v2/wallet/balances", "", "GET", "")
    headers = {
        "Accept": "application/json",
        "api-key": api_key,
        "signature": signature,
        "timestamp": timestamp
    }

    r = requests.get("https://api.delta.exchange/v2/wallet/balances", params={}, headers = headers)
    json_response = r.json()
    user_id = json_response["result"][0]["user_id"]

    return user_id

def get_products():
    headers = {
        "Accept": "application/json"
    }
    r = requests.get("https://api.delta.exchange/v2/products", params={}, headers = headers)

    output = r.json()
    # This returns a monster huge products JSON, see delta_products.txt
    return output

def get_open_orders(product_id):
    # Gets open orders by product ID.
    # You can find the product ID in the delta_products.txt or by calling get_products()
    # BTCUSDT is 139.
    # No open orders returns None
    signature, timestamp = generate_signature_data("https://api.delta.exchange/v2/orders", "/v2/orders", "", "GET", "?product_id="+ str(product_id) + "&state=open")
    headers = {
        "api-key": api_key,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }
    req_url = "https://api.delta.exchange/v2/orders?product_id=" + str(product_id) + "&state=open"
    r = requests.get(req_url, params={}, headers = headers)
    result = r.json()

    if result["meta"]["total_count"] > 0:
        return result
    else:
        return None

def get_price_for_symbol(symbol):
    headers = {
        "Accept": "application/json"
    }
    get_url = "https://api.delta.exchange/v2/tickers/" + symbol
    r = requests.get(get_url, params={}, headers = headers)

    response = r.json()
    # Returns the mark price (not the last traded price)
    mark_price = response["result"]["mark_price"]
    return mark_price

def convert_dollar_order_size_to_btc_contract_size(dollar_size):
    # Converts dollar order size to USDT-settled BTCUSDT Perps contract size
    btc_price = get_price_for_symbol("BTCUSDT")
    price_of_one_contract = float(btc_price) / 1000
    return int(dollar_size / price_of_one_contract) # Returns the integer as that's the max size

def post_market_order(product_id, side, size, time_in_force, reduce_only):
    params = {
        "product_id": int(product_id),
        "side": side,
        "size": size,
        "order_type": "market_order",
        "time_in_force": time_in_force,
        "reduce_only": reduce_only
    }
    query_string = f'?product_id={product_id}&side={side}&size={size}&order_type=market_order&time_in_force={time_in_force}&reduce_only={reduce_only}'
    signature, timestamp = generate_signature_data("https://api.delta.exchange/v2/orders", "/v2/orders", "", "POST", query_string)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'api-key': api_key,
        'signature': signature,
        'timestamp': timestamp
    }
    r = requests.post('https://api.delta.exchange/v2/orders', params=params, headers=headers)
    response = r.json()
    if response["success"]:
        return response["result"]
        # {'result': {'average_fill_price': string,
        #             'created_at': string,
        #             'id': int,
        #             'side': string,
        #             'size': int},
    else:
        return None

def get_position(product_id):
    params = {
        "product_id": int(product_id),
    }
    query_string = f'?product_id={product_id}'
    signature, timestamp = generate_signature_data("https://api.delta.exchange/v2/positions", "/v2/positions", "", "GET", query_string)
    headers = {
        'Accept': 'application/json',
        'api-key': api_key,
        'signature': signature,
        'timestamp': timestamp
    }
    r = requests.get('https://api.delta.exchange/v2/positions', params=params, headers = headers)
    response = r.json()
    if response["success"]:
        return response["result"]
        # {'entry_price': None, 'size': 0, 'timestamp': 1625319008999873} <-- a 0 position is a ["success"]["result"] too!
        # {'entry_price': '34581.50000000', 'size': 1, 'timestamp': 1625319163628629}
        # {'entry_price': '34573.50000000', 'size': -1, 'timestamp': 1625326952163651} <-- negative if it's a short
    else:
        return None

def market_buy_btcusdt(size):
    return post_market_order(139, "buy", size, "gtc", "false")

def market_sell_btcusdt(size):
    return post_market_order(139, "sell", size, "gtc", "false")

def market_close_position(product_id):
    current_position = get_position(product_id)
    current_size = current_position["size"]
    if current_size == 0:
        return None
    elif current_size > 0:
        return post_market_order(product_id, "sell", current_size, "gtc", "true")
    else:
        return post_market_order(product_id, "buy", (current_size * -1), "gtc", "true")


# Testing
# market_buy_btcusdt(1)
# pprint(get_position(139))
# time.sleep(5)
# pprint(market_close_position(139))