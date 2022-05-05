import os.path
from glob import iglob
from os import stat, pardir, path
from stat import *
from time import time
from hashlib import md5, sha1

from utile import data
from utile.data import connect_db, select_data


def get_ref_image(filename='/home/q210002/Desktop/test.py'):
    ref_image = {}
    stat_info = stat(filename)
    ref_image['file_inode'] = stat_info.st_ino
    ref_image['datetime_image'] = int(time())
    ref_image['parent_id'] = stat(path.abspath(path.join(filename, pardir))).st_ino
    ref_image['file_name'] = filename
    ref_image['file_type'] = type_file(stat_info.st_mode)
    ref_image['file_mode'] = filemode(stat_info.st_mode)
    ref_image['file_nlink'] = stat_info.st_nlink
    ref_image['file_uid'] = stat_info.st_uid
    ref_image['file_gid'] = stat_info.st_gid
    ref_image['file_size'] = stat_info.st_size
    ref_image['file_atime'] = int(stat_info.st_atime)
    ref_image['file_mtime'] = int(stat_info.st_mtime)
    ref_image['file_ctime'] = int(stat_info.st_ctime)
    ref_image['file_md5'] = md5_file(filename)
    ref_image['file_sha1'] = sha1_file(filename)
    return ref_image


def get_stat_image(filename):
    ref_image = {}
    stat_info = stat(filename)
    ref_image['file_inode'] = stat_info.st_ino
    ref_image['parent_id'] = stat(path.abspath(path.join(filename, pardir))).st_ino
    ref_image['file_name'] = filename
    ref_image['file_type'] = type_file(stat_info.st_mode)
    ref_image['file_mode'] = filemode(stat_info.st_mode)
    ref_image['file_link'] = stat_info.st_nlink
    ref_image['file_uid'] = stat_info.st_uid
    ref_image['file_gid'] = stat_info.st_gid
    ref_image['file_size'] = stat_info.st_size
    ref_image['file_atime'] = int(stat_info.st_atime)
    ref_image['file_mtime'] = int(stat_info.st_mtime)
    ref_image['file_ctime'] = int(stat_info.st_ctime)
    ref_image['file_md5'] = md5_file(filename)
    ref_image['file_SHA1'] = sha1_file(filename)
    return ref_image


def type_file(mode):
    """

    :param mode: 'D' --> Directory, R --> Regular file, B --> Block file, C --> Character file, L --> Link file
    :return:
    """
    if S_ISDIR(mode):
        return 'D'
    if S_ISREG(mode):
        return 'R'
    if S_ISBLK(mode):
        return 'B'
    if S_ISCHR(mode):
        return 'C'
    if S_ISLNK(mode):
        return 'L'


def md5_file(filename=''):
    if os.path.isfile(filename):
        hash_md5 = md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    return None


def sha1_file(filename=''):
    if os.path.isfile(filename):
        hash_sha1 = sha1()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()
    return None


def get_files(pattern):
    i = 0
    for filename in iglob(pattern, recursive=True):
        liste = [i]
        for valeur in get_ref_image(filename).values():
            liste.append(valeur)
        data.insert_data(connect_db('../cli_panoptes/data/cli_panoptes.sqlite'), "INSERT INTO ref_images VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", liste)

        i += 1


def get_stat(pattern):
    for filename in iglob(pattern, recursive=True):
        liste = []
        for valeur in get_stat_image(filename).values():
            liste.append(valeur)
        data.insert_data(connect_db('../cli_panoptes/data/cli_panoptes.sqlite'), "INSERT INTO stat_files VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", liste)


def comparaison():
    changements = []
    db_conn = connect_db('../cli_panoptes/data/cli_panoptes.sqlite')
    select_ref_images = select_data(db_conn, 'SELECT * FROM ref_images', ())
    for ligne in select_ref_images:
        valeur_base = select_data(db_conn, f'SELECT * FROM stat_files WHERE file_inode = ?', (ligne[1],))
        valeur_image = select_data(db_conn, f'SELECT * FROM ref_images WHERE file_inode = ?', (ligne[1],))

        rules = select_data(db_conn, f'SELECT * FROM fim_rules', ())
        change = ""
        try:
            #filename
            if rules[0][6] and valeur_base[0][2] != valeur_image[0][4]:
                change += f'Le nom a changé:  Nouveau -> {valeur_base[0][2]}  Ancien -> {valeur_image[0][4]} '
            #parent
            if rules[0][5] and valeur_base[0][1] != valeur_image[0][3]:
                change += f'Le dossier parent a changé:  Nouveau ->  {valeur_base[0][1]}  Ancien -> {valeur_image[0][3]} '
            #type
            if rules[0][7] and valeur_base[0][3] != valeur_image[0][5]:
                change += f'Le type a changé:  Nouveau ->  {valeur_base[0][3]}  Ancien -> {valeur_image[0][5]} '
            #mode
            if rules[0][8] and valeur_base[0][4] != valeur_image[0][6]:
                change += f'Le mode a changé:  Nouveau ->  {valeur_base[0][4]}  Ancien -> {valeur_image[0][6]} '
            #nlink
            if rules[0][9] and valeur_base[0][5] != valeur_image[0][7]:
                change += f'Le nlink a changé:  Nouveau ->  {valeur_base[0][5]}  Ancien -> {valeur_image[0][7]} '
            #uid
            if rules[0][10] and valeur_base[0][6] != valeur_image[0][8]:
                change += f'Le uid a changé:  Nouveau ->  {valeur_base[0][6]}  Ancien -> {valeur_image[0][8]} '
            #gid
            if rules[0][11] and valeur_base[0][7] != valeur_image[0][9]:
                change += f'Le gid a changé:  Nouveau ->  {valeur_base[0][7]}  Ancien -> {valeur_image[0][9]} '
            #size
            if rules[0][12] and valeur_base[0][8] != valeur_image[0][10]:
                change += f'Le size a changé:  Nouveau ->  {valeur_base[0][8]}  Ancien -> {valeur_image[0][10]} '
            #atime
            if rules[0][13] and valeur_base[0][9] != valeur_image[0][11]:
                change += f'Le atime a changé:  Nouveau ->  {valeur_base[0][9]}  Ancien -> {valeur_image[0][11]} '
            #mtime
            if rules[0][14] and valeur_base[0][10] != valeur_image[0][12]:
                change += f'Le mtime a changé:  Nouveau ->  {valeur_base[0][10]}  Ancien -> {valeur_image[0][12]} '
            #ctime ???
            if rules[0][17] and valeur_base[0][11] != valeur_image[0][13]:
                change += f'Le ctime a changé:  Nouveau ->  {valeur_base[0][11]}  Ancien -> {valeur_image[0][13]} '
            #md5
            if rules[0][15] and valeur_base[0][12] != valeur_image[0][14]:
                change += f'Le md5 a changé:  Nouveau ->  {valeur_base[0][12]}  Ancien -> {valeur_image[0][14]} '
            #SHA1
            if rules[0][16] and valeur_base[0][13] != valeur_image[0][15]:
                change += f'Le SHA1 a changé:  Nouveau ->  {valeur_base[0][13]}  Ancien -> {valeur_image[0][15]} '
            if change:
                change += ' ' + valeur_base[0][2]
                changements.append(change)
        except IndexError as error:
            print(f"Erreur dans la comparaison: {error}")
        if changements:
            print(changements)
        print("coucou")


def main():
    # print(get_image())
    get_files('/home/q210002/Desktop/**')
    get_stat('/home/q210002/Desktop/**')
    comparaison()

if __name__ == '__main__':
    main()


