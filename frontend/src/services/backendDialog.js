import axios from "axios";
import config from "../../config";
import store from "../store";
import services from "./services";
import cacheService from "./cacheService";

const apiDebiaiURL = config.API_DEBIAI_URL;
const apiDataURL = config.API_DATA_URL;
const apiAlgoURL = config.API_ALGO_URL;

// Request tracking & display utilities
function startRequest(name) {
  let requestCode = services.uuid();
  store.commit("startRequest", { name, code: requestCode });
  return requestCode;
}

function endRequest(code) {
  store.commit("endRequest", code);
}

// Request creation helpers
function dataProviderId() {
  const dpId = store.state.ProjectPage.dataProviderId;
  if (dpId === null || dpId === undefined) throw new Error("Data provider ID not set");
  return dpId;
}

function projectId() {
  const pId = store.state.ProjectPage.projectId;
  if (pId === null || pId === undefined) throw new Error("Project ID not set");
  return pId;
}

// Hash-based cache utilities
//  Provide automatic caching based on hash_content from the backend.
// - If no cached response exists, sends a normal GET request
// - If cached response exists, sends prev_hash_content parameter
// - If backend returns 304, uses cached response
// - If backend returns 200 with new hash_content, updates cache
async function requestWithHashCache(url, cacheKey, requestOptions = {}) {
  try {
    // Get cached response if exists
    const cachedData = await cacheService.getHashResponse(cacheKey);

    // Prepare request parameters
    const params = { ...requestOptions.params };
    if (cachedData && cachedData.hash) params.prev_hash_content = cachedData.hash;

    const response = await axios.get(url, { ...requestOptions, params });

    // If status is 304 (Not Modified), return cached response
    if (response.status === 304 && cachedData) return cachedData.response;

    // If status is 200, save new hash and response
    if (response.status === 200 && response.data.hash_content) {
      await cacheService.saveHashResponse(cacheKey, response.data.hash_content, response.data);
    }

    return response.data;
  } catch (error) {
    // If request fails and we have cached data, return it
    const cachedData = await cacheService.getHashResponse(cacheKey);
    if (cachedData) return cachedData.response;
    throw error;
  }
}

function getCachedRequest(url, cacheKey, requestName) {
  let code = startRequest(requestName);
  return requestWithHashCache(url, cacheKey).finally(() => {
    endRequest(code);
  });
}

// Main API interaction functions
export default {
  startRequest,
  endRequest,
  dataProviderId,
  projectId,

  // Projects
  getProjects() {
    return getCachedRequest(apiDebiaiURL + "projects", "projects", "Getting projects").then(
      (data) => data.projects
    );
  },
  getProject() {
    let code = startRequest("Getting project data");
    return axios
      .get(apiDataURL + dataProviderId() + "/projects/" + projectId())
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  deleteProject() {
    let code = startRequest("Deleting project");
    return axios
      .delete(apiDataURL + dataProviderId() + "/projects/" + projectId())
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // Data providers
  getDataProviders() {
    return getCachedRequest(
      apiDebiaiURL + "data-providers",
      "data-providers",
      "Getting data providers"
    ).then((data) => {
      return data.dataproviders;
    });
  },
  getSingleDataInfo() {
    let code = startRequest("Getting data provider info");
    return axios
      .get(apiDebiaiURL + "data-providers/" + dataProviderId())
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  postDataProvider(type, name, url) {
    let code = startRequest("Creating data provider");
    return axios.post(apiDebiaiURL + "data-providers", { type, name, url }).finally(() => {
      endRequest(code);
    });
  },
  deleteDataProvider(id) {
    let code = startRequest("Deleting data provider");
    return axios.delete(apiDebiaiURL + "data-providers" + "/" + id).finally(() => {
      endRequest(code);
    });
  },

  // Samples ID
  getProjectIdList(analysis, from = null, to = null) {
    let request = apiDataURL + dataProviderId() + "/projects/" + projectId() + "/dataIdList";

    const requestBody = { analysis, from, to };

    return axios.post(request, requestBody).then((response) => response.data);
  },
  getSelectionIdList(selection_id) {
    return axios
      .get(
        apiDataURL + dataProviderId() + "/projects/" + projectId() + "/selections/" + selection_id
      )
      .then((response) => response.data);
  },
  getModelResultsIdList(model_id) {
    return axios
      .get(apiDataURL + dataProviderId() + "/projects/" + projectId() + "/models/" + model_id)
      .then((response) => response.data);
  },

  // Blocks
  getBlocksFromSampleIds(sampleIds, analysis) {
    return axios
      .post(apiDataURL + dataProviderId() + "/projects/" + projectId() + "/blocksFromSampleIds", {
        sampleIds,
        analysis,
      })
      .then((response) => response.data);
  },

  // Models
  getModelResults(modelId, sampleIds) {
    return axios
      .post(
        apiDataURL +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/models/" +
          modelId +
          "/getModelResults",
        { sampleIds }
      )
      .then((response) => response.data);
  },
  delModel(modelId) {
    let code = startRequest("Deleting selection");
    return axios
      .delete(apiDataURL + dataProviderId() + "/projects/" + projectId() + "/models/" + modelId)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Selections
  getSelections() {
    let code = startRequest("Loading selections");
    return axios
      .get(apiDataURL + dataProviderId() + "/projects/" + projectId() + "/selections/")
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addSelection(sampleHashList, selectionName) {
    let code = startRequest("Saving selection");
    return axios
      .post(apiDataURL + dataProviderId() + "/projects/" + projectId() + "/selections/", {
        sampleHashList,
        selectionName,
      })
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  delSelection(selectionId) {
    let code = startRequest("Deleting selection");
    return axios
      .delete(
        apiDataURL + dataProviderId() + "/projects/" + projectId() + "/selections/" + selectionId
      )
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // Layouts
  getLayouts() {
    return axios.get(apiDebiaiURL + "app/layouts/").then((response) => response.data);
  },
  saveLayout(body) {
    let code = startRequest("Saving layout");
    body.projectId = projectId();
    body.dataProviderId = dataProviderId();
    return axios
      .post(apiDebiaiURL + "app/layouts/", body)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteLayout(layoutId) {
    let code = startRequest("Deleting layout");
    return axios
      .delete(apiDebiaiURL + "app/layouts/" + layoutId)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Widget configurations
  getWidgetConfigurationsOverview() {
    return axios.get(apiDebiaiURL + "app/widget-configurations/").then((response) => response.data);
  },
  getWidgetConfigurations(widgetKey) {
    let code = startRequest("Loading widget configurations");
    return axios
      .get(apiDebiaiURL + "app/widgets/" + widgetKey + "/configurations")
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  saveWidgetConfiguration(
    widgetKey,
    { projectId, dataProviderId, configuration, name, description }
  ) {
    let code = startRequest("Saving widget configuration");
    return axios
      .post(apiDebiaiURL + "app/widgets/" + widgetKey + "/configurations", {
        projectId,
        dataProviderId,
        configuration,
        name,
        description,
      })
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteWidgetConfiguration(widgetKey, configurationId) {
    let code = startRequest("Deleting widget configuration");
    return axios
      .delete(apiDebiaiURL + "app/widgets/" + widgetKey + "/configurations/" + configurationId)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Exports
  getExportMethods() {
    let code = startRequest("Loading export methods");
    return axios
      .get(apiDebiaiURL + "app/exportMethods")
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addExportMethod(name, type, parameters) {
    let toExport = { name, type, parameters };

    let code = startRequest("Creating the export method");
    return axios
      .post(apiDebiaiURL + "app/exportMethods", toExport)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteExportMethod(methodId) {
    let code = startRequest("Deleting the export method");
    return axios
      .delete(apiDebiaiURL + "app/exportMethods/" + methodId)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  exportSelection(selectionName, exportMethodId, sampleHashList, annotationValue) {
    let toSend;

    if (annotationValue)
      toSend = {
        selectionName,
        sampleHashList,
        exportMethodId,
        annotationValue,
      };
    else toSend = { selectionName, sampleHashList, exportMethodId };

    let code = startRequest("Exporting the selection " + selectionName);
    return axios
      .post(apiDataURL + dataProviderId() + "/projects/" + projectId() + "/exportSelection", toSend)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  exportData(data, exportMethodId) {
    let code = startRequest("Exporting " + data.type);
    return axios
      .post(apiDebiaiURL + "app/exportMethods/" + exportMethodId + "/exportData", data)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Algo providers
  getAlgoProviders() {
    let code = startRequest("Loading algo providers");
    return axios
      .get(apiAlgoURL)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addAlgoProvider(name, url) {
    let toExport = { name, url };
    let code = startRequest("Adding the algo provider");
    return axios
      .post(apiAlgoURL, toExport)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteAlgoProvider(algoProviderName) {
    let code = startRequest("Deleting the algo provider");
    return axios
      .delete(apiAlgoURL + "/" + algoProviderName)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  useAlgorithm(algoProviderName, algoId, inputs) {
    let code = startRequest("The algorithm is running");
    return axios
      .post(apiAlgoURL + "/" + algoProviderName + "/algorithms/use/" + algoId, {
        inputs,
      })
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
};
