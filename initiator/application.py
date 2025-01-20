# https://quickfixengine.org/c/documentation/

#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
import quickfix
import time
import logging
from model.logger import setup_logger

from processor import Processor

__SOH__ = chr(1)

# Logger
setup_logger('logfix', 'Logs/message.log')
logfix = logging.getLogger('logfix')

class Application(quickfix.Application):
    """FIX Application"""
    
    ClOrdID = 0
    sessionID = None
    leave = False
    processor = Processor()

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        print("onCreate : Session (%s)" % sessionID.toString())
        return

    def onLogon(self, sessionID):
        self.sessionID = sessionID
        print("Successful Logon to session '%s'." % sessionID.toString())
        return

    def onLogout(self, sessionID):
        print("Session (%s) logout !" % sessionID.toString())
        self.processor.logout()
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info = ("(Admin) S >> %s" % msg)
        self.processor.decoder.decodeMessage(msg, True)
        return
    
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info = ("(Admin) R << %s" % msg)
        self.processor.decoder.decodeMessage(msg, True)
        return
    
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info = ("(App) S >> %s" % msg)
        self.processor.decoder.decodeMessage(msg, True)
        return
    
    def fromApp(self, message, sessionID):
        msg = f"{message}".replace(__SOH__, "|")
        logfix.info = ("(App) R << %s" % msg)
        self.onMessage(msg, sessionID)
        return

    def onMessage(self, msg, sessionID):
        """Processing application message here"""
        self.processor.onMessage(msg)
        pass

    def genClOrdID(self):
        """Generate ClOrdID"""
        self.ClOrdID += 1
        return str(self.ClOrdID).zfill(5)

    def run(self):
        """Run"""
        print("Service started")
        self.processor.simulator.run(self.sessionID, self.fromApp)
        while self.leave is False:
            time.sleep(1)
        self.processor.cleanup()
        sys.exit(0)

'''
    def put_new_order_example(self):
        """Request sample new order single example"""
        message = quickfix.Message()
        header = message.getHeader()
        header.setField(quickfix.MsgType(quickfix.MsgType_NewOrderSingle))
        message.setField(quickfix.ClOrdID(self.genClOrdID()))
        message.setField(quickfix.Side(quickfix.Side_BUY))
        message.setField(quickfix.Symbol("MSFT"))
        message.setField(quickfix.OrderQty(10000))
        message.setField(quickfix.Price(100))
        message.setField(quickfix.OrdType(quickfix.OrdType_LIMIT))
        message.setField(quickfix.HandlInst(quickfix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
        message.setField(quickfix.TimeInForce('0'))
        message.setField(quickfix.Text("NewOrderSingle"))
        trstime = quickfix.TransactTime()
        trstime.setString(datetime.now().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)
        print(f"Sending New Order Single {message.toString()}")
        quickfix.Session.sendToTarget(message, self.sessionID)
'''
