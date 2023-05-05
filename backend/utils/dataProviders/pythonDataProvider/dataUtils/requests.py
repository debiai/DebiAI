import os

from utils.dataProviders.pythonDataProvider.dataUtils import pythonModuleUtils

DATA_PATH = pythonModuleUtils.DATA_PATH


def getRequestsIds(projectId):
    try:
        return os.listdir(DATA_PATH + projectId + "/requests")
    except FileNotFoundError:
        os.mkdir(DATA_PATH + projectId + "/requests")
        return []


def getRequests(projetId):
    requests = []
    for requestIds in getRequestsIds(projetId):
        requests.append(getRequest(projetId, requestIds))
    return requests


def getRequest(projectId, requestId):
    return pythonModuleUtils.readJsonFile(
        DATA_PATH + projectId + "/requests/" + requestId + "/info.json"
    )


def getRequestSelections(projectId, requestId):
    selections = []
    selectionsIds = debiaiUtils.getSelectionIds(projectId)
    for selectionId in selectionsIds:
        selectionInfo = debiaiUtils.getSelectionInfo(projectId, selectionId)
        if "requestId" in selectionInfo and selectionInfo["requestId"] == requestId:
            selections.append(selectionInfo)

    return selections


def createRequest(projectId, requestName, requestDescription, filters):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    for filter in filters:
        if "columnLabel" not in filter:
            return "column Label was expected", 400
        # TODO check if columnLabel is valid
        if "type" not in filter:
            return "type was expected", 400
        if filter["type"] not in ["values", "intervals"]:
            return "type " + filter["type"] + " is not 'values' or 'intervals'", 400

        if filter["type"] == "values":
            if "values" not in filter:
                return "values was expected", 400

            for value in filter["values"]:
                if type(value) not in [str, int, float]:
                    return "unexpected values type " + str(type(value)), 400

        if filter["type"] == "intervals":
            if "intervals" not in filter:
                return "intervals was expected", 400

            for interval in filter["intervals"]:
                if "min" not in interval:
                    return "min was expected in the interval", 400
                if "max" not in interval:
                    return "max was expected in the interval", 400

    # Request ID creation
    requestId = pythonModuleUtils.clean_filename(requestName)
    if len(requestId) == 0:
        requestId = pythonModuleUtils.timeNow()

    nbR = 1
    while requestId in getRequestsIds(projectId):
        requestId = pythonModuleUtils.clean_filename(requestName) + "_" + str(nbR)
        nbR += 1

    # Rework filter
    filtersToSave = []
    for filter in filters:
        if "inverted" not in filter:
            filter["inverted"] = False

        f = {
            "columnLabel": filter["columnLabel"],
            "type": filter["type"],
            "inverted": filter["inverted"],
        }
        if f["type"] == "values":
            f["values"] = filter["values"]
        if f["type"] == "intervals":
            f["intervals"] = filter["intervals"]

        filtersToSave.append(f)

    # Save request
    os.mkdir(DATA_PATH + projectId + "/requests/" + requestId)

    requestInfo = {
        "name": requestName,
        "description": requestDescription,
        "id": requestId,
        "filters": filtersToSave,
        "creationDate": pythonModuleUtils.timeNow(),
    }

    pythonModuleUtils.writeJsonFile(
        DATA_PATH + projectId + "/requests/" + requestId + "/info.json", requestInfo
    )

    return requestInfo


def deleteRequest(projectId, requestId):
    pythonModuleUtils.deleteDir(DATA_PATH + projectId + "/requests/" + requestId)


def createSelection(projectId, requestId, selectionName):
    # Load request
    request = getRequest(projectId, requestId)

    # Find the samples that match the request
    selectionSamplesIds = []
    for sample, sampleId in samplesUtils.projectSamplesGerenator(projectId):
        if isSampleInSelection(sample, request["filters"]):
            selectionSamplesIds.append(sampleId)

    # Create the selection
    nbS = 1
    selectionId = pythonModuleUtils.clean_filename(selectionName)
    if len(selectionId) == 0:
        selectionId = pythonModuleUtils.timeNow()
    while debiaiUtils.selectionExist(projectId, selectionId):
        selectionId = pythonModuleUtils.clean_filename(selectionName) + "_" + str(nbS)
        nbS += 1

    debiaiUtils.createSelection(
        projectId, selectionId, selectionName, selectionSamplesIds, requestId=requestId
    )


def isSampleInSelection(sample, filters):
    for filter in filters:
        if filter["columnLabel"] not in sample:
            raise KeyError(
                "columnLabel " + filter["columnLabel"] + " not found in sample"
            )

        if "inverted" not in filter:
            filter["inverted"] = False

        elif filter["type"] == "values" and len(filter["values"]) == 0:
            continue

        elif filter["type"] == "values":
            if str(sample[filter["columnLabel"]]) in filter["values"]:
                if filter["inverted"]:
                    return False
            elif not filter["inverted"]:
                return False

        elif filter["type"] == "intervals":
            if _is_value_in_intervals(
                sample[filter["columnLabel"]], filter["intervals"]
            ):
                if filter["inverted"]:
                    return False
            elif not filter["inverted"]:
                return False
    return True


def _is_value_in_intervals(value, intervals):
    try:
        value = float(value)
    except ValueError:
        return False

    for interval in intervals:
        # Case where the interval is [min, max]
        if (
            "min" in interval
            and interval["min"] is not None
            and "max" in interval
            and interval["max"] is not None
        ):
            if value < interval["min"] or value > interval["max"]:
                return False
        # Case where the interval is [min, None]
        elif "min" in interval and interval["min"] is not None:
            if value < interval["min"]:
                return False
        # Case where the interval is [None, max]
        elif "max" in interval and interval["max"] is not None:
            if value > interval["max"]:
                return False

    return True
