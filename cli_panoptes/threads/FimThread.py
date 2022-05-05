import threading


class FimMaster(threading.Thread):
    def __init__(self, config_fim, queue):
        threading.Thread.__init__(self)
        self.config_fim = config_fim
        self.queue = queue

    def run(self):
        for row in self.config_fim:
            slave = FimSlave(row, self.queue)
            slave.start()


class FimSlave(threading.Thread):
    def __init__(self, config_fim, queue):
        threading.Thread.__init__(self)
        self.config_fim = config_fim

        self.queue = queue

    def run(self):
        pass
