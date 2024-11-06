import ujson as json
import os
import posixpath
import unicodedata
import string
import shutil
import time
from debiaiServer.debiai_gui_utils import data_folder_path

DATA_PATH = data_folder_path + "/pythonDataProvider/"

DATA_TYPES = ["groundTruth", "contexts", "inputs", "others"]


# Init, called at the server start
def init():
    # Create the folder if it does not exist
    if not os.path.exists(DATA_PATH):
        os.mkdir(DATA_PATH)


# File name verifications
def clean_filename(filename):
    # replace spaces
    filename = filename.replace(" ", "_")

    # keep only valid ascii chars
    cleaned_filename = (
        unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore").decode()
    )

    # keep only whitelisted chars
    whitelist = "_-() %s%s" % (string.ascii_letters, string.digits)
    char_limit = 255

    cleaned_filename = "".join(c for c in cleaned_filename if c in whitelist)
    return cleaned_filename[:char_limit]


def is_filename_clean(filename):
    cleanFilename = "".join(i for i in filename if i not in "\/:*?<>|")  # noqa
    return filename == cleanFilename


def is_secure_path(path):
    path = posixpath.normpath(path)
    return not path.startswith(("/", "../"))


# directories and file Manipulation
def fileExist(path):
    return os.path.isfile(path)


def listDir(path):
    # List the directories only
    return [
        name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))
    ]


def deleteFile(filePath):
    os.remove(filePath)


def deleteDir(dirPath):
    deleteFiles = []
    deleteDirs = []
    for root, dirs, files in os.walk(dirPath):
        for f in files:
            deleteFiles.append(os.path.join(root, f))
        for d in dirs:
            deleteDirs.append(os.path.join(root, d))
    for f in deleteFiles:
        os.remove(f)
    for d in deleteDirs:
        os.rmdir(d)
    os.rmdir(dirPath)


def copyDir(src, dest):
    shutil.copytree(src, dest)


# Json files
def readJsonFile(path):
    with open(path, "r") as jsonFile:
        return json.load(jsonFile)


def writeJsonFile(path, obj):
    with open(path, "w") as outfile:
        json.dump(obj, outfile)


def updateJsonFile(path, key, data):
    with open(path, "r") as jsonFile:
        d = json.load(jsonFile)

    d[key] = data

    with open(path, "w") as jsonFile:
        json.dump(d, jsonFile)
    return d


def addToJsonFIle(path, dictToAdd: dict):
    with open(path, "r") as jsonFile:
        d = json.load(jsonFile)

    d = {**d, **dictToAdd}
    with open(path, "w") as jsonFile:
        json.dump(d, jsonFile)
    return d


# Date
def timeNow():
    return time.time() * 1000
