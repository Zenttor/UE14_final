import sqlite3
import subprocess

from utile.data import connect_db, select_data


def commande_execut(commande):
    run = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE)
    return (run.stdout.read()).decode()

# systemctl is-active syslog-ng
# systemctl is-active ssh.service

# systemctl restart ssh.service


def result_comp(nvx_result, attendu):
    if nvx_result.strip("\n") != attendu.strip("\n"):
        return False
    else:
        return True


def comparaison_sa(db_conn: sqlite3.Connection):
    try:
        jobs = select_data(db_conn,"SELECT * FROM sa_jobs", ())
        for commande in jobs:
            if result_comp(commande_execut(commande[3]), commande[4]):
                print("OK")
            else:
                print("Erreur")
    except sqlite3.Error as e:
        print(e)



comparaison_sa(connect_db("../cli_panoptes/data/cli_panoptes.sqlite"))
#systemctl restart syslog-ng
#Failed to restart syslog-ng.service: Unit syslog-ng.service Not found.