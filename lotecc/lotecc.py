"""Main module."""
import os
import re
from fnmatch import fnmatch

from opencc import OpenCC
from pydantic import BaseModel, validator


def check_file_exist(filename):
    dirs = os.path.split(os.getcwd())
    for i in range(len(dirs), 0, -1):
        full_path = os.path.join(*dirs[:i], filename)
        if os.path.isfile(full_path):
            return full_path
    return False


def read_ignores(ignore_file='.gitignore'):
    ignore_file_path = check_file_exist(ignore_file)
    if not ignore_file_path:
        # print(f'Warning: file <{ignore_file}> does not exist')
        return []

    with open(ignore_file_path, 'r') as f:
        lines = f.readlines()

    pt = re.compile(r'\S')
    ignores = [l.strip().replace('/', '') for l in lines if pt.match(l) and not l.strip().startswith('#')]
    ignores.append('.git')

    return ignores


def get_list_of_files(dir_name, ignores):
    # create a list of file and sub directories
    # names in the given directory
    list_of_file = os.listdir(dir_name)
    all_files = []
    # Iterate over all the entries
    for entry in list_of_file:
        # Create full path
        # full_path = os.path.join(dir_name, entry)
        full_path = os.path.abspath(os.path.join(dir_name, entry))
        # If entry is a directory then get the list of files in this directory
        for pattern in ignores:
            if fnmatch(os.path.split(full_path)[-1], pattern):
                break
        else:
            if os.path.isdir(full_path):
                all_files = all_files + get_list_of_files(full_path, ignores)
            else:
                all_files.append(full_path)

    return all_files


class LoteccConfig(BaseModel):
    conversion: str = 's2t'
    input_: str = '.'
    output: str = None
    in_enc: str = 'UTF-8'
    out_enc: str = 'UTF-8'
    suffix: str = None
    ignore: str = None

    @property
    def ignore_patterns(self):
        return read_ignores(self.ignore) or self.ignore.split(',')

    @property
    def input_files(self):
        if os.path.isdir(self.input_):
            print(self.ignore_patterns)
            return get_list_of_files(self.input_, self.ignore_patterns)
        elif os.path.isfile(self.input_):
            return [os.path.abspath(self.input_)]
        else:
            raise ValueError(f'<{self.input_}> is not a file or directory')


    @validator('conversion')
    def valid_conversion(cls, v):
        if v.lower() in ['hk2s', 's2hk', 's2t', 's2tw', 's2twp', 't2hk', 't2s', 't2tw', 'tw2s', 'tw2sp']:
            return v.lower()
        else:
            raise ValueError(f'Error: conversion <{v}> not support')


def lote_chinese_conversion(**kwargs):
    config = LoteccConfig(**kwargs)
    cc = OpenCC(config.conversion)

    for file in config.input_files:
        with open(file, encoding=config.in_enc) as f:
            input_str = f.read()

        output_str = cc.convert(input_str)

        output_file = file

        if config.output:
            if os.path.isdir(config.output):
                output_file = os.path.abspath(os.path.join(config.output, os.path.basename(file)))
            else:
                output_file = os.path.abspath(config.output)

        if config.suffix:
            name, extension = os.path.splitext(output_file)
            output_file = name + config.suffix + extension

        if output_str == input_str and output_file == file:
            continue

        with open(output_file, 'w', encoding=config.out_enc) as f:
            f.write(output_str)
