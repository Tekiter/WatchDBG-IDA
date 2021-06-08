# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os
import re


def build(src_dir, dist_dir):
    move_to_root_path()
    create_dist_dir(dist_dir)

    # src = os.path.join(root, src_dir)
    # dist = os.path.join(root, dist_dir)

    pattern = re.compile(r'.+.py$')
    for root, _, files in os.walk(src_dir):
        for f in files:
            if pattern.match(f):
                print(root, f)


def create_dist_dir(dist_dir):
    path = dist_dir
    try:
        os.mkdir(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def get_root_path():
    current_dir_path = os.path.dirname(__file__)
    parent_dir_path = os.path.dirname(current_dir_path)

    return parent_dir_path


def move_to_root_path():
    os.chdir(get_root_path())


def get_source_files():
    pattern = 'src/**/*.py'
    files = glob.glob(pattern, recursive=True)
    return files


if __name__ == '__main__':
    build('src', 'dist')
