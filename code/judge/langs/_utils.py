import sys
import importlib

def args(mandatory_number):
    if len(sys.argv) != mandatory_number + 1:
        # Not enough arguments, program exits here.
        sys.exit(0)

    return sys.argv[1:]


def load(lang):
    return importlib.import_module('langs.%s' % lang).lang
