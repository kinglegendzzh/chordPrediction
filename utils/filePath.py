import os

def filePath(fileDir):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), fileDir)