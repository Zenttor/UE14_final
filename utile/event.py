import os.path
import threading
import time
from utile import data
from queue import Queue

CONFIG = 'test'
C_FIM = 0
C_SA = 1
C_IMG = 2
C_SCAN = 3

sa_req = f'INSERT INTO sa_events' \
         f'(sa_sets_id, sa_job_id, except_active, datetime_event)' \
         f'VALUES (?,?,?,datetime("now","+1 hour"))'

fim_req = f'INSERT INTO fim_events' \
          f'(datetime_event, except_msg, except_active, fim_set_id, fim_rule_id, image_id, file_inode)' \
          f'VALUES (datetime("now","+1 hour"), ?, ?, ?, ?, ?, ?)'

img_req = f'INSERT INTO ref_images' \
          f'(file_inode, datetime_image, parent_id, file_path, file_name, file_type, file_mode, file_nlink, file_uid' \
          f',file_gid, file_size, file_atime, file_mtime, file_ctime, file_md5, file_SHA1)' \
          f'VALUES(?, datetime("now","+1 hour"),?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

scan_req = f'INSERT INTO stat_files ' \
           f'(file_inode, parent_id, file_name, file_type, file_mode, file_nlink, file_uid, file_gid, file_size,' \
           f' file_atime, file_mtime, file_ctime, file_md5, file_SHA1)' \
           f' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


class EVThread(threading.Thread):
    def __init__(self, ready: bool):
        threading.Thread.__init__(self)

        if not os.path.isfile(CONFIG):
            server_configuration = Config(CONFIG)
            server_configuration.add_section('GENERAL').set(DB_NAME='../cli_panoptes/cli.panoptes.sqlite')
            server_configuration.save()
        else:
            server_configuration = Config(CONFIG)

        self.queue = q
        self.db_conn = data.connect_db(server_configuration.get_section('GENERAL').get('DB_NAME').value)
        self.daemon = True
        self.name = 'EV Daemon'

    def run(self):
        while True:
            try:
                while not self.queue.empty()

    def ev_sa(self, event:any) -> None:
        try:
            assert event[0] == C_SA
            data.insert_data(self.db_conn, sa_req, (event[1]).tuple())
        except IOError as error:
            print(f"Erreur dans EV Thread SA : {error}")
            data.disconnect_db(self.db_conn)
    def ev_fim(self, event:any) -> None:
        try:
            assert event[0] == C_FIM
            for ev in event[0]:
                data.insert_data(self.db_conn, fim_req, ev.tuple())
        except IOError as error:
            print(f'Erreur dans EV Thread FIM : {error}')
            data.disconnect_db(self.db_conn)