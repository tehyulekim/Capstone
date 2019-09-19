import argparse

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("x", type=int, help="the base")
parser.add_argument("-v", "--verbosity", action="count", default=0)
args = parser.parse_args()


def f1():
    print(111)

def f2():
    print(222)


if args.x == 1:
    f1()
if args.x == 2:
    f2()
