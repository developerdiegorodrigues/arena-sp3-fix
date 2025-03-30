import requests
import traceback
from datetime import datetime
__SOH__ = chr(1)

ORDER_RECEIVER_URL = 'http://localhost:8083/order/create'

class Processor():
    def onMessage(self, message):
        msgDict = self.messageToDict(message)
        if (msgDict['35']=='8'):
            self.execReport(msgDict) 
        return 
     
    def messageToDict(message):
        messageDict = {}
        messageList = message.toString().split(__SOH__)
        for message in messageList:
            if message == '':
                continue
            msgPair = message.split('=')
            messageDict[msgPair[0]]=msgPair[1]
        return messageDict

    def execReport(self, msgDict):
        if(self.isZeroPx(msgDict)):
            return
        self.sendArena(msgDict)
        return

    def isZeroPx(msgDict):
        if msgDict['39']=='0' and msgDict['6']=='0': # OrdStatus: NEW, AvgPx: 0
            return True
        if msgDict['39']=='4': # OrdStatus: CANCELED
            return True
        if msgDict['39']=='8': # OrdStatus: REJECTED
            return True
        if msgDict['39']=='C': # OrdStatus: EXPIRED
            return True
        if msgDict['32']=='0': # LastQty: 0
            return True
        return False

    def sendArena(msgDict):
        newDateTime = msgDict['60'][:4] + '/' + msgDict['60'][4:6] + '/' + msgDict['60'][6:8] + ' '  + msgDict['60'][9:] + "000"
        myJson = {
            "side": f"{int(msgDict['54']) - 1}",    # Side
            "quantity": f"{msgDict['32']}",         # LastQty
            "token": f"{msgDict['1']}",             # Account
            "code": f"{msgDict['55']}",             # Symbol
            "price": f"{msgDict['31']}",            # LastPx
            "tradeId": f"{msgDict['17']}",          # ExecID
            "groupOrderId": f"{msgDict['11']}",     # ClOrdID
            "dateTime": f"{newDateTime}"            # TransactTime
        }
        try:
            requests.post(ORDER_RECEIVER_URL, json=myJson, timeout=10)
        except:
            print("Erro ao encaminhar dados para o Java")
            print(traceback.format_exc())
            print(myJson)
            pass
        return
