import ujson as json
import time


def get_app_version():
    # Read the version from the package.json
    try:
        with open("package.json") as f:
            package = json.load(f)
            return package["version"]
    except Exception as e:
        print(e)
        return "?.?.?"


# Date
def timeNow():
    return time.time() * 1000
