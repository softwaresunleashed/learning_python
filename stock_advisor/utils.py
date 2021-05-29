
from config import *



def AddDirectory():
    import os
    path = ROOT_PATH
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)


def RemoveDirectory():
    import shutil
    path = ROOT_PATH

    try:
        shutil.rmtree(path)
    except OSError:
        print("Deletion of the directory %s failed" % path)
    else:
        print("Successfully deleted the directory %s" % path)