#!/usr/bin/env python3

#
# a quick but useful hack to diff similar JSON files, e.g.
# once they have gone through some sort of transformation
#

from itertools import zip_longest
import json
import sys


def load_json(path):
    with open(path) as fd:
        return json.load(fd)


def diff_vals(descr, v1, v2, context=[]):
    if v1 == v2:
        return
    elif type(v1) is dict and type(v2) is dict:
        diff_dict(v1, v2, context)
    elif type(v1) is list and type(v2) is list:
        diff_list(v1, v2, context)
    else:
        print('- {}{}: {}'.format(' '.join(context), descr, repr(v1)))
        print('+ {}{}: {}'.format(' '.join(context), descr, repr(v2)))


def diff_dict(a, b, context=[]):
    all_keys = set(a.keys()) | set(b.keys())
    for key in sorted(all_keys):
        if key not in a:
            print('+ {}{}: {}'.format(' '.join(context), key, repr(b[key])))
        elif key not in b:
            print('- {}{}: {}'.format(' '.join(context), key, repr(a[key])))
        else:
            diff_vals(key, a[key], b[key], context + ['{}:'.format(key)])


def diff_list(a, b, context=''):
    for idx, (e1, e2) in enumerate(zip_longest(a, b)):
        diff_vals('[{}]'.format(idx), e1, e2, context + ['[{}]'.format(idx)])


if __name__ == '__main__':
    a = load_json(sys.argv[1])
    b = load_json(sys.argv[2])
    diff_dict(a, b)
