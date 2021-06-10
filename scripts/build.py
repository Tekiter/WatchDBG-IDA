# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os
import re

from shutil import copyfile, rmtree

SOURCE_PATTERN = r'.+.py$'


def build(src_dir, dist_dir):
    move_to_root_path()
    clean_dir(dist_dir)
    create_dir(dist_dir)

    copy_files(src_dir, dist_dir)


def clean_dir(dir_path):
    if os.path.isdir(dir_path):
        rmtree(dir_path)


def create_dir(dir_path):
    path = dir_path
    try:
        os.mkdir(path)
    except OSError:
        if not os.path.isdir(path):
            raise OSError('Creating directory "{}" failed.'.join(dir_path))


def move_to_root_path():
    os.chdir(get_root_path())


def get_root_path():
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    parent_dir_path = os.path.dirname(current_dir_path)

    return parent_dir_path


def copy_files(src_dir, dist_dir):
    for dir, filename in source_files(src_dir):

        target_dir = source_path_to_target_dir(dir, src_dir, dist_dir)

        src_path = os.path.join(dir, filename)
        target_path = os.path.join(target_dir, filename)

        create_dir(target_dir)
        copyfile(src_path, target_path)

        print("{} >> {}".format(src_path, target_path))


def source_files(src_dir):
    pattern = re.compile(SOURCE_PATTERN)
    for dir, _, files in os.walk(src_dir):
        for filename in files:
            if pattern.match(filename):
                yield (dir, filename)


def source_path_to_target_dir(source_path, src_dir, dist_dir):
    frag_dir = get_path_without_head_dir(source_path, src_dir)
    return os.path.join(dist_dir, frag_dir)


def get_path_without_head_dir(path, head):
    return path[len(head)+1:]


if __name__ == '__main__':
    build('src', 'dist')
