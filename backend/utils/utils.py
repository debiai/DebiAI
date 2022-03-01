import ujson as json
import os
import posixpath
import unicodedata
import string
import shutil
import time
from configparser import ConfigParser

# # Profiling
# import pstats
# import cProfile
# import atexit

# pr = cProfile.Profile()


# def exit_handler():
#     print('My application is ending!')

#     stats = pstats.Stats(pr)
#     stats.sort_stats(pstats.SortKey.TIME)
#     stats.dump_stats(filename="logs/stats.prof")


# atexit.register(exit_handler)

# Read config.ini file
config_object = ConfigParser()
config_object.read("config/config.ini")

TRACE_LOG_CONFIG = config_object["LOG"]["operationTraceLog"]

# Consts
valid_filename_chars = "_-() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


# File name verifications
def clean_filename(filename, whitelist=valid_filename_chars):
    # replace spaces
    filename = filename.replace(" ", "_")

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize(
        'NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    return cleaned_filename[:char_limit]


def is_filename_clean(filename):
    cleanFilename = "".join(i for i in filename if i not in "\/:*?<>|")
    return filename == cleanFilename


def is_secure_path(path):
    path = posixpath.normpath(path)
    return not path.startswith(('/', '../'))


# directories and file Manipulation

def fileExist(path):
    return os.path.isfile(path)


def listDir(path):
    # List the directories only
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]


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
    with open(path, 'w') as outfile:
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


# ==== Function wraper ====
# Performance measuring
def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2 - time1) * 1000.0))

        return ret

    return wrap


# Operations trace log
def traceLog(f):
    def wrap(*args, **kwargs):
        time1 = time.time()

        # Executing the function
        ret = f(*args, **kwargs)

        if TRACE_LOG_CONFIG == "full" or TRACE_LOG_CONFIG == "light":

            # Saving the timestamp, the execution time
            # the function name and the arguments
            executionTime = (time.time() - time1) * 1000.0
            toSave = {
                "timestamp": time.time(),
                "executionTime": executionTime,
                "funtion": f.__name__,
                "args": args,
                "kwargs": kwargs,
            }
            if TRACE_LOG_CONFIG == "full":
                # Saving the return
                toSave["return"] = ret

            # Updating the logs
            with open("logs/logs.json", "a") as logs:
                logs.write(json.dumps(toSave) + "\n")

        return ret

    return wrap


def traceLogLight(f):
    def wrap(*args, **kwargs):
        time1 = time.time()

        # Executing the function
        # pr.enable()
        ret = f(*args, **kwargs)
        # pr.disable()

        if TRACE_LOG_CONFIG == "full" or TRACE_LOG_CONFIG == "light":
            executionTime = (time.time() - time1) * 1000.0
            toSave = {
                "timestamp": time.time(),
                "executionTime": executionTime,
                "funtion": f.__name__,
            }

            # TODO : get a parameters memory size approximation

            with open("logs/logs.json", "a") as logs:
                logs.write(json.dumps(toSave) + "\n")

        return ret

    return wrap
