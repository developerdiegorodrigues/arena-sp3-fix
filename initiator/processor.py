import traceback
from datetime import datetime
import psycopg2
import uuid
import logging
from model.logger import setup_logger
from dotenv import load_dotenv
import os

from webhook import Webhook
from decoder import FixDecoder
from simulator import FixSimulator
from order import *

load_dotenv()
WEBHOOK_URL             = os.getenv("WEBHOOK_URL")
WEBHOOK_ACTIVE          = os.getenv("WEBHOOK_ACTIVE")
DECODER_FILE            = os.getenv("DECODER_FILE")
SHOW_DECODED_MESSAGES   = os.getenv("SHOW_DECODED_MESSAGES")
FORMAT_DECODED_MESSAGES = os.getenv("FORMAT_DECODED_MESSAGES")
SIMULATOR_FILE          = os.getenv("SIMULATOR_FILE")
EXECUTE_SIMULATOR       = os.getenv("EXECUTE_SIMULATOR")
SIMULATOR_TIMER        = os.getenv("SIMULATOR_TIMER")
BASE_DOMAIN             = os.getenv("BASE_DOMAIN")
DB_PORT                 = os.getenv("DB_PORT")
DB_NAME                 = os.getenv("DB_NAME")
DB_USERNAME             = os.getenv("DB_USERNAME")
DB_PASSWORD             = os.getenv("DB_PASSWORD")

class Processor():
    def __init__(self):
        self.webhook = Webhook(WEBHOOK_URL, WEBHOOK_ACTIVE)
        self.decoder = FixDecoder(DECODER_FILE, SHOW_DECODED_MESSAGES, FORMAT_DECODED_MESSAGES)
        self.simulator = FixSimulator(EXECUTE_SIMULATOR, SIMULATOR_FILE, SIMULATOR_TIMER, self.decoder.decodeMessage)
        
        setup_logger("logprocessor", "./log-processor.log")
        self.logProcessor = logging.getLogger("logprocessor")
        self.logProcessor.info("Processor logging started")

        try:
            self.connection = psycopg2.connect(host=BASE_DOMAIN, port=DB_PORT, database=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD)
            self.cursor = self.connection.cursor()
        except Exception as e:
            msg = f"Unable to connect to database: {e}"
            self.logProcessor.info(msg)
            self.webhook.send("Equinix SP3 | Fix (initiator) | Processor.init() -> exception")
            raise RuntimeError(msg)
        return
    
    def logout(self):
        _info = "Equinix SP3 | Fix (initiator) | Logout"
        self.webhook.send(_info)
        return

    def onMessage(self, msg):
        dec = self.decoder.decodeMessage(msg, False)
        if (EXECUTE_SIMULATOR == "True" and dec["SenderCompID"] != "NELOGICA"):
            print(f"Evicted: {dec['SenderCompID']}")
            return
        if (dec["MsgType"] == "EXECUTION_REPORT"):
            self._toDataBase(dec, msg)
            return
        self.logProcessor.info(f"Not execution report: {dec}")
        return

    def _toDataBase(self, dec, msg):
        # (datetime.now().replace(tzinfo=timezone.utc) + timedelta(hours=-3)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:23]
        currentTime = datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%f')[:23]
        sendingTime = datetime.strptime(dec["SendingTime"], "%Y%m%d-%H:%M:%S.%f").strftime("%Y/%m/%dT%H:%M:%S.%f")[:23]
        transactTime = datetime.strptime(dec["TransactTime"], "%Y%m%d-%H:%M:%S.%f").strftime("%Y/%m/%dT%H:%M:%S.%f")[:23]
        _json = {
            # Control fields
            "id":               f"{uuid.uuid4()}",
            "createdAt":        currentTime,
            "updatedAt":        currentTime,
            "status":           0,
            # Fix message
            "account":          dec["Account"],
            "avgPx":            float(dec["AvgPx"]),
            "beginString":      mapBeginString(dec["BeginString"]),
            "bodyLength":       int(dec["BodyLength"]),
            "checkSum":         dec["CheckSum"],
            "clOrdID":          dec["ClOrdID"],
            "cumQty":           float(dec["CumQty"]),
            "execID":           dec["ExecID"],
            "execType":         mapExecType(dec["ExecType"]),
            "lastPx":           float(dec["LastPx"]),
            "lastQty":          float(dec["LastQty"]),
            "leavesQty":        float(dec["LeavesQty"]),
            "maxFloor":         float(dec["MaxFloor"]),
            "msgSeqNum":        int(dec["MsgSeqNum"]),
            "msgType":          8,
            "ordStatus":        mapOrdStatus(dec["OrdStatus"]),
            "ordType":          mapOrdType(dec["OrdType"]),
            "orderID":          dec["OrderID"],
            "orderQty":         float(dec["OrderQty"]),
            "origClOrdID":      dec["OrigClOrdID"],
            "price":            float(dec["Price"]),
            "securityExchange": dec["SecurityExchange"],
            "senderCompID":     0,
            "sendingTime":      sendingTime,
            "side":             mapSide(dec["Side"]),
            "stopPx":           float(dec["StopPx"]),
            "symbol":           dec["Symbol"],
            "targetCompID":     0,
            "timeInForce":      mapTimeInForce(dec["TimeInForce"]),
            "transactTime":     transactTime,
            "rawMessage":       f"{msg}"
        }

        try:
            self.cursor.execute(orderDataInsert, _json)
            self.connection.commit()
        except Exception as e:
            self.logProcessor.info(f"connection.commit() exception | {e}")
            self.logProcessor.info(f"{traceback.print_exc()}")
        return
    
    def cleanup(self):
        self.cursor.close()
        self.connection.close()
        return
