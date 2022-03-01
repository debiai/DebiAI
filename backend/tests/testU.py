import requests
import ujson as json
import random

appUrl = "http://localhost:8080/"

# ============== PROJECTS TEST =================


def test_get_projects():
    url = appUrl + "projects"
    resp = requests.request("GET", url, headers={}, data={})
    assert resp.status_code == 200
    assert type(json.loads(resp.text)) is list


def test_get_bad_project():
    url = appUrl + "projects/IDONSNTEXIST"
    payload = {}
    headers = {}
    resp = requests.request("GET", url, headers=headers, data=payload)
    assert resp.status_code == 404


def test_project_noName():

    # create
    url = appUrl + "projects"
    resp = requests.post(url=url, headers={}, json={})
    assert resp.status_code == 200
    data = json.loads(resp.text)
    projID = data["id"]
    print(projID)
    print(type(projID))
    assert isinstance(projID, unicode)
    assert len(projID) > 0

    # Find back
    url = appUrl + "projects/" + projID
    resp = requests.request("GET", url, headers={}, json={})
    assert resp.status_code == 200
    proj = json.loads(resp.text)
    print(proj)
    print(type(proj))
    assert type(proj) is dict
    assert proj["models"] == []
    assert proj["evaluations"] == []
    assert proj["datasets"] == []
    assert proj["blockLevelInfo"] == []
    assert len(proj["name"]) > 0

    # remove
    url = appUrl + "projects/" + projID
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200

    # Dont Find back
    url = appUrl + "projects/" + projID
    payload = {}
    headers = {}
    resp = requests.request("GET", url, headers=headers, json=payload)
    assert resp.status_code == 404


def test_project_name():

    testProjectName = "My greate project"
    testProjectId = ""

    # Create
    url = appUrl + "projects"
    payload = {"projectName": testProjectName, "blockLevelInfo": []}
    headers = {'content-type': "application/json"}
    resp = requests.post(url=url, headers=headers, json=payload)
    assert resp.status_code == 200
    data = json.loads(resp.text)
    testProjectId = data["id"]
    print(testProjectId)
    assert isinstance(testProjectId, unicode)
    assert len(testProjectId) > 0

    # Get
    url = appUrl + "projects/" + testProjectId
    payload = {}
    headers = {}
    resp = requests.request("GET", url, headers=headers, data=payload)
    assert resp.status_code == 200
    proj = json.loads(resp.text)
    print(proj)
    assert type(proj) is dict
    assert proj["models"] == []
    assert proj["evaluations"] == []
    assert proj["datasets"] == []
    assert proj["blockLevelInfo"] == []
    assert len(proj["name"]) > 0
    assert proj["name"] == testProjectName

    # remove
    url = appUrl + "projects/" + testProjectId
    resp = requests.request("DELETE", url, headers=headers, data=payload)
    assert resp.status_code == 200

    # remove Again
    url = appUrl + "projects/" + testProjectId
    resp = requests.request("DELETE", url, headers=headers, data=payload)
    assert resp.status_code == 404

    # Dont Find back
    url = appUrl + "projects/" + testProjectId
    payload = {}
    headers = {}
    resp = requests.request("GET", url, headers=headers, json=payload)
    assert resp.status_code == 404


def test_project_nameTooLong():
    testProjectName = "My greate project that is clearely too long \
        stop stop stop stop"

    # Create
    url = appUrl + "projects"
    payload = {"projectName": testProjectName, "blockLevelInfo": []}
    headers = {'content-type': "application/json"}
    resp = requests.post(url=url, headers=headers, json=payload)
    assert resp.status_code == 400

# ============== BLOCKS TEST =================


testProjectId = ""


def test_get_Block_BadProject():

    url = appUrl + "projects/IDONTEXIST/blocks/"
    payload = {}
    headers = {}
    resp = requests.get(url=url, json=payload, headers=headers)
    assert resp.status_code == 404


def test_get_Block():
    global testProjectId
    # create Project
    url = appUrl + "projects"
    resp = requests.post(url=url, headers={}, json={})
    assert resp.status_code == 200
    data = json.loads(resp.text)
    testProjectId = data["id"]
    print(testProjectId)
    assert isinstance(testProjectId, unicode)
    assert len(testProjectId) > 0

    url = appUrl + "projects/" + testProjectId + "/blocks"
    resp = requests.get(url=url, json={}, headers={})
    print(resp.text)
    assert resp.status_code == 200
    data = json.loads(resp.text)
    blocks = data["blocks"]
    assert blocks == []


def test_post_block_badProjectName():
    url = appUrl + "projects/IDONTEXIST/blocks"
    payload = {
        "parentId": "",
        "blockName": "block1",
        "groundThruthList": {"toto": "tata"},
        "inputList": {"toto": "tata"},
        "contextList": {"toto": "tata"},
    }
    headers = {'content-type': "application/json"}
    resp = requests.post(url=url, json=payload, headers=headers)
    assert resp.status_code == 404


def test_post_block_badParents():
    url = appUrl + "projects/" + testProjectId + "/blocks"

    payload = {
        "parentId": "IDONTEXIST",
        "blockName": "poorBlock",
        "groundThruthList": {"toto": "tata"},
        "inputList": {"toto": "tata"},
        "contextList": {"toto": "tata"},
    }
    headers = {'content-type': "application/json"}

    resp = requests.post(url=url, json=payload, headers=headers)
    assert resp.status_code == 404


def test_post_block():
    blockName = "My first block"
    # ADD first block
    url = appUrl + "projects/" + testProjectId + "/blocks"
    payload = {
        "blockName": blockName,
        "parentId": "",
        "groundThruthList": {"toto": "tata"},
        "inputList": {"toto": "tata"},
        "contextList": {"toto": "tata"},
    }
    resp = requests.post(url=url, json=payload, headers={
                         'content-type': "application/json"})
    assert resp.status_code == 200
    data = json.loads(resp.text)
    blockTestId = data["blockId"]
    assert isinstance(blockTestId, unicode)
    assert len(blockTestId) > 0

    # Get
    url = appUrl + "projects/" + testProjectId + "/blocks"
    resp = requests.get(url=url, json={}, headers={})
    print(resp.text)
    assert resp.status_code == 200
    data = json.loads(resp.text)
    blocks = data["blocks"]
    assert len(blocks) == 1
    myBlock = blocks[0]
    assert myBlock["name"] == blockName

    # add block to the block
    url = appUrl + "projects/" + testProjectId + "/blocks"
    payload = {
        "blockName": "The very second Second",
        "parentId": blockTestId,
        "groundThruthList": {"toto": "tata"},
        "inputList": {"toto": "tata"},
        "contextList": {"toto": "tata"},
    }
    headers = {'content-type': "application/json"}
    resp = requests.post(url=url, json=payload, headers=headers)
    assert resp.status_code == 200
    data = json.loads(resp.text)
    secBlockId = data["blockId"]
    assert len(secBlockId) > 0

    # Get depth
    url = appUrl + "projects/" + testProjectId + "/blocks?depth=1"
    resp = requests.get(url=url, json={}, headers={})
    print(resp.text)
    assert resp.status_code == 200
    data = json.loads(resp.text)
    blocks = data["blocks"]
    assert len(blocks) == 1
    block = data["blocks"][0]
    assert type(block["childrenInfoList"]) is list
    assert len(block["childrenInfoList"]) == 1

    # Delete
    url = appUrl + "projects/" + testProjectId + "/blocks/" + secBlockId
    resp = requests.delete(url=url, json={}, headers={})
    assert resp.status_code == 200

    # Get depth
    url = appUrl + "projects/" + testProjectId + "/blocks?depth=1"
    resp = requests.get(url=url, json={}, headers={})
    print(resp.text)
    assert resp.status_code == 200
    data = json.loads(resp.text)
    blocks = data["blocks"]
    assert len(blocks) == 1
    block = data["blocks"][0]
    assert type(block["childrenInfoList"]) is list
    assert len(block["childrenInfoList"]) == 0

    # Delete Again
    url = appUrl + "projects/" + testProjectId + "/blocks/" + secBlockId
    resp = requests.delete(url=url, json={}, headers={})
    assert resp.status_code == 404

    # Delete First
    url = appUrl + "projects/" + testProjectId + "/blocks/" + blockTestId
    resp = requests.delete(url=url, json={}, headers={})
    assert resp.status_code == 200

    # Get
    url = appUrl + "projects/" + testProjectId + "/blocks"
    resp = requests.get(url=url, json={}, headers={})
    print(resp.text)
    assert resp.status_code == 200
    data = json.loads(resp.text)
    blocks = data["blocks"]
    assert len(blocks) == 0


def test_delete_block_badProj():
    url = appUrl + "projects/IDONTEXIST/blocks/TODELETE"
    resp = requests.delete(url=url)
    assert resp.status_code == 404


def test_delete_block_badBlock():
    url = appUrl + "projects/" + testProjectId + "/blocks/IDONTEXIST"
    resp = requests.delete(url=url)
    assert resp.status_code == 404

    # remove project
    url = appUrl + "projects/" + testProjectId
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200

# ============== DATASETS TEST =================


def test_post_dataset_badProject():

    url = appUrl + "projects/IDONTEXIST/datasets/"

    payload = {
        "datasetName": "Greate dataset",
        "blockIdList": []
    }
    headers = {'content-type': "application/json"}

    resp = requests.post(url=url, json=payload, headers=headers)
    assert resp.status_code == 404


def test_post_dataset_badBlocks():
    # Create project
    url = appUrl + "projects"
    payload = {"projectName": "My greate project with dataset",
               "blockLevelInfo": []}
    headers = {'content-type': "application/json"}
    resp = requests.post(url=url, headers=headers, json=payload)
    assert resp.status_code == 200
    pId = json.loads(resp.text)["id"]

    # Add dataset
    url = appUrl + "projects/" + pId + "/datasets"

    payload = {
        "datasetName": "I am a dataset",
        "blockIdList": ["toto", "IDONTEXIST", "tutu"]
    }
    headers = {'content-type': "application/json"}

    resp = requests.post(url=url, json=payload, headers=headers)
    assert resp.status_code == 404

    # remove project
    url = appUrl + "projects/" + pId
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200


def test_post_dataset():
    # Create project
    url = appUrl + "projects"
    payload = {"projectName": "My greate project with dataset",
               "blockLevelInfo": []}
    headers = {'content-type': "application/json"}
    resp = requests.post(url=url, headers=headers, json=payload)
    assert resp.status_code == 200
    pId = json.loads(resp.text)["id"]

    # Get
    url = appUrl + "projects/" + pId
    resp = requests.request("GET", url, headers={}, data={})
    assert resp.status_code == 200
    proj = json.loads(resp.text)
    print(proj)
    assert type(proj) is dict
    assert proj["datasets"] == []

    # create dataset
    url = appUrl + "projects/" + pId + "/datasets"
    payload = {
        "datasetName": "I am a dataset",
        "blockIdList": []  # empty blocks ref
    }
    headers = {'content-type': "application/json"}
    resp = requests.post(url=url, json=payload, headers=headers)
    assert resp.status_code == 200
    print(resp.text)
    datasetId = json.loads(resp.text)["id"]

    # get Dataset with project
    url = appUrl + "projects/" + pId
    resp = requests.request("GET", url, headers={}, data={})
    assert resp.status_code == 200
    proj = json.loads(resp.text)
    assert type(proj) is dict
    assert len(proj["datasets"]) == 1
    assert proj["datasets"][0]["id"] == datasetId

    # delete dataset
    url = appUrl + "projects/" + pId + "/datasets/" + datasetId
    resp = requests.delete(url=url, json={}, headers={})
    assert resp.status_code == 200

    # Delete again
    resp = requests.delete(url=url, json={}, headers={})
    assert resp.status_code == 404

    # remove project
    url = appUrl + "projects/" + pId
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200


def test_post_dataset_withCreatedBlock():
    # Create project
    url = appUrl + "projects"
    payload = {"projectName": "My greate project with dataset",
               "blockLevelInfo": []}
    headers = {'content-type': "application/json"}
    resp = requests.post(url=url, headers=headers, json=payload)
    assert resp.status_code == 200
    pId = json.loads(resp.text)["id"]

    # ADD  block
    url = appUrl + "projects/" + pId + "/blocks"
    payload = {
        "blockName": "My first block",
        "parentId": "",
        "groundThruthList": {"toto": "tata"},
        "inputList": {"toto": "tata"},
        "contextList": {"toto": "tata"},
    }
    resp = requests.post(url=url, json=payload, headers={
                         'content-type': "application/json"})
    assert resp.status_code == 200
    data = json.loads(resp.text)
    blockTestId = data["blockId"]
    assert len(blockTestId) > 0

    # addadataset
    url = appUrl + "projects/" + pId + "/datasets"
    payload = {
        "datasetName": "dataset with blocks",
        "blockIdList": [blockTestId]
    }
    headers = {'content-type': "application/json"}

    resp = requests.post(url=url, json=payload, headers=headers)
    print(resp.text)
    assert resp.status_code == 200

    # remove project
    url = appUrl + "projects/" + pId
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 200
