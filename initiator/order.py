def mapBeginString(value):
    match value:
        case "FIX.1.1":
            return 0
        case "FIX.4.0":
            return 1
        case "FIX.4.1":
            return 2
        case "FIX.4.2":
            return 3
        case "FIX.4.3":
            return 4
        case "FIX.4.4":
            return 5
        case "FIX.5.0":
            return 6
        case "FIX.5.0":
            return 7
        case _:
            return -1

def mapExecType(value):
    match value:
        case "NEW":
            return 0
        case "DONE_FOR_DAY":
            return 1
        case "CANCELED":
            return 2
        case "REPLACE":
            return 3
        case "PENDING_CANCEL":
            return 4
        case "STOPPED":
            return 5
        case "REJECTED":
            return 6
        case "SUSPENDED":
            return 7
        case "PENDING_NEW":
            return 8
        case "CALCULATED":
            return 9
        case "EXPIRED":
            return 10
        case "RESTATED":
            return 11
        case "PENDING_REPLACE":
            return 12
        case "TRADE":
            return 13
        case "TRADE_CORRECT":
            return 14
        case "TRADE_CANCEL":
            return 15
        case "ORDER_STATUS":
            return 16
        case _:
            return -1

def mapOrdStatus(value):
    match value:
        case "NEW":
            return 0
        case "PARTIALLY_FILLED":
            return 1
        case "FILLED":
            return 2
        case "DONE_FOR_DAY":
            return 3
        case "CANCELED":
            return 4
        case "PENDING_CANCEL":
            return 5
        case "STOPPED":
            return 6
        case "REJECTED":
            return 7
        case "SUSPENDED":
            return 8
        case "PENDING_NEW":
            return 9
        case "CALCULATED":
            return 10
        case "EXPIRED":
            return 11
        case "ACCEPTED_FOR_BIDDING":
            return 12
        case "PENDING_REPLACE":
            return 13
        case _:
            return -1

def mapOrdType(value):
    match value:
        case "MARKET":
            return 0
        case "LIMIT":
            return 1
        case "STOP":
            return 2
        case "STOP_LIMIT":
            return 3
        case "WITH_OR_WITHOUT":
            return 4
        case "LIMIT_OR_BETTER":
            return 5
        case "LIMIT_WITH_OR_WITHOUT":
            return 6
        case "ON_BASIS":
            return 7
        case "PREVIOUSLY_QUOTED":
            return 8
        case "PREVIOUSLY_INDICATED":
            return 9
        case "FOREX":
            return 10
        case "FUNARI":
            return 11
        case "MARKET_IF_TOUCHED":
            return 12
        case "MARKET_WITH_LEFTOVER_AS_LIMIT":
            return 13
        case "PREVIOUS_FUND_VALUATION_POINT":
            return 14
        case "NEXT_FUND_VALUATION_POINT":
            return 15
        case "PEGGED":
            return 16
        case _:
            return -1

def mapSide(value):
    match value:
        case "BUY":
            return 0
        case "SELL":
            return 1
        case "BUY_MINUS":
            return 2
        case "SELL_PLUS":
            return 3
        case "SELL_SHORT":
            return 4
        case "SELL_SHORT_EXEMPT":
            return 5
        case "UNDISCLOSED":
            return 6
        case "CROSS":
            return 7
        case "CROSS_SHORT":
            return 8
        case "CROSS_SHORT_EXEMPT":
            return 9
        case "AS_DEFINED":
            return 10
        case "OPPOSITE":
            return 11
        case "SUBSCRIBE":
            return 12
        case "REDEEM":
            return 13
        case "LEND":
            return 14
        case "BORROW":
            return 15
        case _:
            return -1

def mapTimeInForce(value):
    match value:
        case "DAY":
            return 0
        case "GOOD_TILL_CANCEL":
            return 1
        case "AT_THE_OPENING":
            return 2
        case "IMMEDIATE_OR_CANCEL":
            return 3
        case "FILL_OR_KILL":
            return 4
        case "GOOD_TILL_CROSSING":
            return 5
        case "GOOD_TILL_DATE":
            return 6
        case "AT_THE_CLOSE":
            return 6
        case _:
            return -1

orderDataInsert = """
    INSERT INTO n_order_data (
        id,
        "createdAt",
        "updatedAt",
        status,
        account,
        "avgPx",
        "beginString",
        "bodyLength",
        "checkSum",
        "clOrdID",
        "cumQty",
        "execID",
        "execType",
        "lastPx",
        "lastQty",
        "leavesQty",
        "maxFloor",
        "msgSeqNum",
        "msgType",
        "ordStatus",
        "ordType",
        "orderID",
        "orderQty",
        "origClOrdID",
        price,
        "securityExchange",
        "senderCompID",
        "sendingTime",
        side,
        "stopPx",
        symbol,
        "targetCompID",
        "timeInForce",
        "transactTime",
        "rawMessage"
    ) VALUES (
        %(id)s,
        %(createdAt)s,
        %(updatedAt)s,
        %(status)s,
        %(account)s,
        %(avgPx)s,
        %(beginString)s,
        %(bodyLength)s,
        %(checkSum)s,
        %(clOrdID)s,
        %(cumQty)s,
        %(execID)s,
        %(execType)s,
        %(lastPx)s,
        %(lastQty)s,
        %(leavesQty)s,
        %(maxFloor)s,
        %(msgSeqNum)s,
        %(msgType)s,
        %(ordStatus)s,
        %(ordType)s,
        %(orderID)s,
        %(orderQty)s,
        %(origClOrdID)s,
        %(price)s,
        %(securityExchange)s,
        %(senderCompID)s,
        %(sendingTime)s,
        %(side)s,
        %(stopPx)s,
        %(symbol)s,
        %(targetCompID)s,
        %(timeInForce)s,
        %(transactTime)s,
        %(rawMessage)s
    );
"""
