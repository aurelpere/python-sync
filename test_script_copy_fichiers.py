#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is test_script_copy_fichiers.py
"""
import os
import filecmp
from script_copy_fichiers import mkdirs
from script_copy_fichiers import listfolders
from script_copy_fichiers import listfileskw
from script_copy_fichiers import dico_maker
from script_copy_fichiers import recopier
from script_copy_fichiers import pythoncopy
from script_copy_fichiers import chiffrer
from script_copy_fichiers import dechiffrer
from script_copy_fichiers import script_copy_fichiers

def test_mkdirs():
    "test of mkdirs function"
    mkdirs('testfolder')
    assert os.path.isdir('testfolder') is True
    os.rmdir('testfolder')

def test_listfileskw():
    "test of listfileskw function"
    os.makedirs('./1')
    for file in range(3):
        with open(f'./1/{file}.txt','w',encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    assert sorted(listfileskw('./1'))==['0.txt','1.txt','2.txt']
    assert sorted(listfileskw('./1','1.txt')) == ['1.txt']
    for file in range(3):
        os.remove(f'./1/{file}.txt')
    os.rmdir('./1')
def test_listfolders():
    "test of listfolders function"
    for folder in range(3):
        os.makedirs(f'{folder}')
    assert all(x in listfolders('.') for x in ['0','1', '2'])
    for folder in range(3):
        os.rmdir(f'{folder}')

def test_dico_maker():
    "test of dico_maker function"
    for folder in range(3):
        os.makedirs(f'./testfolder/{folder}')
    for file in range(4,6):
        with open(f'./testfolder/2/{file}.txt', 'w',encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    assert dico_maker('./testfolder')=={'./testfolder':[],'./testfolder/0':[],'./testfolder/1':[],'./testfolder/2':['5.txt','4.txt']}
    for file in range(4,6):
        os.remove(f'./testfolder/2/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./testfolder/{folder}')
    os.rmdir('./testfolder')
def test_recopier():
    "test of recopier function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    os.makedirs('./2/22')
    for file in range(4,6):
        with open(f'./2/{file}.txt', 'w',encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    with open('./2/22/22.txt','w',encoding='utf-8') as filesub:
        filesub.write('testfile22')
    recopier('./2','./1')
    for file in range(4, 6):
        assert os.path.isfile(f'./1/{file}.txt') is True
    assert os.path.isdir('./1/22')
    assert os.path.isfile('./1/22/22.txt')
    os.remove('./2/22/22.txt')
    os.remove('./1/22/22.txt')
    for file in range(4,6):
        os.remove(f'./2/{file}.txt')
        os.remove(f'./1/{file}.txt')
    os.rmdir('./1/22')
    os.rmdir('./2/22')
    for folder in range(3):
        os.rmdir(f'./{folder}')

def test_chiffrer():
    "test of chiffrer function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4,6):
        with open(f'2/{file}.txt', 'w',encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    chiffrer('./2','./1',keyword=4,password='pw')
    assert os.path.isfile('./1/4.txt.7z') is True
    chiffrer('./2', './1', password='pw')
    assert os.path.isfile('./1/4.txt.7z') is True
    assert os.path.isfile('./1/5.txt.7z') is True
    for file in range(4,6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
    for folder in range(3):
        os.rmdir(f'./{folder}')

def test_dechiffrer():
    "test of dechiffrer function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4,6):
        with open(f'2/{file}.txt', 'w',encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    with open('2/blabla.txt', 'w', encoding='utf-8') as filbla:
        filbla.write('testfileblabla')
    chiffrer('./2', './1', password='pw')
    dechiffrer('./1','./0',password='pw',keyword='bla')
    assert filecmp.cmp('./2/blabla.txt','./0/blabla.txt') is True
    dechiffrer('./1', './0', password='pw')
    for file in range(4,6):
        assert filecmp.cmp(f'./2/{file}.txt',f'./0/{file}.txt') is True
    for file in range(4,6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
        os.remove(f'0/{file}.txt')
    os.remove('./2/blabla.txt')
    os.remove('./1/blabla.txt.7z')
    os.remove('./0/blabla.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')

def test_pythoncopy():
    "test of pythoncopy function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4,6):
        with open(f'2/{file}.txt', 'w',encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
        pythoncopy(f'2/{file}.txt',f'1/{file}.txt')
        assert os.path.isfile(f'1/{file}.txt') is True
    for file in range(4,6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')
def test_script_copy_fichiers():
    "test of script_copy_fichiers function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4,6):
        with open(f'2/{file}.txt', 'w',encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    script_copy_fichiers('./2','./1')
    script_copy_fichiers('./2', './1',cypher='pw')
    for file in range(4,6):
        assert os.path.isfile(f'1/{file}.txt')
        assert os.path.isfile(f'1/{file}.txt.7z')
    script_copy_fichiers('./1', './0',decypher='pw')
    for file in range(4, 6):
        assert os.path.isfile(f'0/{file}.txt')
    script_copy_fichiers('./1', './0', keyword='4')
    assert os.path.isfile('./0/4.txt.7z')
    for file in range(4,6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
        os.remove(f'0/{file}.txt')
    os.remove('./0/4.txt.7z')
    for folder in range(3):
        os.rmdir(f'./{folder}')
