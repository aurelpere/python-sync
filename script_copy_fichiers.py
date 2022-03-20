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
import py7zr

def mkdirs(newdir):
    "make dir with 777 mode"
    try:
        os.makedirs(newdir)
        return 1
    except OSError as err:
        return err

def listfileskw(folder, keyword=""):
    "la fonction listfiles renvoie une liste des fichiers du répertoire folder contenant kw"
    currentfolder=os.getcwd()
    os.chdir(folder)
    files = []
    dirlist = os.listdir()
    templist = []
    for i in dirlist:
        if keyword!="":
            compiledkw=re.compile(r'{}'.format(keyword))
            if os.path.isfile(i) and re.search(compiledkw, i):
                files.append(i)
            else:
                templist.append(i)
        else:
            if os.path.isfile(i):
                files.append(i)
            else:
                templist.append(i)
    os.chdir(currentfolder)
    return files

def listfolders(folder):
    "la fonction listfolders renvoie une liste des noms des sousrépertoires du repertoire folder"
    currentfolder=os.getcwd()
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

def dico_maker(folder):
    "renvoie un dictionnaire des fichiers et repertoires de folder"
    dico={}
    fileslist = listfileskw(folder)
    folderlist = listfolders(folder)
    dico[folder] = fileslist
    for fold in folderlist:
        dico[f'{folder}/{fold}'] = listfileskw(f'{folder}/{fold}')
        dico_maker(f'{folder}/{fold}')
    return dico

def recopier(source, dest,keyword=''):
    """recopie les fichiers du repertoire source ainsi que ses
    sous repertoire vers le repertoire dest et copie le plus recent s'ils ont le meme nom"""
    if keyword!='':
        fileslist = listfileskw(source,keyword)
    else:
        fileslist=listfileskw(source)
    folderlist = listfolders(source)
    identique = []
    for i in fileslist:
        if os.path.isfile(f'{dest}/{i}'):  # si le fichier dest existe
            if not filecmp.cmp(f'{source}/{i}', f'{dest}/{i}'):
            # si le fichier dest est différent du fichier source
                timestampdest = os.stat(f'{dest}/{i}')
                timestampsrc = os.stat(f'{source}/{i}')
                if timestampsrc[8] > timestampdest[8]:
                    # si le fichier source est plus récent que le fichier dest
                    # stat[8] donne le mtime cad le temps en seconde depuis lequel le
                    # fichier a été modifié. copyfile conserve cette propriété
                    try:
                        shutil.copy2(f'{source}/{i}', f'{dest}/{i}',follow_symlinks=False)
                    except Exception as err:
                        print (err)
                        pythoncopy(f'{source}/{i}', f'{dest}/{i}')
            else:
            # sinon on ajoute les fichiers identiques à une liste qui n'est pas utilise
                identique.append(i)
        else:  # si le fichier dest n'existe pas
            try:
                shutil.copy2(f'{source}/{i}', f'{dest}/{i}', follow_symlinks=False)
            except Exception as err:
                print(err)
                pythoncopy(f'{source}/{i}', f'{dest}/{i}')
    for j in folderlist:
        if os.path.isdir(f'{dest}/{j}'):
            print(f'{dest}/{j} existe')
        else:
            mkdirs(f'{dest}/{j}')
        recopier(f'{source}/{j}', f'{dest}/{j}')

def pythoncopy(src_file,dest_file):
    "copy src to dest_folder bytes by bytes. used to replace shutil.copy2"
    with open(src_file,'rb') as filesrc:
        filelist=filesrc.readlines()
    with open(f'{dest_file}','wb') as filedest:
        for i in filelist:
            filedest.write(i)

def chiffrer(source, dest,keyword='',password=''):
    """la fonction chiffrer(source,dest) 7zippe avec chiffrement les fichiers
    du repertoire source ainsi que ses sous repertoire vers le repertoire dest
    s'ils n'existent pas ou s'ils sont plus recent (pr le meme nom)"""
    cwd=os.getcwd()
    if keyword!='':
        fileslist = listfileskw(source,keyword)
    else:
        fileslist=listfileskw(source)
    folderlist = listfolders(source)
    identique = []
    for i in fileslist:
        if os.path.isfile(f'{dest}/{i}.7z'):  # si le fichier dest existe en .7z
            timestampdest = os.stat(f'{dest}/{i}.7z')
            timestampsrc = os.stat(f'{source}/{i}')
            if timestampsrc[8] > timestampdest[8]:
                # si le timestamp source est plus récent que celui du dest
                with py7zr.SevenZipFile(f'{dest}/{i}.7z', mode='w',password=password) as archive:
                    os.chdir(source)
                    archive.write(f'./{i}')
                    os.chdir(cwd)
            else:  # sinon on ajoute les fichiers identiques à une liste qui n'est pas utilise
                identique.append(i)
        else:  # si le fichier dest n'existe pas
            with py7zr.SevenZipFile(f'{dest}/{i}.7z', mode='w',password=password) as archive:
                os.chdir(source)
                archive.write(f'./{i}')
                os.chdir(cwd)

    for j in folderlist:
        if os.path.isdir(f'{dest}/{j}'):
            print(f"{dest}/{j} existe ou il y a eu un message d'erreur de copie")
        else:
            mkdirs(f'{dest}/{j}')
        chiffrer(f'{source}/{j}', f'{dest}/{j}')

def dechiffrer(source, dest,keyword='',password=''):
    """la fonction dechiffrer(source,dest) utilise 7zipp pour extraire les
     archives du repertoire source et ses sous repertoires vers le repertoire
     dest s'ils n'existent pas ou s'ils sont plus recent (pr le meme nom)"""
    if keyword!='':
        fileslist = listfileskw(source,r'({}).+(\.7z$)'.format(keyword))
    else:
        fileslist=listfileskw(source,'.7z')
    folderlist = listfolders(source)
    identique = []
    for i in fileslist:
        no7z_i = f'{i}'.replace(".7z", " ").strip()
        if os.path.isfile(f'{dest}/{no7z_i}'):  # si le fichier dest existe sans .7z
            timestampdest = os.stat(f'{dest}/{no7z_i}')
            timestampsrc = os.stat(f'{source}/{i}')
            if timestampsrc[8] > timestampdest[8]:
                with py7zr.SevenZipFile(f'{source}/{i}', mode='r', password=password) as archive:
                    archive.extractall(path=dest)
            else:  # sinon on ajoute les fichiers identiques à une liste qui n'est pas utilise
                identique.append(i)
        else:  # si le fichier dest n'existe pas
            with py7zr.SevenZipFile(f'{source}/{i}', mode='r', password=password) as archive:
                archive.extractall(path=dest)
    for j in folderlist:
        if os.path.isdir(f'{dest}/{j}'):
            print(f"{dest}/{j} existe ou il y a eu un message d'erreur de copie")
        else:
            os.mkdir(f'{dest}/{j}')
        dechiffrer(f'{source}/{j}', f'{dest}/{j}')

def script_copy_fichiers(sourcefolder,destfolder,keyword='',cypher='',decypher=''):
    """copy files from sourcefolder to destfolder and only copy files containing
    keyword if defined. cypher dest files if cypher=1"""
    sourcedict=dico_maker(sourcefolder)
    keyslist = list(sourcedict.keys())
    if '~/' in destfolder:
        tildexpand = os.path.expanduser('~/')
        destfolder=destfolder.replace('~/',tildexpand)
    if not os.path.isdir(destfolder):
        mkdirs(destfolder)
    if cypher=='' and decypher=='':
        for key in keyslist:  # key is a folder
            recopier(key, destfolder,keyword=keyword)
    elif cypher!='' and decypher=='':
        for key in keyslist:
            chiffrer(key,destfolder,password=cypher,keyword=keyword)
    elif cypher!='' and decypher!='':
        print('chooose either to cypher or decypher')
    else:
        dechiffrer(sourcefolder,destfolder,password=decypher,keyword=keyword)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='python script_copy_fichiers.py csvfile year')
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
    parser.add_argument('-k',
                        '--keyword',
                        default='',
                        metavar='keyword: will copy files only if keyword included in filenames',
                        type=str,
                        help='keyword that must be included in filesnames to process copy')
    parser.add_argument('-c',
                        '--cypher',
                        default='',
                        metavar='will cypher with 7zip with the password provided',
                        type=str,
                        help='will cypher the copy with 7ziping files with the password provided')
    parser.add_argument('-dc',
                        '--decypher',
                        default='',
                        metavar='will decypher with 7zip with the password provided',
                        type=str,
                        help='will decypher the copied files with the password provided')

    args = vars(parser.parse_args())
    script_copy_fichiers(args['origin'],
                         args['dest'],
                         keyword=args['keyword'],
                         cypher=args['cypher'],
                         decypher=args['decypher'])
