# Python wrapper for Delta.Exchange

**This module comes with absolutely no warranties. It is not complete or even very gracious with error handling, which you mostly need to do on your side. This code is primarly for exucational purposes.**

## Usage
`import delta`

## Functions

### get_balance(asset)

Use this to get the available balance of an asset.

**Arguments:**

`asset` (string): "ETH" | "BTC" | "USDT" | "USDC" | "DAI" | "XRP" | "DETO"

**Returns**

The *available balance* (i.e., not used in a trade or vested, etc) of the asset as a string.

### get_userid()

Use this to query the user ID.

**Arguments:**

none

**Returns**

The user's user ID as a string.

### get_products()
**Arguments:**

none

**Returns**

All the products on Delta Exchange is a JSON. It's a very long list with all the granular info, see `delta_products.txt` for reference.

### get_price_for_symbol(symbol)

Use this to get the price of a symbol, e.g., BTCUSDT.

**Arguments:**

`symbol` (string): "BTCUSDT", "BTCUSD", "ETHUSDT", etc. See `get_products()` for the whole list of symbols. Alternatively, you can check the URL on Delta, e.g., `https://www.delta.exchange/app/futures/trade/BTC/BTCUSDT` --> the symbol is `BTCUSDT`.

**Returns**

The *mark price* (i.e., not the last traded price) of the symbol as a string. This is a design choice, as trading might be low volume on some assets, the mark price is more useful.

### post_market_order(product_id, side, size, time_in_force, reduce_only)

Use this to post market orders.

**Arguments:**

`product_id` (int): The internal ID of the market. E.g., BTCUSDT is 139. See `get_products()` for all the IDs.

`side` (string): "buy" | "sell"

`size` (int): The size of the trade. **Pay attention** to the specifications, because Delta is using **contracts** for sizing. E.g., the BTCUSDT contract size is 0.001 BTC, the ETHUSDT contract size is 0.01 ETH, etc.

`time_in_force` (string): "gtc" (good till cancelled) | "fok" (fill or kill) | "ioc" (immediate or cancel)

`reduce_only` (string): "true" | "false"

**Returns**

Returns a JSON where the most important fields are:
- `'average_fill_price'`: string
- `'created_at'`: string,
- `'id'`: int,
- `'side'`: string,
- `'size'`: int
It returns some additional fields, too, see https://docs.delta.exchange/#place-order for details.

### get_position(product_id)

Use this to get the current position on a market.

**Arguments:**

`product_id` (int): The internal ID of the market. E.g., BTCUSDT is 139. See `get_products()` for all the IDs.

**Returns**

Returns a JSON with these fields:
- `'entry_price'`: string
- `'size'`: int,
- `'timestamp'`: epoch timestamp
The `size` can be negative, if the trade is short.

### market_close_position(product_id)

Use this to close all positions on a market.

**Arguments:**

`product_id` (int): The internal ID of the market. E.g., BTCUSDT is 139. See `get_products()` for all the IDs.

**Returns**

Returns a JSON where the most important fields are:
- `'average_fill_price'`: string
- `'created_at'`: string,
- `'id'`: int,
- `'side'`: string,
- `'size'`: int
It returns some additional fields, too, see https://docs.delta.exchange/#place-order for details.

### market_buy_btcusdt(size)

Use this to market buy BTCUSDT.

**Arguments:**

`size` (int): The size of the trade. **Pay attention** to the specifications, because Delta is using **contracts** for sizing. E.g., the BTCUSDT contract size is 0.001 BTC, the ETHUSDT contract size is 0.01 ETH, etc.

**Returns**

Returns a JSON where the most important fields are:
- `'average_fill_price'`: string
- `'created_at'`: string,
- `'id'`: int,
- `'side'`: string,
- `'size'`: int
It returns some additional fields, too, see https://docs.delta.exchange/#place-order for details.

### market_sell_btcusdt(size)

Use this to market sell BTCUSDT.

**Arguments:**

`size` (int): The size of the trade. **Pay attention** to the specifications, because Delta is using **contracts** for sizing. E.g., the BTCUSDT contract size is 0.001 BTC, the ETHUSDT contract size is 0.01 ETH, etc.

**Returns**

Returns a JSON where the most important fields are:
- `'average_fill_price'`: string
- `'created_at'`: string,
- `'id'`: int,
- `'side'`: string,
- `'size'`: int
It returns some additional fields, too, see https://docs.delta.exchange/#place-order for details.
