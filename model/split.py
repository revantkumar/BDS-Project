import os
import shutil
import random
from random import shuffle

random.seed()

DATA = "data"


def cleanup(d):
    assert d != DATA
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))


def copy(d, flist):
    for f in flist:
        print "Copying {} to {}".format(f, d)
        shutil.copyfile(os.path.join(DATA, f), os.path.join(d, f))

dirs = {"train":  0.7, "dev": 0.2, "test": 0.1}

for d in dirs:
    cleanup(d)

files = []

for f in os.listdir(DATA):
    files.append(f)

shuffle(files)
start = 0

for d, p in dirs.iteritems():
    end = start + int(p*len(files))
    copy(d, files[start:end])
    start = end
