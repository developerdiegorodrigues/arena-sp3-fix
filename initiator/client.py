"""FIX GATEWAY"""
import sys
import argparse
import quickfix
from application import Application
import logging
from model.logger import setup_logger

setup_logger("logclient", "./log-client.log")
logClient = logging.getLogger("logclient")

def main(config_file):
    """Main"""
    logClient.info("Initiator logging started")
    try:
        settings = quickfix.SessionSettings(config_file)
        application = Application()
        storefactory = quickfix.FileStoreFactory(settings)
        logfactory = quickfix.FileLogFactory(settings)
        initiator = quickfix.SocketInitiator(application, storefactory, settings, logfactory)

        initiator.start()
        application.run()
        initiator.stop()

    except (quickfix.ConfigError, quickfix.RuntimeError) as e:
        logClient.info(f"Initiator exception | {e}")
        initiator.stop()
        sys.exit()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()
    main(args.file_name)
