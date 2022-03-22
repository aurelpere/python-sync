#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is static.py
"""
import os
import filecmp
import re
import shutil
import functools
import py7zr


class Static():

    def __init__(self):
        self.name = 'Static'

    @staticmethod
    def tildexpand(chain):
        "expand tild in folder names"
        if '~/' in chain:
            tildexpand = os.path.expanduser('~/')
            result = chain.replace('~/', tildexpand)
            return result
        return chain

    @staticmethod
    def listfileskw(directory, keyword=""):
        "la fonction listfiles renvoie une liste des fichiers du répertoire folder contenant kw"
        currentfolder = os.getcwd()
        os.chdir(directory)
        files = []
        itemslist = os.listdir()
        for item in itemslist:
            if keyword != "":
                if os.path.isfile(item) and Static.findkeyword(item, keyword):
                    files.append(item)
            else:
                if os.path.isfile(item):
                    files.append(item)
        os.chdir(currentfolder)
        return files

    @staticmethod
    def findkeyword(chain, keyword):
        "return true if keyword in chain"
        compiledkw = re.compile(r'{}'.format(keyword))
        if re.search(compiledkw, chain):
            return True

    @staticmethod
    def listfolders(folder):
        """la fonction listfolders renvoie une liste des noms des
        sousrépertoires du repertoire folder"""
        currentfolder = os.getcwd()
        os.chdir(folder)
        folders = []
        dirlist = os.listdir()
        for item in dirlist:
            if os.path.isdir(item):
                folders.append(item)
        os.chdir(currentfolder)
        return folders

    @staticmethod
    def timestamp_check(sourcefile, destfile):
        "return True if files are different and sourcefile is more recent than destfile"
        if not filecmp.cmp(sourcefile, destfile):
            print('files different')
            # si le fichier dest est différent du fichier source
            timestampdest = os.stat(destfile)[8]
            timestampsrc = os.stat(sourcefile)[8]
            print(timestampsrc)
            print(timestampdest)
            if timestampsrc > timestampdest:
                return True

    def fileprocessing(func):
        "decorator for cypher,decypher and copy methods"

        @functools.wraps(func)
        def wrapped_f(*args):
            "process copy if source files are newer in case they exist in dest"
            source = args[0]
            dest = args[1]
            file = args[2]
            if func.__name__ == 'copyfile':
                destfile = f'{dest}/{file}'
            elif func.__name__ == 'copyfilec':
                destfile = f'{dest}/{file}.7z'
            else:
                destfile = f'{dest}/{file}'.replace(".7z", " ").strip()
            print(destfile)
            if os.path.isfile(destfile):  # si le fichier dest existe
                print('destfile exists')
                if Static.timestamp_check(f'{source}/{file}', destfile):
                    func(*args)
            else:  # si le fichier dest n'existe pas
                func(*args)

        return wrapped_f

    @staticmethod
    def pythoncopyfile(src_file, dest_file):
        "copy src to dest_folder bytes by bytes with python. used to replace shutil.copy2"
        with open(src_file, 'rb') as filesrc:
            filelist = filesrc.readlines()
        with open(f'{dest_file}', 'wb') as filedest:
            for line in filelist:
                filedest.write(line)

    @staticmethod
    @fileprocessing
    def copyfile(src, dst, file):
        "try copying with shutil file in src folder to dst folder, otherwise with python"
        try:
            shutil.copy2(f'{src}/{file}',
                         f'{dst}/{file}',
                         follow_symlinks=False)
        except Exception as err:
            print(err)
            Static.pythoncopyfile(f'{src}/{file}', f'{dst}/{file}')

    @staticmethod
    @fileprocessing
    def copyfilec(src, dst, file, password):
        """cypher file in src folder to dst folder with py7zr
        to dst/file.7z with password if provided"""
        cwd = os.getcwd()
        with py7zr.SevenZipFile(f'{dst}/{file}.7z',
                                mode='w',
                                password=password) as archive:
            os.chdir(src)
            archive.write(f'./{file}')
            os.chdir(cwd)

    @staticmethod
    @fileprocessing
    def copyfiled(src, dst, file, password):
        """decypher file in dst folder to src folder with py7zr
                to dst/file with password if provided"""
        with py7zr.SevenZipFile(f'{src}/{file}', mode='r',
                                password=password) as archive:
            archive.extractall(path=dst)
