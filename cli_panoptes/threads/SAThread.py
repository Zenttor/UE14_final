import subprocess
import threading
from asyncio import sleep


class SAMaster(threading.Thread):
    def __init__(self, config_sa, queue):
        threading.Thread.__init__(self)
        self.config_sa = config_sa
        self.queue = queue

    def run(self):
        for row in self.config_sa:
            slave = SASlave(row, self.queue)
            slave.start()


class SASlave(threading.Thread):
    def __init__(self, config_sa, queue):
        threading.Thread.__init__(self)
        self.config_sa = config_sa

        self.queue = queue

    def run(self):
        # TODO commande
        resultat = subprocess.run([f"{self.command_script}{self.expected_result}"]).stdout.decode().strip()

        # TODO Compare

        # Si erreur on envoie dans la queue [Proto.EV_SA, infos_event]

        sleep(self.schedule)
