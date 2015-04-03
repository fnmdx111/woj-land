import sys
import importlib
import os

def args(mandatory_number):
    if len(sys.argv) != mandatory_number + 1:
        # Not enough arguments, program exits here.
        sys.exit(0)

    return sys.argv[1:]


def load(lang):
    return importlib.import_module('langs.%s' % lang).lang

def list_langs(dir_):
    for module in os.listdir(dir_):
        if (module not in ['__init__.py', '_fundamental.py',
                           '_utils.py', 'colors.py']
        and module.endswith('.py')):
            if module.endswith('rf.py'):
                continue

            yield module

