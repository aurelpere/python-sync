#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is test_staticfunctions.py
"""
import os
import time
import shutil
from static import Static


def test_tildexpand():
    "test of tildexpand function"
    assert os.path.expanduser('~/') in Static.tildexpand('~/blab/bla')


def test_findkeyword():
    "test of findkeyword function"
    assert Static.findkeyword('this is a chain', 'chain') == True


def test_listfileskw():
    "test of listfileskw function"
    os.makedirs('./1')
    for file in range(3):
        with open(f'./1/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    assert sorted(Static.listfileskw('./1')) == ['0.txt', '1.txt', '2.txt']
    assert sorted(Static.listfileskw('./1', '1.txt')) == ['1.txt']
    for file in range(3):
        os.remove(f'./1/{file}.txt')
    os.rmdir('./1')


def test_listfolders():
    "test of listfolders function"
    for folder in range(3):
        os.makedirs(f'{folder}')
    assert all(x in Static.listfolders('.') for x in ['0', '1', '2'])
    for folder in range(3):
        os.rmdir(f'{folder}')


def test__pythoncopyfile():
    "test of pythoncopyfile function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
        Static.pythoncopyfile(f'2/{file}.txt', f'1/{file}.txt')
        assert os.path.isfile(f'1/{file}.txt') is True
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_decorated_copyfile():
    "test of copyfile function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
        Static.copyfile('2', '1', f'{file}.txt')
        assert os.path.isfile(f'1/{file}.txt') is True
    time.sleep(3)
    with open('0/4.txt', 'w', encoding='utf-8') as fileo:
        fileo.write('testfiletestfile')
    shutil.copy2('2/5.txt', '0/5.txt')  # 5 same timestamp
    Static.copyfile('0', '1', '4.txt')
    assert os.stat('1/4.txt')[8] > os.stat('2/4.txt')[8]
    Static.copyfile('0', '1', '5.txt')
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
        Static.copyfile.__wrapped__('2', '1', f'{file}.txt')
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
        Static.copyfilec('2', '1', f'{file}.txt', 'pw')
        assert os.path.isfile(f'1/{file}.txt.7z') is True
    storedtimestamp4 = os.stat('1/4.txt.7z')[8]
    storedtimestamp5 = os.stat('1/5.txt.7z')[8]
    time.sleep(1)
    shutil.copy('2/4.txt', '0/4.txt')  # 4 more recent
    shutil.copy2('2/5.txt', '0/5.txt')  # 5 same timestamp
    Static.copyfilec('0', '1', '4.txt', 'pw')
    assert os.stat('1/4.txt.7z')[8] > storedtimestamp4
    Static.copyfilec('0', '1', '5.txt', 'pw')
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
        Static.copyfilec('2', '1', f'{file}.txt', 'pw')
        Static.copyfiled('1', '0', f'{file}.txt.7z', 'pw')
        assert os.path.isfile(f'0/{file}.txt') is True
    storedtimestamp4 = os.stat('0/4.txt')[8]
    storedtimestamp5 = os.stat('0/5.txt')[8]
    time.sleep(1)
    with open('2/4.txt', 'w', encoding='utf-8') as fileo:
        fileo.write('testfiletestfile')
    Static.copyfilec('2', '1', '4.txt', 'pw')  # 4 more recent
    Static.copyfiled('1', '0', '4.txt.7z', 'pw')
    assert os.stat('0/4.txt')[8] > storedtimestamp4
    Static.copyfiled('1', '0', '5.txt.7z', 'pw')
    assert os.stat('0/5.txt')[8] == storedtimestamp5
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
        os.remove(f'0/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')
