from functools import partial
import sys

COLORS = {
    'BLUE': '\033[94m',
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'PURPLE': '\033[95m',
    'YELLOW': '\033[93m',
    'ENDC': '\033[0m'
}

BOLD_COLORS = {
    'BLUE': '\033[1;34m',
    'RED': '\033[1;31m',
    'GREEN': '\033[1;32m',
    'YELLOW': '\033[1;33m',
    'WHITE': '\033[1;37m',
    'ENDC': '\033[0m'
}

def colored(d, color, s):
    return ''.join([d[color], s, d['ENDC']])


this = sys.modules[__name__]
for item in COLORS:
    if item == 'ENDC':
        continue

    setattr(this, item.lower(), partial(colored, COLORS, item))

for item in BOLD_COLORS:
    setattr(this, ''.join(['b', item.lower()]),
            partial(colored, BOLD_COLORS, item))

