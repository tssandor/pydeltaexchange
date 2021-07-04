# Python wrapper for Delta.Exchange

## Usage
`import delta`

## Functions

### get_balance(asset)
**Arguments:**
`asset` (string): "ETH" | "BTC" | "USDT" | "USDC" | "DAI" | "XRP" | "DETO"

**Returns**
The *available balance* (i.e., not used in a trade or vested, etc) of the asset as a string.

### get_userid()
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
**Arguments:**
`symbol` (string): "BTCUSDT", "BTCUSD", "ETHUSDT", etc. See `get_products()` for the whole list of symbols. Alternatively, you can check the URL on Delta, e.g., `https://www.delta.exchange/app/futures/trade/BTC/BTCUSDT` --> the symbol is `BTCUSDT`.

**Returns**
The *mark price* (i.e., not the last traded price) of the symbol as a string. This is a design choice, as trading might be low volume on some assets, the mark price is more useful.

### post_market_order(product_id, side, size, time_in_force, reduce_only)
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
