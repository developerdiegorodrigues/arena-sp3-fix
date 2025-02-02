def mapBeginString(value):
    match value:
        case "FIX.4.0":
            return 0
        case "FIX.4.1":
            return 1
        case "FIX.4.2":
            return 2
        case "FIX.4.3":
            return 3
        case "FIX.4.4":
            return 4
        case "FIX.5.0":
            return 5
        case _:
            return -1

def mapExecType(value, msg):
    match value:
        case "NEW":
            return 0 # 
        case "PARTIAL_FILL":
            return 1 # !
        case "FILL":
            return 2 # !
        case "DONE_FOR_DAY":
            return 3 # 
        case "CANCELED":
            return 4 # 
        case "REPLACE":
            return 5 # 
        case "PENDING_CANCEL":
            return 6 # 
        case "STOPPED":
            return 7 # 
        case "REJECTED":
            return 8 # 
        case "SUSPENDED":
            return 9 # 
        case "PENDING_NEW":
            return 10 # A
        case "CALCULATED":
            return 11 # B
        case "EXPIRED":
            return 12 # C
        case "RESTATED":
            return 13 # D
        case "PENDING_REPLACE":
            return 14 # E
        case "TRADE":
            return 15 # F
        case "TRADE_CORRECT":
            return 16 # G
        case "TRADE_CANCEL":
            return 17 # H
        case "ORDER_STATUS":
            return 18 # I
        case _:
            return getASCII(msg, 150) + 500

def mapOrdStatus(value, msg):
    match value:
        case "NEW":
            return 0 # 
        case "PARTIALLY_FILLED":
            return 1 # 
        case "FILLED":
            return 2 # 
        case "DONE_FOR_DAY":
            return 3 # 
        case "CANCELED":
            return 4 # 
        case "REPLACED":
            return 5 # !
        case "PENDING_CANCEL":
            return 6 # 
        case "STOPPED":
            return 7 # 
        case "REJECTED":
            return 8 # 
        case "SUSPENDED":
            return 9 # 
        case "PENDING_NEW":
            return 10 # A
        case "CALCULATED":
            return 11 # B
        case "EXPIRED":
            return 12 # C
        case "ACCEPTED_FOR_BIDDING":
            return 13 # D
        case "PENDING_REPLACE":
            return 14 # E
        case _:
            return getASCII(msg, 39) + 500

def mapOrdType(value, msg):
    match value:
        case "MARKET":
            return 0 # 1
        case "LIMIT":
            return 1 # 2
        case "STOP":
            return 2 # 3
        case "STOP_LIMIT":
            return 3 # 4
        case "MARKET_ON_CLOSE":
            return 4 # 5 !
        case "WITH_OR_WITHOUT":
            return 5 # 6
        case "LIMIT_OR_BETTER":
            return 6 # 7
        case "LIMIT_WITH_OR_WITHOUT":
            return 7 # 8
        case "ON_BASIS":
            return 8 # 9
        case "ON_CLOSE":
            return 9 # A !
        case "LIMIT_ON_CLOSE":
            return 10 # B !
        case "FOREX_C":
            return 11 # C !
        case "PREVIOUSLY_QUOTED":
            return 12 # D
        case "PREVIOUSLY_INDICATED":
            return 13 # E
        case "FOREX_F":
            return 14 # F
        case "FOREX":
            return 15 # !G
        case "FOREX_H":
            return 16 # H
        case "FUNARI":
            return 17 # I
        case "MARKET_IF_TOUCHED":
            return 18 # J
        case "MARKET_WITH_LEFTOVER_AS_LIMIT":
            return 19 # K
        case "PREVIOUS_FUND_VALUATION_POINT":
            return 20 # L
        case "NEXT_FUND_VALUATION_POINT":
            return 21 # M
        case "PEGGED":
            return 24 # P
        case _:
            return getASCII(msg, 40) + 500

def mapSide(value, msg):
    match value:
        case "BUY":
            return 0 # 1
        case "SELL":
            return 1 # 2
        case "BUY_MINUS":
            return 2 # 3
        case "SELL_PLUS":
            return 3 # 4
        case "SELL_SHORT":
            return 4 # 5
        case "SELL_SHORT_EXEMPT":
            return 5 # 6
        case "UNDISCLOSED":
            return 6 # 7
        case "CROSS":
            return 7 # 8
        case "CROSS_SHORT":
            return 8 # 9
        case "CROSS_SHORT_EXEMPT":
            return 9 # A
        case "AS_DEFINED":
            return 10 # B
        case "OPPOSITE":
            return 11 # C
        case "SUBSCRIBE":
            return 12 # D
        case "REDEEM":
            return 13 # E
        case "LEND":
            return 14 # F
        case "BORROW":
            return 15 # G
        case _:
            return getASCII(msg, 54) + 500

def mapTimeInForce(value, msg):
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
            return 7
        case _:
            return getASCII(msg, 59) + 500

def getASCII(msg, field):
    _list = msg.split("|")
    for _pair in _list:
        if not _pair.strip():
            continue
        _apart = _pair.split('=')
        if f"{_apart[0]}" == f"{field}":
            return ord(f"{_apart[1]}")
    return 500

orderDataInsert = """
    INSERT INTO n_order (
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
