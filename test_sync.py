#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is test_sync.py
"""
import os
import filecmp
from sync import Sync


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
