#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is test_staticfunctions.py
"""
import os
from sync import Sync


def test_mkdirs():
    "test of mkdirs function"
    Sync.mkdirs('testfolder')
    assert os.path.isdir('testfolder') is True
    os.rmdir('testfolder')


def test_listfileskw():
    "test of listfileskw function"
    os.makedirs('./1')
    for file in range(3):
        with open(f'./1/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    assert sorted(Sync.listfileskw('./1')) == ['0.txt', '1.txt', '2.txt']
    assert sorted(Sync.listfileskw('./1', '1.txt')) == ['1.txt']
    for file in range(3):
        os.remove(f'./1/{file}.txt')
    os.rmdir('./1')


def test_listfolders():
    "test of listfolders function"
    for folder in range(3):
        os.makedirs(f'{folder}')
    assert all(x in Sync.listfolders('.') for x in ['0', '1', '2'])
    for folder in range(3):
        os.rmdir(f'{folder}')


def test__pythoncopyfile():
    "test of pythoncopyfile function"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
        Sync.pythoncopyfile(f'2/{file}.txt', f'1/{file}.txt')
        assert os.path.isfile(f'1/{file}.txt') is True
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')
