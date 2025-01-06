import time

__SOH__ = chr(1)

class FixSimulator:
    """Simulador de envio de mensagens FIX baseado em arquivo de log gerado pelo initiator"""
    
    def __init__(self, executeSimulator, simulatorFile, simulatorTimer, decoder):
        self.executeSimulator = executeSimulator
        self.logFile = simulatorFile
        self.interval = simulatorTimer
        self.decodeMessage = decoder
        self.messages = []
        return

    def _loadMessages(self):
        # Caution with too big files
        try:
            with open(self.logFile, 'r') as file:
                for line in file:
                    timestamp, message = line.strip().split(" : ", 1)
                    self.messages.append(message)
            file.close()
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar o arquivo de log: {e}")
        return

    def _simulate(self, sessionID, fromApp):
        print(f"Simulation started {sessionID}")
        for message in self.messages:
            try:
                msg = f"{message}".replace(__SOH__, "|")
                print(f"Sending message: {msg}")
                fromApp(message, sessionID)
                # if quickfix.Session.sendToTarget(quickfix.Message(message), sessionID):
                #     print(f"@@@ MENSAGEM ENVIADA")
                # else:
                #     self.decodeMessage(msg)
                #     print(f"#### ERRO AO ENVIAR MENSAGEM")
                print(f"@@@ Message sent")
            except Exception as e:
                self.decodeMessage(msg)
                print(f"### Send messagem exception: {e}")
            time.sleep(float(self.interval))
        return

    def run(self, sessionID, fromApp):
        if (self.executeSimulator != 'True'):
            return
        self._loadMessages()
        self._simulate(sessionID, fromApp)
        return

    def cleanup(self):
        self.messages = []
        return
