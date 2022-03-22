#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is sync.py
"""
import os
import argparse
from static import Static


class Sync():
    """use : sync (sourcefolder, destfolder, keyword=your_keyword)
    keyword is used to filter which files are copied, only those whith
    names including keyword"""

    def __init__(self, sourcefolder, destfolder, keyword=''):
        self.keyword = keyword
        self.sourcefolder = Static.tildexpand(sourcefolder)
        self.destfolder = Static.tildexpand(destfolder)
        if not os.path.isdir(destfolder):
            os.makedirs(destfolder)

    def copyfolders(self, source, dest):
        """recopie les fichiers du repertoire source ainsi que ses
        sous repertoire vers le repertoire dest et copie le plus recent s'ils ont le meme nom"""
        fileslist = Static.listfileskw(source, self.keyword)
        folderlist = Static.listfolders(source)
        for file in fileslist:
            Static.copyfile(source, dest, file)
        for subfolder in folderlist:
            if not os.path.isdir(f'{dest}/{subfolder}'):
                os.makedirs(f'{dest}/{subfolder}', exist_ok=True)
            self.copyfolders(f'{source}/{subfolder}', f'{dest}/{subfolder}')

    def cypherfolders(self, source, dest, password=''):
        """7zip with password all files in source to all files.7z in dest
        if they dont exist or are more recent"""
        fileslist = Static.listfileskw(source, self.keyword)
        folderlist = Static.listfolders(source)
        for file in fileslist:
            Static.copyfilec(source, dest, file, password)
        for subfolder in folderlist:
            if not os.path.isdir(f'{dest}/{subfolder}'):
                os.makedirs(f'{dest}/{subfolder}', exist_ok=True)
            self.cypherfolders(f'{source}/{subfolder}', f'{dest}/{subfolder}')

    def decypherfolders(self, source, dest, password=''):
        """un7zip password all files.7z in source to all files in dest
        if they dont exist or are more recent"""
        fileslist = Static.listfileskw(source,
                                       r'({}).+(\.7z$)'.format(self.keyword))
        folderlist = Static.listfolders(source)
        for file in fileslist:
            Static.copyfiled(source, dest, file, password)
        for subfolder in folderlist:
            if not os.path.isdir(f'{dest}/{subfolder}'):
                os.makedirs(f'{dest}/{subfolder}', exist_ok=True)
            self.decypherfolders(f'{source}/{subfolder}',
                                 f'{dest}/{subfolder}')

    ### interface ###
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
