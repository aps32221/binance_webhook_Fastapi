from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

from binance.futures import Futures
from binance.error import ClientError
from binance.lib.utils import config_logging
import config
import json
import logging

client = Futures()

config_logging(logging, logging.DEBUG)

logging.debug(client.time())
client = Futures(key=config.API_KEY, secret=config.SECRET_KEY)

AccInfo = None

param = {
"recvWindow": 15000
}
AccInfo = client.account(**param)

def showAccWalletBalance():
    print(f"Wallet balance : {str(AccInfo['totalWalletBalance'])}")
    for asset in AccInfo['assets']:
        if asset['asset']=='USDT':
            logging.info(f"USDT Balance : {asset['walletBalance']}")
            break
    # if AccInfo['totalWalletBalance']:
    #     print(f"wallet total balance : {AccInfo['totalWalletBalance']}")

# showAccWalletBalance()
app = FastAPI()

class Bar(BaseModel):
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float

class Strategy(BaseModel):
    position_size: float
    order_action: str
    order_contracts: float
    order_price: float
    order_id: str
    market_position: str
    market_position_size: float
    prev_market_position: str
    prev_market_position_size: float

class Payload(BaseModel):
    passphrase: str
    time: str
    exchange: str
    ticker: str
    bar: Bar
    strategy: Strategy



@app.get("/")
def root():
    return {"message": "home"}

@app.post("/webhook")
def webhook(payload: Payload):
    if payload.passphrase == config.PASSPHRASE:
        showAccWalletBalance()
        try:
            response = client.new_order(symbol="ETHUSDT", side=payload.strategy.order_action.upper(), type="MARKET", quantity=payload.strategy.order_contracts, recvWindow=60000, timestamp=client.time())#, quantity=payload.strategy.order_contracts)
            logging.info(response)
        except ClientError as error:
            logging.error(f"Found error. status: {error.status_code},\n"+
                    f"error code: {error.error_code}, \n"+
                    f"error message: {error.error_message}\n")
            return {"status": "failed", "msg": str(error)}
        return {"status": "successed", "payload": payload}
    else:
        return {"status": "failed"}