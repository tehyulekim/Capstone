""r"""
https://docs.python.org/3/library/os.html

https://www.tutorialspoint.com/python/os_walk.htm

os.path.dirname('a/b/c/d') =  a/b/c
os.path.basename('a/b/c/d') =  d




"""

import os

for x in os.walk('.'):
    print(x)

print()

for root, dirs, files in os.walk('.'):
    print("<root = ", root, ">  <dirs = ", dirs, " > <files = ", files)

for root, dirs, files in os.walk("."):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))


print("os.path.dirname('a/b/c/d') = ", os.path.dirname('a/b/c/d'))
print("os.path.basename('a/b/c/d') = ", os.path.basename('a/b/c/d'))
