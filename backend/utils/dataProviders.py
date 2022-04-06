import utils.debiaiUtils as debiaiUtils
from configparser import ConfigParser
from utils.utils import timeNow
import requests

#############################################################################
#
# Data providers util
#
# A data provider is a service that the projects that use DebiAI
# can deploy to easily provide data for the application.
# This utility provides a way to interact with the data providers.
#
#############################################################################


class DataProvider:
    def __init__(self, name, url):
        self.name = name
        self.url = url

        # Test the connection
        self.get_info()

    def get_info(self):
        try:
            r = requests.get(self.url + "info")
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return None

    def get_data_id_list(self, view):
        try:
            r = requests.get(self.url + "view/{}/dataIdList".format(view))
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("Error getting data id list from {} on view {}".format(
                self.url, view))
            return []

    def get_data(self, view, data_id_list):
        try:
            r = requests.post(
                self.url + "view/{}/data".format(view), json=data_id_list)
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise Exception(
                "Could not get the data provider {} data for view {}".format(self.url, view))

    def get_models(self, view):
        try:
            r = requests.get(self.url + "view/{}/models".format(view))
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return []

    def get_model_evaluated_data_id_list(self, view, model_id):
        try:
            r = requests.get(
                self.url + "view/{}/model/{}/evaluatedDataIdList".format(view, model_id))
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return []

    def getModelListResults(self, view, modelIds: list, common: bool) -> list:
        samples = set(self.get_model_evaluated_data_id_list(view, modelIds[0]))

        for modelId in modelIds[1:]:
            if common:  # Common samples between models
                samples.intersection_update(
                    self.get_model_evaluated_data_id_list(view, modelId))
            else:  # Union of the model results samples
                samples = samples.union(
                    self.get_model_evaluated_data_id_list(view, modelId))

        return list(samples)

    def getModelResults(self, view, modelId, samples: list) -> dict:
        try:
            r = requests.post(
                self.url + "view/{}/model/{}/results".format(view, modelId), json=samples)
            return r.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return {}


def is_data_provider_up(data_provider_url):
    try:
        r = requests.get(data_provider_url + "info")
        return r.status_code == 200
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False


# The data providers url are stored in the config file
config_object = ConfigParser()
config_object.read("config/config.ini")

data_providers = []


# Get the data providers from the config file
def setup_data_prividers():
    if len(config_object["DATA_PROVIDERS"]) == 0:
        print("No data providers configured")
    else:
        print("Data providers configured:")
        for provider_name in config_object["DATA_PROVIDERS"]:
            provider_url = config_object["DATA_PROVIDERS"][provider_name]

            # Correct the url if needed
            if not provider_url.endswith("/"):
                provider_url += "/"

            print("\t" + provider_name + ": " + provider_url)

            # Test the connection
            if not is_data_provider_up(provider_url):
                print("\t\tError: " + provider_name +
                      " is not available or does not respect the DebiAI data provider API.")
            else:
                data_providers.append(DataProvider(
                    provider_name, provider_url))


# Projects
def get_projects():
    projects = []

    for data_provider in data_providers:
        data_provider_info = data_provider.get_info()
        if data_provider_info is not None:
            for view in data_provider_info:
                # Converting columns to DebiAI block structure
                otherColumns = []
                contextColumns = []
                groundtruthColumns = []
                inputColumns = []
                for column in data_provider_info[view]["columns"]:
                    debiaiColumn = {
                        "name": column["name"],
                        "type": column["type"] if "type" in column else "auto"
                    }
                    if "category" in column and column["category"] == "context":
                        contextColumns.append(debiaiColumn)
                    elif "category" in column and column["category"] == "groundtruth":
                        groundtruthColumns.append(debiaiColumn)
                    elif "category" in column and column["category"] == "input":
                        groundtruthColumns.append(debiaiColumn)
                    else:
                        otherColumns.append(debiaiColumn)

                blockLevelInfo = [{
                    "name": "Data Id",
                    "others": otherColumns,
                    "contexts": contextColumns,
                    "groundTruth": groundtruthColumns,
                    "inputs": inputColumns
                }]

                # Get the models
                models = data_provider.get_models(view)
                debiai_models = []
                for model in models:
                    debiai_models.append({
                        "name": model["name"] if "name" in model else model["id"],
                        "id": model["id"],
                        "nbResults": model["nbSamples"] if "nbSamples" in model else 0,
                        "creationDate": timeNow(),
                        "updateDate": timeNow(),
                        "metadata": {}
                    })

                # Get the data
                samples = data_provider.get_data_id_list(view)

                # Converting views to DebiAI projects
                projects.append({
                    "id": data_provider.name + "|" + view,
                    "name": data_provider_info[view]["name"] if "name" in data_provider_info[view] else view,
                    "dataProvider": data_provider.name,
                    "view": view,
                    "blockLevelInfo": blockLevelInfo,
                    "resultStructure": data_provider_info[view]["expectedResults"],
                    "nbModels": len(debiai_models),
                    "nbSamples": len(samples),
                    "nbRequests": 0,
                    "nbTags": 0,
                    "nbSelections": 0,
                    "creationDate": timeNow(),
                    "updateDate": timeNow(),
                    "modelOverviews": [],
                    "selections": [],
                    "models": debiai_models,
                })

    return projects


def projectExist(projectId):
    projects = get_projects()

    for project in projects:
        if project["id"] == projectId:
            return True


def getProjectById(projectId):
    projects = get_projects()

    for project in projects:
        if project["id"] == projectId:
            return project


def getDataproviderByname(name):
    for data_provider in data_providers:
        if data_provider.name == name:
            return data_provider
    return None


# Data providers
def get_list(projectId, data):
    project = getProjectById(projectId)
    data_provider = getDataproviderByname(project["dataProvider"])
    samples = data_provider.get_data_id_list(project["view"])

    # Then, concat with the model results if given
    if data["modelIds"] and len(data["modelIds"]) > 0:
        modelSamples = data_provider.getModelListResults(
            project["view"], data["modelIds"],  data["commonResults"])
        nbFromModels = len(modelSamples)
        samples = set(samples)
        samples.intersection_update(set(modelSamples))

        return {
            "samples": list(samples),
            "nbSamples": len(samples),
            "nbFromSelection": len(samples),
            "nbFromModels": nbFromModels
        }
    return {
        "samples": samples,
        "nbSamples": len(samples),
        "nbFromSelection": len(samples),
        "nbFromModels": 0
    }


def get_data(projectId, sampleIds):
    project = getProjectById(projectId)
    data_provider = getDataproviderByname(project["dataProvider"])
    return {
        "dataMap": True,
        "data": data_provider.get_data(project["view"], sampleIds)
    }


# Models
def modelExist(projectId, modelId):
    project = getProjectById(projectId)
    if project is None:
        return False

    for model in project["models"]:
        if model["id"] == modelId:
            return True
    return False


def getModelResults(projectId, modelId, sampleIds):
    project = getProjectById(projectId)
    data_provider = getDataproviderByname(project["dataProvider"])
    return data_provider.getModelResults(project["view"], modelId, sampleIds)


# Selections
def get_selections(projectId):
    return []


setup_data_prividers()
