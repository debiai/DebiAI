#############################################################################
# Imports
#############################################################################
import os
from datetime import date

import utils.debiaiUtils as debiaiUtils
import utils.utils as utils
import backend.utils.export.kafkaUtils as kafkaUtils

dataPath = debiaiUtils.dataPath

#############################################################################
# Selections Management
#############################################################################


@utils.traceLogLight
def get_selections(projectId):
    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    # Get selections
    selections = []
    for selectionId in debiaiUtils.getSelectionIds(projectId):
        selections.append(debiaiUtils.getSelectionInfo(projectId, selectionId))

    return selections, 200


@utils.traceLogLight
def post_selection(projectId, data):

    # ParametersCheck
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    # Selection creation
    selectionId = utils.clean_filename(data['selectionName'])
    if len(selectionId) == 0:
        selectionId = utils.timeNow()

    nbS = 1
    while debiaiUtils.selectionExist(projectId, selectionId):
        selectionId = utils.clean_filename(
            data['selectionName']) + "_" + str(nbS)
        nbS += 1

    # Add the request id to the selection if provided
    requestId = None
    if 'requestId' in data:
        requestId = data['requestId']

    # Save the selection
    selectionInfo = debiaiUtils.createSelection(
        projectId,
        selectionId,
        data['selectionName'],
        list(set(data['sampleHashList'])),
        requestId
    )

    # Send the selection to Kafka
    project_name = debiaiUtils.getProjectNameFromId(projectId)
    project_sample_hashmap = debiaiUtils.getHashmap(projectId)
    sample_path = []
    for sample_hash in selectionInfo['samples']:
        sample_path.append(project_sample_hashmap[sample_hash])

    kafkaUtils.send_sample_selection(
        project_name,
        data['selectionName'],
        sample_path
    )
    return selectionInfo, 200


@utils.traceLog
def delete_selection(projectId, selectionId):
    if not debiaiUtils.projectExist(projectId):
        return "project " + projectId + " not found", 404

    if not debiaiUtils.selectionExist(projectId, selectionId):
        return "The selection doesn't exist", 404

    debiaiUtils.deleteSelection(projectId, selectionId)

    return 200
