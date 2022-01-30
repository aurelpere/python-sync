#!/usr/bin/python3
# -*- coding:utf-8 -*-
# script qui recopie un répertoire dans un autre répertoire
# définir source et dest avant de lancer le script
# version brutecopy sans identifier les modifs
di = "/"
df = "/home/user/df"
kw = "brave"

import shutil
import os
import time
import filecmp


def mkdirs(newdir, mode=777):
    try:
        os.makedirs(newdir, mode)
    except OSError as err:
        return err

def test_mkdirs():
    mkdirs('testfolder')
    assert os.path.isdir('testfolder')==True
    
def contain(chaine1, chaine2):
    "true si chaine1 inclut ds chaine2"
    chaine1 = chaine1.lower()
    chaine2 = chaine2.lower()
    L = len(chaine1)
    if len(chaine2) < len(chaine1):
        return False
    for i in range(len(chaine2) - L + 1):
        slicee = ""
        for j in range(L):
            slicee += chaine2[i + j]
        if slicee == chaine1: 
            return True
    return False

def test_contain():
    assert contain('test','this is a test')==True
    assert contain('test','this is a sentence')==False

def listFiles(folder):
    "la fonction listFiles renvoie une liste des fichiers du répertoire courant contenant kw"
    os.chdir(folder)
    files = []
    a = os.listdir()
    b = []
    for i in a:
        if os.path.isfile(i):
            files.append(i)
        else:
            b.append(i)
    return files

def test_listFiles():
    assert sorted(listFiles('/Users/macbook/github/scraping'))==['boxplot_scraping.png','README.md','scraping.py']



def listFileskw(folder, kw=""):
    "la fonction listFiles renvoie une liste des fichiers du répertoire folder contenant kw"
    os.chdir(folder)
    files = []
    a = os.listdir()
    b = []
    for i in a:
        if os.path.isfile(i) and contain(i, kw):
            files.append(i)
        else:
            b.append(i)
    return files

def test_listFileskw():
    assert sorted(listFileskw('/Users/macbook/github/scraping',kw='scraping'))==['boxplot_scraping.png','scraping.py']



def listFolders(folder):
    "la fonction listFolders renvoie une liste des noms des sousrépertoires du repertoire folder"
    os.chdir(folder)
    folders = []
    a = os.listdir()
    b = []
    for i in a:
        if os.path.isdir(i):
            folders.append(i)
        else:
            b.append(i)
    return folders

def test_listFolders():
    assert sorted(listFolders('/Users/macbook/github/scraping'))==['subfolder']



def dicoisation(dico, folder):
    "renvoie un dictionnaire des fichiers et repertoires de folder"
    a = listFiles(folder)
    b = listFolders(folder)
    dico[folder] = a
    for m in b:
        dico[folder + "/" + m] = listFiles(folder + "/" + m)
        dicoisation(dico, folder + "/" + m)
    return dico

def test_dicoisation():
    assert (dicoisation('/Users/macbook/github/scraping'))=={'/Users/macbook/github/scraping':['boxplot_scraping.png','README.md','scraping.py'],'/Users/macbook/github/scraping/subfolder':['']}



def recopier(source, dest):
    "recopie les fichiers du repertoire source ainsi que ses sous repertoire vers le repertoire dest et copie le plus recent s'ils ont le meme nom"

    a = listFiles(source)
    b = listFolders(source)
    timestampsrc = 0
    timestampdest = 0
    identique = []
    # print(a)
    for i in a:
        if os.path.isfile(str(dest) + "/" + i):  # si le fichier dest existe
            if not (
                filecmp.cmp(str(i), str(dest) + "/" + str(i))
            ):  # si le fichier dest est différent du fichier source
                timestampdest = os.stat(str(dest) + "/" + i)
                timestampsrc = os.stat(str(source) + "/" + i)
                if (
                    timestampsrc[8] > timestampdest[8]
                ):  # si le fichier source est plus récent que le fichier dest
                    # stat[8] donne le mtime cad le temps en seconde depuis lequel le fichier a été modifié. copyfile conserve cette propriété
                    goodcopy(dest, str(i))
                    # print(str(i))
            else:  # sinon on ajoute les fichiers identiques à une liste qui n'est pas utilise
                identique.append(i)
        else:  # si le fichier dest n'existe pas
            goodcopy(dest, str(i))
            # print(str(i))
    for j in b:
        if os.path.isdir(str(dest) + "/" + j):
            print(str(dest) + "/" + j + "existe ")
        else:
            mkdirs(str(dest) + "/" + j)
        recopier(str(source) + "/" + j, str(dest) + "/" + j)

def test_recopier():
    recopier('/Users/macbook/github/scraping','/Users/macbook')
    assert os.path.isfile('/Users/macbook/boxplot_scraping.png')==True
    assert os.path.isfile('/Users/macbook/README.md')==True
    assert os.path.isfile('/Users/macbook/scraping.py')==True

    
def chiffrer(source, dest):
    "la fonction chiffrer(source,dest) 7zippe avec chiffrement les fichiers du repertoire source ainsi que ses sous repertoire vers le repertoire dest s'ils n'existent pas ou s'ils sont plus recent (pr le meme nom)"
    a = listFiles(source)
    b = listFolders(source)
    timestampsrc = 0
    timestampdest = 0
    identique = []
    # print(a)
    for i in a:
        if os.path.isfile(
            str(dest) + "/" + i + ".7z"
        ):  # si le fichier dest existe en .7z
            timestampdest = os.stat(str(dest) + "/" + i + ".7z")
            timestampsrc = os.stat(str(source) + "/" + i)
            if (
                timestampsrc[8] > timestampdest[8]
            ):  # si le timestamp source est plus récent que celui du dest
                prgmrun = (
                    "7z a -mhe=on -pmdp "
                    + '"'
                    + str(dest)
                    + "/"
                    + str(i)
                    + ".7z"
                    + '"'
                    + ' "'
                    + str(i)
                    + '"'
                    + " -scrc SHA256 -stl"
                )
                os.system(prgmrun)  # ajouter un overwrite
            else:  # sinon on ajoute les fichiers identiques à une liste qui n'est pas utilise
                identique.append(i)
        else:  # si le fichier dest n'existe pas
            prgmrun = (
                "7z a -mhe=on -pmdp "
                + '"'
                + str(dest)
                + "/"
                + str(i)
                + ".7z"
                + '"'
                + ' "'
                + str(i)
                + '"'
                + " -scrc SHA256 -stl"
            )
            os.system(prgmrun)  # ajouter un overwrite
    for j in b:
        if os.path.isdir(str(dest) + "/" + j):
            print(
                str(dest)
                + "/"
                + j
                + " existe ou il y a eu un message d'erreur de copie"
            )
        else:
            mkdirs(str(dest) + "/" + j)

        chiffrer(str(source) + "/" + j, str(dest) + "/" + j)

def test_chiffrer():
    chiffrer('/Users/macbook/github/scraping','/Users/macbook')
    assert os.path.isfile('/Users/macbook/boxplot_scraping.png.7z')==True
    assert os.path.isfile('/Users/macbook/README.md.7z')==True
    assert os.path.isfile('/Users/macbook/scraping.py.7z')==True

        
def dechiffrer(source, dest):
    "la fonction dechiffrer(source,dest) utilise 7zipp pour extraire les archives du repertoire source et ses sous repertoires vers le repertoire dest s'ils n'existent pas ou s'ils sont plus recent (pr le meme nom)"
    a = listFiles(source)
    b = listFolders(source)
    timestampsrc = 0
    timestampdest = 0
    identique = []
    # print(a)
    for i in a:
        x = str(i)
        y = x.replace(".7z", " ")
        z = y.strip()  # stripping de i
        if os.path.isfile(str(dest) + "/" + z):  # si le fichier dest existe sans .7z
            timestampdest = os.stat(str(dest) + "/" + z)
            timestampsrc = os.stat(str(source) + "/" + i)
            if (
                timestampsrc[8] > timestampdest[8]
            ):  # si le timestamp source est plus récent que celui du dest
                prgmrun = (
                    "7z e "
                    + str(source)
                    + "/"
                    + '"'
                    + i
                    + '"'
                    + " -pmdp -o"
                    + str(dest)
                )
                os.system(prgmrun)
            else:  # sinon on ajoute les fichiers identiques à une liste qui n'est pas utilise
                identique.append(i)
        else:  # si le fichier dest n'existe pas
            prgmrun = (
                "7z e " + str(source) + "/" + '"' + i + '"' + " -pmdp -o" + str(dest)
            )
            os.system(prgmrun)
    for j in b:
        if os.path.isdir(str(dest) + "/" + j):
            print(
                str(dest)
                + "/"
                + j
                + " existe ou il y a eu un message d'erreur de copie"
            )
        else:
            os.mkdir(str(dest) + "/" + j)

        dechiffrer(str(source) + "/" + j, str(dest) + "/" + j)

def test_dechiffrer():
    chiffrer('/Users/macbook/github/scraping','/Users/macbook')
    dechiffrer('/Users/macbook','/Users/macbook/testdechiffrer')
    assert os.path.isfile('/Users/macbook/testdechiffrer/boxplot_scraping.png')==True
    assert os.path.isfile('/Users/macbook/testdechiffrer/README.md')==True
    assert os.path.isfile('/Users/macbook/testdechiffrer/scraping.py')==True
        

if __name__ == "__main__":
    a = dicoisation({}, "/home/user/Téléchargements")
    keys = list(a.keys())
    for i in keys:  # i est un repertoire
        if contain("brave", i):
            print(i)
            recopier(i, "/home/user/df")

