import hashlib
import hmac
import base64
import requests
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# Don"t forget to create a .env file with this content:
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

def get_time_stamp():
    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970,1,1)
    return str(int((d - epoch).total_seconds()))

# DELTA EXCHANGE CALLS START HERE

def get_balance(asset):
    url = "https://api.delta.exchange/v2/wallet/balances"
    payload = ""
    method = "GET"
    timestamp = get_time_stamp()
    path = "/v2/wallet/balances"
    query_string = ""
    signature_data = method + timestamp + path + query_string + payload
    signature = generate_signature(api_secret, signature_data)

    timestamp = get_time_stamp()

    headers = {
        "Accept": "application/json",
        "api-key": api_key,
        "signature": signature,
        "timestamp": timestamp
    }

    r = requests.get("https://api.delta.exchange/v2/wallet/balances", params={}, headers = headers)

    response = r.json()
    result = response["result"]
    # THIS IS NOT READY
    if asset == "USDT":
        return result[3]["available_balance"]
    # NEED TO FINISH FOR OTHER ASSETS. CURRENTLY ONLY RETURNS USDT.

def get_user_id():
    url = "https://api.delta.exchange/v2/wallet/balances"
    payload = ""
    method = "GET"
    timestamp = get_time_stamp()
    path = "/v2/wallet/balances"
    query_string = ""
    signature_data = method + timestamp + path + query_string + payload
    signature = generate_signature(api_secret, signature_data)

    timestamp = get_time_stamp()

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
    return output

def get_open_orders():
    url = "https://api.delta.exchange/v2/orders"
    payload = ""
    method = "GET"
    timestamp = get_time_stamp()
    path = "/v2/orders"
    query_string = "?product_id=139&state=open"
    signature_data = method + timestamp + path + query_string + payload
    signature = generate_signature(api_secret, signature_data)

    req_headers = {
        "api-key": api_key,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }
    
    # THIS CURRENTLY ONLY GETS OPEN ORDERS FOR THE BTCUSDT PERPS (PRODUCT ID 139)
    # NEEDS TO BE ADAPTED FOR ALL THE OTHER PAIRS, TOO
    r = requests.get("https://api.delta.exchange/v2/orders?product_id=139&state=open", params={}, headers = req_headers)

    result = r.json()
    return result

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