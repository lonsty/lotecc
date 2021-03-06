import os
import re
from fnmatch import fnmatch

from opencc import OpenCC
from pydantic import BaseModel, validator


def check_file_exist(filename: str) -> str:
    """
    Check if the file exists in the current directory or the upper directories.

    :param filename: str, the filename.
    :return: str, a abspath of the file if exist, else a empty string.
    """
    if os.path.isfile(filename):
        return os.path.abspath(filename)
    else:
        dirs = os.path.split(os.getcwd())
        for i in range(len(dirs), 0, -1):
            full_path = os.path.join(*dirs[:i], filename)
            if os.path.isfile(full_path):
                return full_path
    return ''


def read_ignores(ignore_file: str) -> list:
    """
    Read ignore patterns from a .gitignore syntax file.

    :param ignore_file: str, the ignore file, may not be the correct path.
    :return: list, the ignore patterns.
    """

    ignore_file_path = check_file_exist(ignore_file)
    if not ignore_file_path:
        return []

    with open(ignore_file_path, 'r') as f:
        lines = f.readlines()

    pt = re.compile(r'\S')
    ignores = [l.strip().replace('/', '') for l in lines
               if pt.match(l) and not l.strip().startswith('#')]
    ignores.append('.git')

    return ignores


def get_list_of_files(dir_name: str, ignores: list) -> list:
    """
    Get all files in a directory excluding ignored files.

    :param dir_name: str, the root directory.
    :param ignores: str, the patterns to exclude.
    :return: list, the files excluding ignored files.
    """
    list_of_file = os.listdir(dir_name)
    all_files = []

    for entry in list_of_file:
        full_path = os.path.abspath(os.path.join(dir_name, entry))
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
    input: str = '.'
    output: str = None
    in_enc: str = 'utf-8'
    out_enc: str = 'utf-8'
    suffix: str = None
    ignore: str = '.gitignore'

    @property
    def ignore_patterns(self) -> list:
        """
        Read ignore patterns from file, or get from input string.

        :return: list, the .gitignore syntax patterns.
        """
        return read_ignores(self.ignore) or self.ignore.split(',')

    @property
    def input_files(self) -> list:
        """
        List files filtered by ignore patterns in the input directory,
    or a input file.

        :return: list, the files to convert.
        """
        if os.path.isdir(self.input):
            return get_list_of_files(self.input, self.ignore_patterns)
        elif os.path.isfile(self.input):
            return [os.path.abspath(self.input)]
        else:
            raise ValueError(f'<{self.input}> is not a file or directory')

    @validator('conversion')
    def valid_conversion(cls, v: str) -> str:
        """
        Validate argument of conversion.

        :param v: str, the value of conversion.
        :return: str, the valid value of conversion.
        :raise: raise a ValueError if conversion is not supported.
        """
        if v.lower() in ['hk2s', 's2hk', 's2t', 's2tw', 's2twp',
                         't2hk', 't2s', 't2tw', 'tw2s', 'tw2sp']:
            return v.lower()
        else:
            raise ValueError(f'Error: conversion <{v}> not support')


def lote_chinese_conversion(**kwargs):
    """
    Convert files between Simplified Chinese and Traditional Chinese.

    :param conversion: str, default 's2t', the conversion method.
    :param input: str, default '.', an input file or a directory.
    :param output: str, default None, an output file or a directory.
    :param in_enc: str, default 'utf-8', encoding for input.
    :param out_enc: str, default 'utf-8', encoding for output.
    :param suffix: str, default None, suffix of output filename.
    :param ignore: str, default '.gitignore', a .gitignore syntax file,
                   or patterns, separated by commas.
    :return: list, list of tuples, a tuple contains source file and
             converted file.
    """
    config = LoteccConfig(**kwargs)
    cc = OpenCC(config.conversion)
    converted = []

    for input_file in config.input_files:
        try:
            with open(input_file, encoding=config.in_enc) as f:
                input_str = f.read()
        except UnicodeDecodeError:
            continue

        output_str = cc.convert(input_str)

        output_file = input_file

        if config.output:
            if os.path.isdir(config.output):
                output_file = os.path.abspath(
                    os.path.join(config.output,os.path.basename(input_file)))
            else:
                output_file = os.path.abspath(config.output)

        if config.suffix:
            name, extension = os.path.splitext(output_file)
            output_file = name + config.suffix + extension

        if output_str == input_str:
            continue

        with open(output_file, 'w', encoding=config.out_enc) as f:
            f.write(output_str)
            converted.append((input_file, output_file))

    return converted
