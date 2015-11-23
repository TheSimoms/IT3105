import sys

sys.path.append('../../')

from modules.module_five.mnist import mnist_basics


def major_demo(ann, r, d):
    return mnist_basics.minor_demo(ann)
