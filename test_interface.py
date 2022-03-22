#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
this is test_interface.py
tests of interface functions
"""
import os
from sync import Sync


def test_cypher():
    "test of cypher function"
    for folder in range(3):
        os.makedirs(f'./testfolder/{folder}')
    os.makedirs('./testfolder2')
    for file in range(4, 6):
        with open(f'./testfolder/2/{file}.txt', 'w',
                  encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./testfolder', './testfolder2').cypher('pw')
    for folder in range(3):
        assert os.path.isdir(f'./testfolder2/{folder}')
    for file in range(4, 6):
        assert os.path.isfile(f'./testfolder2/2/{file}.txt.7z')
    for file in range(4, 6):
        os.remove(f'./testfolder/2/{file}.txt')
        os.remove(f'./testfolder2/2/{file}.txt.7z')
    for folder in range(3):
        os.rmdir(f'./testfolder/{folder}')
        os.rmdir(f'./testfolder2/{folder}')
    os.rmdir('./testfolder')
    os.rmdir('./testfolder2')


def test_decypher():
    "test of decypher function"
    for folder in range(3):
        os.makedirs(f'./testfolder/{folder}')
    os.makedirs('./testfolder2')
    os.makedirs('./testfolder0')
    for file in range(4, 6):
        with open(f'./testfolder/2/{file}.txt', 'w',
                  encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./testfolder', './testfolder2').cypher('pw')
    Sync('./testfolder2', './testfolder0').decypher('pw')
    for folder in range(3):
        assert os.path.isdir(f'./testfolder0/{folder}')
    for file in range(4, 6):
        assert os.path.isfile(f'./testfolder0/2/{file}.txt')
    for file in range(4, 6):
        os.remove(f'./testfolder/2/{file}.txt')
        os.remove(f'./testfolder2/2/{file}.txt.7z')
        os.remove(f'./testfolder0/2/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./testfolder/{folder}')
        os.rmdir(f'./testfolder2/{folder}')
        os.rmdir(f'./testfolder0/{folder}')
    os.rmdir('./testfolder')
    os.rmdir('./testfolder2')
    os.rmdir('./testfolder0')


def test_copy():
    "test of copy function"
    for folder in range(3):
        os.makedirs(f'./testfolder/{folder}')
    os.makedirs('./testfolder2')
    for file in range(4, 6):
        with open(f'./testfolder/2/{file}.txt', 'w',
                  encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./testfolder', './testfolder2').copy()
    for folder in range(3):
        assert os.path.isdir(f'./testfolder2/{folder}')
    for file in range(4, 6):
        assert os.path.isfile(f'./testfolder2/2/{file}.txt')
    for file in range(4, 6):
        os.remove(f'./testfolder/2/{file}.txt')
        os.remove(f'./testfolder2/2/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./testfolder/{folder}')
        os.rmdir(f'./testfolder2/{folder}')
    os.rmdir('./testfolder')
    os.rmdir('./testfolder2')


def test_choose1():
    "test of choose with simple copy"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./2', './1').choose('', '')
    for file in range(4, 6):
        assert os.path.isfile(f'1/{file}.txt')
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_choose2():
    "test of choose function with cypher"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./2', './1').choose('pw', '')
    for file in range(4, 6):
        assert os.path.isfile(f'1/{file}.txt.7z')
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_choose3():
    "test of choose function with decypher"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./2', './1').choose('pw', '')
    Sync('./1', './0').choose('', 'pw')
    for file in range(4, 6):
        assert os.path.isfile(f'0/{file}.txt')
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
        os.remove(f'0/{file}.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_choose4():
    "test of choose function copy with keyword"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./2', './1').choose('pw', '')
    Sync('./1', './0', keyword='4').choose('', '')
    assert os.path.isfile('./0/4.txt.7z')
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
    os.remove('./0/4.txt.7z')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_choose5():
    "test of choose cypher with keyword"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./2', './1', keyword='4').choose('pw', '')
    assert os.path.isfile('1/4.txt.7z')
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
    os.remove('1/4.txt.7z')
    for folder in range(3):
        os.rmdir(f'./{folder}')


def test_choose6():
    "test of choose function decypher with keyword"
    for folder in range(3):
        os.makedirs(f'./{folder}')
    for file in range(4, 6):
        with open(f'2/{file}.txt', 'w', encoding='utf-8') as fileo:
            fileo.write(f'testfile{file}')
    Sync('./2', './1').choose('pw', '')
    Sync('./1', './0', keyword='4').choose('', 'pw')
    assert os.path.isfile('0/4.txt')
    for file in range(4, 6):
        os.remove(f'2/{file}.txt')
        os.remove(f'1/{file}.txt.7z')
    os.remove('0/4.txt')
    for folder in range(3):
        os.rmdir(f'./{folder}')
