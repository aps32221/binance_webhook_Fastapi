# binance_webhook_Fastapi
The API that receive TradingView webhook and make new future order by Binance Futures API

How to?
---
1. change API_KEY, SECRET_KEY, PASSPHRASE to your Binance account's API_KEY, SECRET_KEY in config.py
2. deploy to any cloud platform. e.g. Heroku
3. go TradingView, create alert, then select webhook and paste YOURSERVER/webhook to the field
4. change message to 
  ```
{
  "passphrase": "dbA5KD6PpmINEqKOFx3vJDAQy1YIHWR",
  "time": "{{timenow}}",
  "exchange": "{{exchange}}",
  "ticker": "{{ticker}}",
  "bar": {
      "time": "{{time}}",
      "open": {{open}},
      "high": {{high}},
      "low": {{low}},
      "close": {{close}},
      "volume": {{volume}}
  },
  "strategy": {
      "position_size": {{strategy.position_size}},
      "order_action": "{{strategy.order.action}}",
      "order_contracts": {{strategy.order.contracts}},
      "order_price": {{strategy.order.price}},
      "order_id": "{{strategy.order.id}}",
      "market_position": "{{strategy.market_position}}",
      "market_position_size": {{strategy.market_position_size}},
      "prev_market_position": "{{strategy.prev_market_position}}",
      "prev_market_position_size": {{strategy.prev_market_position_size}}
  }
}
```
then click create, done~
