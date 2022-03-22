#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is test_sync.py
"""
import os
import time
import shutil
import filecmp
from sync import Sync


def test_decorated_copyfile():
    "test of copyfile function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
        Sync('2', '1').copyfile('2', '1', f'{file}.txt')
        assert os.path.isfile(f'1/{file}.txt') is True
    time.sleep(3)
    with open(f'0/4.txt', 'w', encoding='utf-8') as fileo:
        fileo.write(f'testfiletestfile')
    shutil.copy2('2/5.txt', '0/5.txt')  # 5 same timestamp
    Sync('0', '1').copyfile('0', '1', '4.txt')
    assert os.stat('1/4.txt')[8] > os.stat('2/4.txt')[8]
    Sync('0', '1').copyfile('0', '1', '5.txt')
    assert os.stat('1/5.txt')[8] == os.stat('2/5.txt')[8]
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt')
        os.remove(f'0/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_undecorated_copyfile():
    "test of undecorated copyfile function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
        sync = Sync('2', '1')
        sync.copyfile.__wrapped__('2', '1', f'{file}.txt')
        assert os.path.isfile(f'1/{file}.txt') is True
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_decorated_copyfilec():
    "test of copyfilec function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
        Sync('2', '1').copyfilec('2', '1', f'{file}.txt', 'pw')
        assert os.path.isfile(f'1/{file}.txt.7z') is True
    storedtimestamp4 = os.stat('1/4.txt.7z')[8]
    storedtimestamp5 = os.stat('1/5.txt.7z')[8]
    time.sleep(1)
    shutil.copy('2/4.txt', '0/4.txt')  # 4 more recent
    shutil.copy2('2/5.txt', '0/5.txt')  # 5 same timestamp
    Sync('0', '1').copyfilec('0', '1', '4.txt', 'pw')
    assert os.stat('1/4.txt.7z')[8] > storedtimestamp4
    Sync('0', '1').copyfilec('0', '1', '5.txt', 'pw')
    assert os.stat('1/5.txt.7z')[8] == storedtimestamp5
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
        os.remove(f'0/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_decorated_copyfiled():
    "test of copyfiled function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
        Sync('2', '1').copyfilec('2', '1', f'{file}.txt', 'pw')
        Sync('1', '0').copyfiled('1', '0', f'{file}.txt.7z', 'pw')
        assert os.path.isfile(f'0/{file}.txt') is True
    storedtimestamp4 = os.stat('0/4.txt')[8]
    storedtimestamp5 = os.stat('0/5.txt')[8]
    time.sleep(1)
    with open(f'2/4.txt', 'w', encoding='utf-8') as fileo:
        fileo.write(f'testfiletestfile')
    Sync('2', '1').copyfilec('2', '1', f'4.txt', 'pw')  # 4 more recent
    Sync('1', '0').copyfiled('1', '0', '4.txt.7z', 'pw')
    assert os.stat('0/4.txt')[8] > storedtimestamp4
    Sync('1', '0').copyfiled('1', '0', '5.txt.7z', 'pw')
    assert os.stat('0/5.txt')[8] == storedtimestamp5
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
        os.remove(f'0/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_copyfolder():
    "test of copyfolder function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    os.makedirs('./2/22')
    for file in range(4, 6):
        with open(f'./2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    with open('./2/22/22.txt', 'w', encoding='utf-8') as filesub:
        filesub.write('testfile22')
    Sync('2', '1').copyfolders('./2', './1')
    for file in range(4, 6):
        assert os.path.isfile(f'./1/{file}.txt') is True
    assert os.path.isdir('./1/22')
    assert os.path.isfile('./1/22/22.txt')
    os.remove('./2/22/22.txt')
    os.remove('./1/22/22.txt')
    for file in range(4, 6):
        os.remove(f'./2/{file}.txt')
        os.remove(f'./1/{file}.txt')
    os.rmdir('./1/22')
    os.rmdir('./2/22')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_cypherfolders():
    "test of chiffrer function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('2', '1', keyword=4).cypherfolders('./2', './1', password='pw')
    assert os.path.isfile('./1/4.txt.7z') is True
    Sync('2', '1').cypherfolders('./2', './1', password='pw')
    assert os.path.isfile('./1/4.txt.7z') is True
    assert os.path.isfile('./1/5.txt.7z') is True
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_decypherfolders():
    "test of dechiffrer function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    with open('2/blabla.txt', 'w', encoding='utf-8') as filbla:
        filbla.write('testfileblabla')
    Sync('2', '1').cypherfolders('./2', './1', password='pw')
    Sync('1', '0', keyword='bla').decypherfolders('./1', './0', password='pw')
    assert filecmp.cmp('./2/blabla.txt', './0/blabla.txt') is True
    Sync('1', '0').decypherfolders('./1', './0', password='pw')
    for file in range(4, 6):
        assert filecmp.cmp(f'./2/{file}.txt', f'./0/{file}.txt') is True
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
        os.remove(f'0/{file}.txt')
    os.remove('./2/blabla.txt')
    os.remove('./1/blabla.txt.7z')
    os.remove('./0/blabla.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_tildexpand():
    "test of tildexpand function"
    assert os.path.expanduser('~/') in Sync.tildexpand('~/blab/bla')


if __name__ == "__main__":
    os.makedirs('1')
    os.makedirs('2')
    with open('2/testfile.txt', 'w') as fileopen:
        fileopen.write('this is a test file')

    def f(src, dst, file):
        shutil.copy(f'{src}/{file}', f'{dst}/{file}')

    a = Sync('2', '1').fileprocessing(f('2', '1', 'testfile.txt'))
    print(a)
