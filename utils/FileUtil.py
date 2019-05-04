from os import listdir, getcwd
from os.path import isfile, join

def getFutureList(folderName):
    cwd = getcwd()
    mypath = cwd + '/' + folderName
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    futureFiles = list(filter(lambda x: x[-6:]=='F1.txt', onlyfiles))
    return map(lambda x:x[:-4], futureFiles)
