import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
rootdir = os.path.dirname(os.path.dirname(currentdir))
srcdir = os.path.join(rootdir, 'src')
sys.path.insert(0, srcdir)


def import_src(name):

    return __import__(name)
