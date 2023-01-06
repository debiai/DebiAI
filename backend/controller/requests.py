#############################################################################
# Imports
#############################################################################
# import utils.debiaiUtils as debiaiUtils
# import utils.debiai.requests as requestsUtils
import utils.utils as utils

#############################################################################
# Widget request Management
#############################################################################


def get_requests(projectId):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    # Get requests
    requests = requestsUtils.getRequests(projectId)

    return requests, 200


def get_request(projectId, requestId):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    if requestId not in requestsUtils.getRequestsIds(projectId):
        return "Request  " + requestId + " not found", 404

    # Get request
    request = requestsUtils.getRequest(projectId, requestId)

    # Add the request selections to the request
    requestSelections = requestsUtils.getRequestSelections(projectId, requestId)
    request["selections"] = requestSelections

    return request, 200


def post_request(projectId, data):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    requestDescription = data.get("requestDescription", "")

    # Save the selection
    requestInfo = requestsUtils.createRequest(
        projectId, data["requestName"], requestDescription, data["filters"]
    )

    return requestInfo, 200


def delete_request(projectId, requestId):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    if requestId not in requestsUtils.getRequestsIds(projectId):
        return "Request  " + requestId + " not found", 404

    # Delete the request
    requestsUtils.deleteRequest(projectId, requestId)


def create_selection(projectId, requestId, data):
    # ParametersCheck
    if not debiaiUtils.project_exist(projectId):
        return "project " + projectId + " not found", 404

    if requestId not in requestsUtils.getRequestsIds(projectId):
        return "Request  " + requestId + " not found", 404

    # Create the selection
    try:
        requestsUtils.createSelection(projectId, requestId, data["selectionName"])
    except KeyError as e:
        return str(e), 403
    return 200
