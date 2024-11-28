import requests
import ujson as json

appUrl = "http://localhost:3000/"
testLayoutId = None


def delete_layout(id):
    url = appUrl + "app/layouts/" + id
    resp = requests.request("DELETE", url, headers={}, data={})
    assert resp.status_code == 204


def test_get_layouts():
    url = appUrl + "app/layouts"
    resp = requests.request("GET", url, headers={}, data={})
    layouts = json.loads(resp.text)
    print(layouts)
    assert resp.status_code == 200
    assert type(layouts) is list

    # Remove all layouts
    for layout in layouts:
        assert type(layout) is dict
        assert "id" in layout
        delete_layout(layout["id"])


def test_add_layout():
    global testLayoutId
    url = appUrl + "app/layouts/"
    data = {
        "name": "testName",
        "description": "testDescription",
        "projectId": "testProjectId",
        "dataProviderId": "testDataProviderId",
        "layout": [
            {
                "x": 0,
                "y": 0,
                "width": 1,
                "height": 1,
                "widgetKey": "testWidgetKey",
                "config": {},
                "name": "testName",
            }
        ],
        "selectedColorColumn": "TestColorColumn",
    }
    resp = requests.request("POST", url, headers={}, json=data)
    assert resp.status_code == 204

    # Check if the layout was added
    resp = requests.request("GET", url, headers={}, data={})
    layouts = json.loads(resp.text)
    assert resp.status_code == 200
    assert type(layouts) is list
    assert len(layouts) == 1
    assert layouts[0]["name"] == data["name"]
    assert layouts[0]["description"] == data["description"]
    assert layouts[0]["projectId"] == data["projectId"]
    assert layouts[0]["dataProviderId"] == data["dataProviderId"]
    assert type(layouts[0]["layout"]) is list
    assert len(layouts[0]["layout"]) == 1
    assert layouts[0]["layout"][0]["x"] == data["layout"][0]["x"]
    assert layouts[0]["layout"][0]["y"] == data["layout"][0]["y"]
    assert layouts[0]["selectedColorColumn"] == data["selectedColorColumn"]

    assert "id" in layouts[0]
    assert type(layouts[0]["id"]) is str
    assert len(layouts[0]["id"]) > 0
    testLayoutId = layouts[0]["id"]


def test_delete_layout():
    # Remove the layout
    delete_layout(testLayoutId)

    # Check if the layout was removed
    url = appUrl + "app/layouts/"
    resp = requests.request("GET", url, headers={}, data={})
    layouts = json.loads(resp.text)
    assert resp.status_code == 200
    assert type(layouts) is list
    assert len(layouts) == 0


def test_last_layout_saved():
    # if lastLayoutSaved is true, the previous layout with lastLayoutSaved = true
    # should be deleted

    # Add the first layout
    url = appUrl + "app/layouts/"
    data = {
        "name": "testName",
        "description": "testDescription",
        "projectId": "testProjectId",
        "dataProviderId": "testDataProviderId",
        "lastLayoutSaved": True,
        "layout": [],
    }
    resp = requests.request("POST", url, headers={}, json=data)
    assert resp.status_code == 204

    # Add the second layout
    data = {
        "name": "testName2",
        "description": "testDescription",
        "projectId": "testProjectId",
        "dataProviderId": "testDataProviderId",
        "lastLayoutSaved": True,
        "layout": [],
    }
    resp = requests.request("POST", url, headers={}, json=data)
    assert resp.status_code == 204

    # Check if the first layout was removed
    url = appUrl + "app/layouts/"
    resp = requests.request("GET", url, headers={}, data={})
    layouts = json.loads(resp.text)
    assert resp.status_code == 200
    assert type(layouts) is list
    assert len(layouts) == 1
    assert layouts[0]["lastLayoutSaved"] is True
    assert layouts[0]["name"] == data["name"]
    assert layouts[0]["description"] == data["description"]
    assert layouts[0]["projectId"] == data["projectId"]
    assert layouts[0]["dataProviderId"] == data["dataProviderId"]

    # Remove the layout
    delete_layout(layouts[0]["id"])
