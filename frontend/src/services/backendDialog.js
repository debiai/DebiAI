import axios from 'axios'
import config from '../../config'
import store from '../store'
import services from "./services"

const apiURL = config.API_URL

function startRequest(name) {
  let requestCode = services.uuid()
  store.commit("startRequest", { name, code: requestCode })
  return requestCode
}

function endRequest(code) {
  store.commit("endRequest", code)
}

export default {

  ping() { return axios.get(apiURL) },

  log(projectId, data) {
    return axios.post(apiURL + "projects/" + projectId + "/log", data);
  },

  // ====== Menu

  // Projects
  getProjects() {
    let code = startRequest("Getting projects")
    return axios.get(apiURL + 'projects').finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  addProject(project) {
    let code = startRequest("Creating project")
    return axios.post(apiURL + 'projects', project).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  getProject(id) {
    let code = startRequest("Getting project data")
    return axios.get(apiURL + 'projects/' + id).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  deleteProject(id) {
    let code = startRequest("Deleting project")
    return axios.delete(apiURL + 'projects/' + id).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  saveProjectlevels(projectId, blockLevels) {
    let code = startRequest("Creating project")
    return axios.post(apiURL + 'projects/' + projectId + '/blocklevels', blockLevels).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },

  // Data providers
  getDataProviders() {
    let code = startRequest("Getting data providers")
    return axios.get(apiURL + 'data-providers').finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  postDataProvider(type, name, url) {
    let code = startRequest("Creating data provider")
    return axios.post(apiURL + 'data-providers', { type, name, url }).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  
  // Samples
  getSampleNumber(projectId, selectionId = undefined) {
    let code = startRequest("Loading the project data")
    let request = apiURL + 'projects/' + projectId + '/getAvailableDataNumber'
    if (selectionId) request += '?selectionId=' + selectionId

    return axios.get(request).finally(() => endRequest(code))
      .then((response) => response.data)
  },
  getSampleNumberWithModelResults(projectId, modelIds, common) {
    let code = startRequest("Loading the project data")
    let request = apiURL + 'projects/' + projectId + '/getAvailableDataNumberWithModelResults?modelIds=' + modelIds + '&common=' + common

    return axios.get(request).finally(() => endRequest(code))
      .then((response) => response.data)
  },
  getProjectSamples(projectId, {
    selectionIds = [],
    selectionIntersection = false,
    modelIds = [],
    commonResults = false,
    from = null,
    to = null
  }) {
    let code;
    if (from === null) code = startRequest("Loading the project samples list")
    let request = apiURL + 'projects/' + projectId + '/samples'

    console.log("getProjectSamples", projectId, selectionIds, selectionIntersection, modelIds, commonResults);

    const requestBody = {
      selectionIds,
      selectionIntersection,
      modelIds,
      commonResults,
    }

    if (from !== null && to !== null) {
      requestBody.from = from
      requestBody.to = to
    }

    return axios.post(request, requestBody).finally(() => endRequest(code))
      .then((response) => response.data)
  },
  getSelectionSamples(projectId, selectionId) {
    let code = startRequest("Loading the project samples list")
    let request = apiURL + 'projects/' + projectId + '/selectionSamples/' + selectionId

    return axios.get(request).finally(() => endRequest(code))
      .then((response) => response.data)
  },

  // Blocks
  addBlock(projectId, block) {
    let code = startRequest("Adding Block")
    return axios.post(apiURL + 'projects/' + projectId + '/blocks', block).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  getBlocks(projectId, depth = 1) {
    let code = startRequest("Loading the project data")

    return axios.get(apiURL + 'projects/' + projectId + '/blocks?depth=' + depth).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  getBlocksChunk(projectId, start, size, selectionId = undefined) {
    let request = apiURL + 'projects/' + projectId + '/trainingSamples?start=' + start + '&size=' + size
    if (selectionId) request += '&selectionId=' + selectionId

    return axios.get(request).then((response) => response.data)
  },
  getBlocksChunkWithModelResults(projectId, start, size, modelIds, common, selectionId = undefined) {
    let request = apiURL + 'projects/' + projectId +
      '/trainingSamplesWithModelResults?start=' + start + '&size=' + size + '&modelIds=' + modelIds + '&common=' + common
    if (selectionId) request += '&selectionId=' + selectionId

    return axios.get(request).then((response) => response.data)
  },
  getBlocksFromSelection(projectId, selectionId, depth = 1) {
    let code = startRequest("Loading the request data")

    return axios.get(apiURL + 'projects/' + projectId + '/blocks/' + selectionId + '?depth=' + depth).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  getBlocksTree(projectId, blockId, blockPath, depth = 1) {
    let code = startRequest("Loading the project data")

    return axios.post(apiURL + 'projects/' + projectId + '/block', {
      blockId,
      blockPath,
      depth,
    }).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  getBlocksTreeWithModelResults(projectId, modelIds, common) {
    let code = startRequest("Loading the project data and the model results")

    return axios.post(apiURL + 'projects/' + projectId + '/blocksWithModelResults', {
      modelIds,
      common,
    }).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  getBlocksFromSampleIds(projectId, sampleIds) {
    return axios.post(apiURL + 'projects/' + projectId + '/blocksFromSampleIds', { sampleIds })
      .then((response) => response.data)
  },

  // Models
  getModelResults(projectId, modelId, sampleIds) {
    return axios.post(apiURL + 'projects/' + projectId + '/models/' + modelId + '/getModelResults', { sampleIds })
      .then((response) => response.data)
  },

  delModel(projectId, modelId) {
    let code = startRequest("Deleting selection")
    return axios.delete(apiURL + 'projects/' + projectId + '/models/' + modelId)
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },


  // Selections
  getSelections(projectId) {
    let code = startRequest("Loading selections")
    return axios.get(apiURL + 'projects/' + projectId + '/selections/')
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  addSelection(projectId, sampleHashList, selectionName, requestId = null) {
    console.log(requestId);
    let code = startRequest("Saving selection")
    return axios.post(apiURL + 'projects/' + projectId + '/selections/',
      { sampleHashList, selectionName, requestId }).finally(() => {
        endRequest(code)
      }).then((response) => {
        return response.data
      })
  },
  delSelection(projectId, selectionId) {
    let code = startRequest("Deleting selection")
    return axios.delete(apiURL + 'projects/' + projectId + '/selections/' + selectionId).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },

  // Requests
  getRequests(projectId) {
    let code = startRequest("Loading requests")
    return axios.get(apiURL + 'projects/' + projectId + '/requests/')
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  getRequest(projectId, requestId) {
    let code = startRequest("Loading request")
    return axios.get(apiURL + 'projects/' + projectId + '/requests/' + requestId)
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  addRequest(projectId, requestName, requestDescription, filters) {
    let code = startRequest("Saving the request")
    return axios.post(apiURL + 'projects/' + projectId + '/requests/',
      { requestName, requestDescription, filters }).finally(() => {
        endRequest(code)
      }).then((response) => {
        return response.data
      })
  },
  createSelectionFromRequest(projectId, requestId, selectionName) {
    let code = startRequest("Creating a selection")
    return axios.post(apiURL + 'projects/' + projectId + '/requests/' + requestId + '/newSelection', { selectionName }).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  delRequest(projectId, requestId) {
    let code = startRequest("Deleting request")
    return axios.delete(apiURL + 'projects/' + projectId + '/requests/' + requestId).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },


  // ====== DataAnalysis

  // Operation center
  correlationMatrix(columnsData, matrixType) {
    let code = startRequest("Calculating " + matrixType + " correlation matrix")
    return axios.post(apiURL + 'statisticalOperations/' + matrixType + 'Correlation', columnsData).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  mutualInformation(columnsData, matrixType) {
    let code = startRequest("Calculating " + matrixType + " correlation matrix")
    return axios.post(apiURL + 'statisticalOperations/' + matrixType + 'Correlation', columnsData).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  higherDimensionMutualInformation(columnsData, k, base) {
    let code = startRequest("Calculating higher mutual information")
    return axios.post(apiURL + 'statisticalOperations/higherDimensionMutualInformation', {
      X: columnsData,
      k,
      base
    }).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },
  continuousAndHigherDimensionMutualInformation(list_continuous, list_discrete, k, base, normalise) {

    let code = startRequest("Calculating mutual information")
    return axios.post(apiURL + 'statisticalOperations/continuousAndHigherDimensionMutualInformation', {
      list_continuous,
      list_discrete,
      k,
      base,
      normalise
    }).finally(() => {
      endRequest(code)
    }).then((response) => {
      return response.data
    })
  },

  // Widget configurations
  getWidgetConfiguration(projectId) {
    let code = startRequest("Loading widget configurations")
    return axios.get(apiURL + 'projects/' + projectId + '/widgetconf')
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  saveWidgetConfiguration(projectId, { widgetTitle, configuration, name, description }) {
    let code = startRequest("Saving widget configuration")
    return axios.post(apiURL + 'projects/' + projectId + '/widgetconf',
      { widgetTitle, configuration, name, description })
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  deleteWidgetConfiguration(projectId, { widgetTitle, name }) {
    let code = startRequest("Deleting widget configuration")
    return axios.post(apiURL + 'projects/' + projectId + '/widgetconf/delete', { widgetTitle, name })
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },

  // Tags
  updateTag(projectId, tagName, tagHash) {
    let code = startRequest("Updating tag")
    return axios.post(apiURL + 'projects/' + projectId + '/tags', { tagName, tagHash })
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  getTags(projectId) {
    let code = startRequest("Loading tags")
    return axios.get(apiURL + 'projects/' + projectId + '/tags')
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  deleteTag(projectId, tagId) {
    let code = startRequest("Deleting tag")
    return axios.delete(apiURL + 'projects/' + projectId + '/tags/' + tagId)
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },

  // Exports
  getExportMethods() {
    let code = startRequest("Loading export methods")
    return axios.get(apiURL + 'app/exportMethods')
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  addExportMethod(name, type, parameters) {

    let toExport = { name, type, parameters }

    let code = startRequest("Creating the export method")
    return axios.post(apiURL + 'app/exportMethods', toExport)
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  deleteExportMethod(methodId) {
    let code = startRequest("Deleting the export method")
    return axios.delete(apiURL + 'app/exportMethods/' + methodId)
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  exportSelection(projectId, selectionName, exportMethodId, sampleHashList, annotationValue) {
    let toSend

    if (annotationValue) toSend = { selectionName, sampleHashList, exportMethodId, annotationValue }
    else toSend = { selectionName, sampleHashList, exportMethodId }

    let code = startRequest("Exporting the selection " + selectionName)
    return axios.post(apiURL + 'projects/' + projectId + '/exportSelection', toSend)
      .finally(() => endRequest(code))
      .then((response) => response.data)
  },
  exportData(data, exportMethodId) {
    let code = startRequest("Exporting " + data.type)
    return axios.post(apiURL + 'app/exportMethods/' + exportMethodId + '/exportData', data)
      .finally(() => endRequest(code))
      .then((response) => response.data)
  }
}