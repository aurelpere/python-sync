#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is script_copy_fichiers.py
"""
import os
import filecmp
import re
import argparse
import shutil
import functools
import py7zr


class Sync():
    """use : sync (sourcefolder, destfolder, keyword=your_keyword)
    keyword is used to filter which files are copied, only those whith
    names including keyword"""

    def __init__(self, sourcefolder, destfolder, keyword=''):
        self.keyword = keyword
        self.sourcefolder = self.tildexpand(sourcefolder)
        self.destfolder = self.tildexpand(destfolder)
        if not os.path.isdir(destfolder):
            self.mkdirs(destfolder)

    @staticmethod
    def mkdirs(newdir):
        "make newdir with"
        try:
            os.makedirs(newdir)
            return 1
        except OSError as err:
            return err

    @staticmethod
    def listfileskw(directory, keyword=""):
        "la fonction listfiles renvoie une liste des fichiers du répertoire folder contenant kw"
        currentfolder = os.getcwd()
        os.chdir(directory)
        files = []
        dirlist = os.listdir()
        for folder in dirlist:
            if keyword != "":
                compiledkw = re.compile(r'{}'.format(keyword))
                if os.path.isfile(folder) and re.search(compiledkw, folder):
                    files.append(folder)
            else:
                if os.path.isfile(folder):
                    files.append(folder)
        os.chdir(currentfolder)
        return files

    @staticmethod
    def listfolders(folder):
        """la fonction listfolders renvoie une liste des noms des
        sousrépertoires du repertoire folder"""
        currentfolder = os.getcwd()
        os.chdir(folder)
        folders = []
        dirlist = os.listdir()
        templist = []
        for i in dirlist:
            if os.path.isdir(i):
                folders.append(i)
            else:
                templist.append(i)
        os.chdir(currentfolder)
        return folders

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
                if not filecmp.cmp(f'{source}/{file}', destfile):
                    print('files different')
                    # si le fichier dest est différent du fichier source
                    timestampdest = os.stat(destfile)[8]
                    timestampsrc = os.stat(f'{source}/{file}')[8]
                    print(timestampsrc)
                    print(timestampdest)
                    if timestampsrc > timestampdest:
                        # si le fichier source est plus récent que le fichier dest
                        # stat[8] donne le mtime cad le temps en seconde depuis lequel le
                        # fichier a été modifié. copyfile conserve cette propriété
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
            self.pythoncopyfile(f'{src}/{file}', f'{dst}/{file}')

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

    def copyfolders(self, source, dest):
        """recopie les fichiers du repertoire source ainsi que ses
        sous repertoire vers le repertoire dest et copie le plus recent s'ils ont le meme nom"""
        if self.keyword != '':
            fileslist = self.listfileskw(source, self.keyword)
        else:
            fileslist = self.listfileskw(source)
        folderlist = self.listfolders(source)
        for file in fileslist:
            self.copyfile(source, dest, file)
        for subfolder in folderlist:
            if os.path.isdir(f'{dest}/{subfolder}'):
                print(f'{dest}/{subfolder} existe')
            else:
                self.mkdirs(f'{dest}/{subfolder}')
            self.copyfolders(f'{source}/{subfolder}', f'{dest}/{subfolder}')

    def cypherfolders(self, source, dest, password=''):
        """7zip with password all files in source to all files.7z in dest
        if they dont exist or are more recent"""
        if self.keyword != '':
            fileslist = self.listfileskw(source, self.keyword)
        else:
            fileslist = self.listfileskw(source)
        folderlist = self.listfolders(source)
        for file in fileslist:
            self.copyfilec(source, dest, file, password)
        for subfolder in folderlist:
            if os.path.isdir(f'{dest}/{subfolder}'):
                print(
                    f"{dest}/{subfolder} existe ou il y a eu un message d'erreur de copie"
                )
            else:
                self.mkdirs(f'{dest}/{subfolder}')
            self.cypherfolders(f'{source}/{subfolder}', f'{dest}/{subfolder}')

    def decypherfolders(self, source, dest, password=''):
        """un7zip password all files.7z in source to all files in dest
        if they dont exist or are more recent"""
        if self.keyword != '':
            fileslist = self.listfileskw(source,
                                         r'({}).+(\.7z$)'.format(self.keyword))
        else:
            fileslist = self.listfileskw(source, '.7z')
        folderlist = self.listfolders(source)
        for file in fileslist:
            self.copyfiled(source, dest, file, password)
        for subfolder in folderlist:
            if os.path.isdir(f'{dest}/{subfolder}'):
                print(
                    f"{dest}/{subfolder} existe ou il y a eu un message d'erreur de copie"
                )
            else:
                os.mkdir(f'{dest}/{subfolder}')
            self.decypherfolders(f'{source}/{subfolder}',
                                 f'{dest}/{subfolder}')

    @staticmethod
    def tildexpand(chain):
        "expand tild in folder names"
        if '~/' in chain:
            tildexpand = os.path.expanduser('~/')
            result = chain.replace('~/', tildexpand)
            return result
        return chain

    def cypher(self, password=''):
        """cypher method made for interpreter use :
        imported_module.Sync(sourcefolder,destfolder,keyword).cypher('password')"""
        self.cypherfolders(self.sourcefolder,
                           self.destfolder,
                           password=password)

    def decypher(self, password=''):
        """cypher method made for interpreter use :
        imported_module.Sync(sourcefolder,destfolder,keyword).decypher('password')"""
        self.decypherfolders(self.sourcefolder,
                             self.destfolder,
                             password=password)

    def copy(self):
        """copy method made for interpreter use :
        imported_module.Sync(sourcefolder,destfolder,keyword).copy()"""
        self.copyfolders(self.sourcefolder, self.destfolder)

    def choose(self, cypherpw='', decypherpw=''):
        """choose copy,cypher, or decypher from source to dest
        for command line use:
        python script_copy_fichiers.py -o originfolder -d destfolder
        -k keyword [-c password][-d password]"""
        if cypherpw == '' and decypherpw == '':
            self.copy()
        elif cypherpw != '' and decypherpw == '':
            self.cypher(password=cypherpw)
        elif cypherpw != '' and decypherpw != '':
            print('chooose either to cypher or decypher')
        else:
            self.decypher(password=decypherpw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    python script_copy_fichiers.py -o originfolder -d destfolder -k keyword
    [-c password][-d password]')
    """)
    parser.add_argument('-o',
                        '--origin',
                        required=True,
                        metavar='origin folder',
                        type=str,
                        help='origin folder to process')
    parser.add_argument('-d',
                        '--dest',
                        required=True,
                        metavar='destination folder',
                        type=str,
                        help='destination folder to copy to')
    parser.add_argument(
        '-k',
        '--keyword',
        default='',
        metavar=
        'keyword : will copy files only if keyword included in filenames',
        type=str,
        help='keyword that must be included in filesnames to process copy')
    parser.add_argument(
        '-c',
        '--cypher',
        default='',
        metavar='password : will cypher with 7zip with the password provided',
        type=str,
        help=
        'will cypher the copy with 7ziping files with the password provided')
    parser.add_argument(
        '-dc',
        '--decypher',
        default='',
        metavar='password : will decypher with 7zip with the password provided',
        type=str,
        help='will decypher the copied files with the password provided')

    arguments = vars(parser.parse_args())
    sync_object = Sync(arguments['origin'],
                       arguments['dest'],
                       keyword=arguments['keyword'])
    sync_object.choose(cypherpw=arguments['cypher'],
                       decypherpw=arguments['decypher'])
