import threading
import subprocess
from time import sleep

from utile import data, event

SELECT = "SELECT * FROM sa_sets JOIN sa_jobs sj on sa_sets.sa_job_id = sj.sa_job_id"


class SA (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.dbconnexion = data.connect_db()
        self.config = data.select_data(self.dbconnexion, SELECT, ())

    def run(self):
        for row in self.config:
            schedule = row[3]
            command_script = row[7]
            expected_result = row[8]
            commande = Commande(schedule, command_script, expected_result)
            commande.start()


class Commande (threading.Thread):
    def __init__(self, schedule, command_script, expected_result):
        threading.Thread.__init__(self)
        self.schedule = schedule
        self.command_script = command_script
        self.expected_result = expected_result

    def run(self):
        subprocess.run([f"{self.command_script}{self.expected_result}"]).stdout.decode().strip()
        sleep(self.schedule)


if __name__ == "__main__":
    thread_sa = SA("test")
    thread_sa.start()

