#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
import quickfix as fix
import time
import logging
from datetime import datetime
from model.logger import setup_logger
from processor import Processor
__SOH__ = chr(1)

# Logger
setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')


class Application(fix.Application):
    """FIX Application"""

    ClOrdID = 0
    leave = False
    processor = Processor()

    def onCreate(self, sessionID):
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        print("Session (%s) logout !" % sessionID.toString())
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Admin) S >> %s" % msg)
        return
    
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(Admin) R << %s" % msg)
        return
    
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(App) S >> %s" % msg)
        return
    
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("(App) R << %s" % msg)
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        """Processing application message here"""
        self.processor.onMessage(message)
        pass

    def genClOrdID(self):
        """Generate ClOrdID"""
        self.ClOrdID += 1
        return str(self.ClOrdID).zfill(5)

    def put_new_order(self):
        """Request sample new order single"""
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle)) #39 = D 
        message.setField(fix.ClOrdID(self.genClOrdID())) #11 = Unique Sequence Number
        message.setField(fix.Side(fix.Side_BUY)) #43 = 1 BUY 
        message.setField(fix.Symbol("MSFT")) #55 = MSFT
        message.setField(fix.OrderQty(10000)) #38 = 1000
        message.setField(fix.Price(100))
        message.setField(fix.OrdType(fix.OrdType_LIMIT)) #40=2 Limit Order 
        message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION)) #21 = 3
        message.setField(fix.TimeInForce('0'))
        message.setField(fix.Text("NewOrderSingle"))
        trstime = fix.TransactTime()
        trstime.setString(datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)
        fix.Session.sendToTarget(message, self.sessionID)

    def run(self):
        """Run"""
        while self.leave is False:
            time.sleep(1)
        sys.exit(0)
