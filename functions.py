import ccxt
import time

huobipro = ccxt.huobipro()
gateio = ccxt.gateio()

PAIR = 'NEO/USDT'
INIT_BASE = 20000
POSITION = 0.25
MY_DEPTH = INIT_BASE / 4 * POSITION
BUYBACK_DEPTH = INIT_BASE / 4 * (1 - POSITION)
GATEIO_FEE = (5 / POSITION + 10) * POSITION
HUOBI_FEE = (5 / POSITION + 15) * POSITION

#######FUNCTIONS########

#FETCH ALL DATA
def fetch_all():
    global HUOBIPRO_ORDERBOOK
    global HUOBIPRO_TICKER
    global HUOBIPRO_BALANCE
    global GATEIO_ORDERBOOK
    global GATEIO_TICKER
    global GATEIO_BALANCE

    HUOBIPRO_ORDERBOOK = huobipro.fetch_order_book(PAIR)
    HUOBIPRO_TICKER = huobipro.fetch_ticker(PAIR)
    HUOBIPRO_BALANCE = huobipro.fetch_balance()
    GATEIO_ORDERBOOK = gateio.fetch_order_book(PAIR)
    GATEIO_TICKER = gateio.fetch_ticker(PAIR)
    GATEIO_BALANCE = gateio.fetch_balance()

    MY_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#EMERGENCY PROTOCOL CHECK
#ENTER PRICE TICKER, CHECK IF PERCENTAGE < 5, RETURN TRUE OR FALSE
def check_emergency():
    if HUOBIPRO_TICKER['percentage'] < 5 and GATEIO_TICKER['percentage'] < 5:
        return True
    else:
        return False

#BALANCE CHECK
#RETURN TRUE OR A DICT THAT INCLUDE THE CURRENCY THAT IS NOT ENOUGH AND THE MARKET
def check_balance():
    balance_status = {}
    if HUOBIPRO_BALANCE['NEO']['free'] / HUOBIPRO_BALANCE['NEO']['total'] <= position:
        balance_status['HUOBI']['NEO'] = False
    elif HUOBIPRO_BALANCE['USDT']['free'] / HUOBIPRO_BALANCE['USDT']['total'] <= position:
        balance_status['HUOBI']['USDT'] = False
    elif GATEIO_BALANCE['NEO']['free'] / HUOBIPRO_BALANCE['NEO']['total'] <= position:
        balance_status['GATEIO']['NEO'] = False
    elif elif GATEIO_BALANCE['USDT']['free'] / GATEIO_BALANCE['USDT']['total'] <= position:
        balance_status['GATEIO']['USDT'] = False
    else:
        balance_status['HUOBI']['NEO'] = True
        balance_status['HUOBI']['USDT'] = True
        balance_status['GATEIO']['NEO'] = True
        balance_status['GATEIO']['USDT'] = True
    return balance_status

#DEPTH CALCULATOR
def depth_cal(pricelist, depth):
    n = 0
    market_depth = pricelist[n][0] * pricelist[n][1]

    while market_depth < depth:
        n += 1
        market_depth = market_depth + pricelist[n][0] * pricelist[n][1]

    else:
        return pricelist[n][0]

#CALCULATE ALL DEPTH
def depth_cal_all():
    global HUOBI_ASK_PRICE_D
    global HUOBI_BID_PRICE_D
    global GATEIO_ASK_PRICE_D
    global GATEIO_BID_PRICE_D
    HUOBI_ASK_PRICE_D = depth_cal(HUOBIPRO_ORDERBOOK['asks'], MY_DEPTH * 0.2)
    HUOBI_BID_PRICE_D = depth_cal(HUOBIPRO_ORDERBOOK['bids'], MY_DEPTH * 0.2)
    GATEIO_ASK_PRICE_D = depth_cal(GATEIO_ORDERBOOK['asks'], MY_DEPTH * 0.2)
    GATEIO_BID_PRICE_D = depth_cal(GATEIO_ORDERBOOK['bids'], MY_DEPTH * 0.2)

#SPREAD PROFITABILITY CHECK
#ENTER BIDPRICE FROM MARKET A, ASKPRICE FROM MARKET B, DEPTH AND FEE, RETURN TRUE OR FALSE
def check_profit_spread():
    spread_check = {}
    if (HUOBI_BID_PRICE_D - GATEIO_ASK_PRICE_D) * MY_DEPTH > GATEIO_FEE:
        spread_check['HUOBI'] = False
        spread_check['GATEIO'] = True
        spread_check['HOLD'] = False
    elif (GATEIO_BID_PRICE_D - HUOBI_ASK_PRICE_D) * MY_DEPTH > HUOBI_FEE:
        spread_check['HUOBI'] = True
        spread_check['GATEIO'] = False
        spread_check['HOLD'] = False
    else:
        spread_check['HUOBI'] = False
        spread_check['GATEIO'] = False
        spread_check['HOLD'] = True
    return spread_check

#DEPTH CHECK
#def check_depth():
#    pass

#ORDER STATUS CHECK
#ENTER FETCHORDER, RETURN 'CLOSED', 'UNCLOSE', 'PARTIALLY CLOSED' OR 'CANNOT FIND THIS ORDER'

def check_order_status(market, order_id):
    order_status = {}
    order_status['market'] = market
    order_status['order_id'] = order_id

    if market = 'HUOBI':
        order = huobipro.fetch_order(order_id, PAIR)
    elif market = 'GATEIO':
        order = gateio.fetch_order(order_id, PAIR)

    if order['remaining'] = 0:
        order_status['status'] = 2 #ORDER CLOSED
    elif 0 < order['remaining'] / order['amount'] <= 0.2:
        order_status['status'] = 1 #ORDER PARTIALLY CLOSED
    elif 0 < order['remaining'] / order['amount'] > 0.2:
        order_status['status'] = 0 #ORDER UNCLOSE
    return order_status


#BUYBACK LOSS CHECK
#ENTER BALANCE STATUS, RETURN LOSS
def check_buyback_loss(status):
    if status['HUOBI']['NEO'] = False or status['GATEIO']['USDT'] = False:
        loss = (HUOBI_BID_PRICE_D - GATEIO_ASK_PRICE_D - 0.004) * BUYBACK_DEPTH
    elif status['HUOBI']['USDT'] = False or status['GATEIO']['NEO'] = False:
        loss = (GATEIO_BID_PRICE_D - HUOBI_ASK_PRICE_D - 0.004) * BUYBACK_DEPTH
    return loss

#ESTIMATED BALANCE CALCULATOR
def est_balance():
    pass

#STORE STARTING DATA(TICKER, BALANCE)
def store_starting_data():
    pass

#STORE FINISHING DATA(STATUS, STATUS_INFO, ESTIMATED BALANCE)
def store_finishing_data():
    pass


########PROTOCOLS########


#EMERGENCY PROTOCOL(WHEN NEO DROPS OVER 5%)
def emergency_prot():
    pass

#BUYBACK PROTOCOL
def buyback_prot():
    pass

#TRANSFER PROTOCOL
def transfer_prot():
    pass
