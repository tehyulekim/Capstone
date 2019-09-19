""""""r"""
$ python fire1.py f1 stnw
Hello stnw!

$ python fire1.py f2 111 222 333
111 222 333

"""

import fire


def f1(x):
    return 'Hello {name}!'.format(name=x)


def f2(p1, p2, p3):
    return '{} {} {}'.format(p1, p2, p3)


if __name__ == '__main__':
    fire.Fire()
