import requests
import traceback
import json
import logging
from model.logger import setup_logger

class Webhook():
    def __init__(self, webhook, active):
        self.active = active
        self.webhook = webhook
        setup_logger("logwebhook", "./log-webhook.log")
        self.logWebhook = logging.getLogger("logwebhook")
        self.logWebhook.info("Webhook logging started")
        return

    def send(self, message):
        self.logWebhook.info(f"Webhook.send() | {message}")
        _json = json.dumps({"type": message})
        if self.active == 'True':
            try:
                requests.post(self.webhook, json=_json, timeout=10)
            except Exception as e:
                self.logWebhook.info(f"Webhook.send() -> exception | {message} | {e}")
                self.logWebhook.info(f"{traceback.print_exc()}")
        return
