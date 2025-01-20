import json

class FixDecoder:
    """Decodifica mensagens FIX para JSON com base no arquivo fields-fix[xx].py"""

    def __init__(self, decoderFile, showDecodedMessages, formatDecodedMessages):
        self.fieldsMap = {}
        self._loadFields(decoderFile)
        self.showDecodedMessages = showDecodedMessages
        self.formatDecodedMessages = formatDecodedMessages
        return

    def _loadFields(self, filePath):
        # Caution with big files!
        try:
            with open(filePath, 'r') as f:
                fieldsData = json.load(f)
            self.fieldsMap = {field["number"]: field for field in fieldsData["fields"]["field"]}
            f.close()
        except Exception as e:
            raise RuntimeError(f"File load error | {filePath}: {e}")
        return

    def decodeMessage(self, message, onlyShow=False):
        if onlyShow == True:
            if self.showDecodedMessages == 'False':
                return
        
        pairs = message.split('|')
        decodedMessage = {}

        for pair in pairs:
            if not pair.strip():
                continue
            key, value = pair.split('=', 1)
            fieldInfo = self.fieldsMap.get(key)
            if fieldInfo:
                fieldName = fieldInfo["name"]
                if "value" in fieldInfo:
                    enum_description = next((enum["description"] for enum in fieldInfo["value"] if enum["enum"] == value), None)
                    decodedMessage[fieldName] = f"{enum_description}"
                else:
                    decodedMessage[fieldName] = f"{value}"
            else:
                decodedMessage[f"UnknownField({key})"] = value
        
        if self.showDecodedMessages == 'True':
            if self.formatDecodedMessages == 'True':
                print(json.dumps(decodedMessage, indent=4, sort_keys=True))
            else:
                print(decodedMessage)
        
        return decodedMessage

    def cleanup(self):
        self.fieldsMap = {}
        return

""" Exemplo de mensagem FIX decodificada para JSON:
{
    "Account": "00000",
    "AvgPx": "0",
    "BeginString": "FIX.4.4",
    "BodyLength": "301",
    "CheckSum": "227",
    "ClOrdID": "NELO.0000000000000000000",
    "CumQty": "0",
    "ExecID": "EXEC.0000000000000000000",
    "ExecType": "REPLACE",
    "LastPx": "0",
    "LastQty": "0",
    "LeavesQty": "1",
    "MaxFloor": "0",
    "MsgSeqNum": "592",
    "MsgType": "EXECUTION_REPORT",
    "OrdStatus": "None",
    "OrdType": "STOP_LIMIT",
    "OrderID": "0000000000000000000",
    "OrderQty": "1",
    "OrigClOrdID": "NELO.000000000000000000",
    "Price": "131365",
    "SecurityExchange": "70",
    "SenderCompID": "NELOGICA",
    "SendingTime": "20241101-11:55:15.900",
    "Side": "BUY",
    "StopPx": "131215",
    "Symbol": "WINZ24",
    "TargetCompID": "TRADEARENA",
    "TimeInForce": "DAY",
    "TransactTime": "20241101-08:55:15.900"
}
"""
