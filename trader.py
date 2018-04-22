import ccxt
import time
#from pymongo import MongoClient

#CONSTANTS
huobipro = ccxt.huobipro()
gateio = ccxt.gateio()
pair = 'NEO/USDT'
init_base = 20000
position = 0.25
my_depth = init_base / 4 * position
gateio_fee = (5 / position + 10) * position
huobi_fee = (5 / position + 15) * position

#DEPTH CALCULATOR, ENTER PRICELIST AND DEPTH, RETURN BEST PRICE
def DepthCal(pricelist, depth):
    n = 0
    market_depth = pricelist[n][0] * pricelist[n][1]
    while market_depth < depth:
        n += 1
        market_depth = market_depth + pricelist[n][0] * pricelist[n][1]
    else:
        return pricelist[n][0]

#FREE BALANCE CHECK, ENTER BALANCE LIST, TOKEN SYMBOL AND BALANCE THAT REQUIRED, RETURN TRUE OR FALSE
def CheckFreeBalance(balancelist, token, balancereq):
    if balancelist[token]['free'] > balancereq:
        return True
    else:
        return False

#SPREAD PROFITABILITY CHECK, ENTER BIDPRICE FROM MARKET A, ASKPRICE FROM MARKET B, DEPTH AND FEE, RETURN TRUE OR FALSE
def CheckProfitSpread(bidprice, askprice, depth, fee):
    if (bidprice - askprice) * depth > fee:
        return True
    else:
        return False

#TRADING LOOP
while True:

    #FETCH DATA
    my_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    huobi_orderbook = huobipro.fetch_order_book(pair)
    gateio_orderbook = gateio.fetch_order_book(pair)
    huobi_balance = huobipro.fetch_balance()
    gateio_balance = gateio.fetch_balance()

    #STORE DATA(TBA)

    #GET BEST PRICE WITH DEPTH CONSIDERED
    huobi_ask_price_d = DepthCal(huobi_orderbook['asks'], my_depth)
    huobi_bid_price_d = DepthCal(huobi_orderbook['bids'], my_depth)
    gateio_ask_price_d = DepthCal(gateio_orderbook['asks'], my_depth)
    gateio_bid_price_d = DepthCal(gateio_orderbook['bids'], my_depth)

    #CHECK SPREAD
    if CheckProfitSpread(huobi_bid_price_d, gateio_ask_price_d, my_depth, gateio_fee) and CheckFreeBalance(gateio_balance, 'USDT', my_depth * 1.002) and CheckFreeBalance(huobi_balance, 'NEO', my_depth * 1.002):
        pass

    elif CheckProfitSpread(gateio_bid_price_d, huobi_ask_price_d, my_depth, huobi_fee) and CheckFreeBalance(huobi_balance, 'USDT', my_depth * 1.002) and CheckFreeBalance(gateio_balance, 'NEO', my_depth * 1.002):
        pass

    else:
        pass

    #CHECK ORDER SITUATION(TBA)

    #CHECK TRANSFER SITUATION(TBA)

    #PRINT LOG(TBA)

#EMERGENCY BREAK(TBA)
