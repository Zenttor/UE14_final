import threading


class EventMaster(threading.Thread):
    def __init__(self, config_fim, queue):
        threading.Thread.__init__(self)
        self.config_fim = config_fim
        self.queue = queue

    def run(self):
        while True:
            pass