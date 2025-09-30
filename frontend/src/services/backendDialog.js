import axios from "axios";
import config from "../../config";
import store from "../store";
import services from "./services";
import cacheService from "./cacheService";
import authService from "./authService";

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

function dataProviderUrl() {
  let dpUrl = store.state.ProjectPage.dataProviderInfo?.metadata?.external_url;
  if (dpUrl === null || dpUrl === undefined) dpUrl = config.API_DATA_URL + dataProviderId();

  // Remove trailing slash if exists
  if (dpUrl.endsWith("/")) return dpUrl.slice(0, -1);
  return dpUrl;
}

function projectId() {
  const pId = store.state.ProjectPage.projectId;
  if (pId === null || pId === undefined) throw new Error("Project ID not set");
  return pId;
}

// Create request configuration with authentication headers
function createRequestConfig() {
  const config = {};
  const authHeaders = authService.getAuthHeader();

  if (Object.keys(authHeaders).length > 0) {
    config.headers = {
      ...authHeaders,
    };
  }

  return config;
}

const requestConfig = createRequestConfig();

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

    // Create request config with auth headers
    const response = await axios.get(url, {
      ...requestOptions,
      ...requestConfig,
      params,
    });

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
      .get(dataProviderUrl() + "/projects/" + projectId(), requestConfig)
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
      .delete(dataProviderUrl() + "/projects/" + projectId(), requestConfig)
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
    ).then((data) => data.dataproviders);
  },
  getSingleDataInfo() {
    let code = startRequest("Getting data provider info");
    return axios
      .get(apiDebiaiURL + "data-providers/" + dataProviderId(), requestConfig)
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  postDataProvider(type, name, url) {
    let code = startRequest("Creating data provider");
    return axios
      .post(apiDebiaiURL + "data-providers", { type, name, url }, requestConfig)
      .finally(() => {
        endRequest(code);
      });
  },
  deleteDataProvider(id) {
    let code = startRequest("Deleting data provider");
    return axios.delete(apiDebiaiURL + "data-providers" + "/" + id, requestConfig).finally(() => {
      endRequest(code);
    });
  },

  // Samples ID
  getProjectIdList(analysis, from = null, to = null) {
    let request = dataProviderUrl() + "/projects/" + projectId() + "/dataIdList";
    const requestBody = { analysis, from, to };

    return axios.post(request, requestBody, requestConfig).then((response) => response.data);
  },
  getSelectionIdList(selection_id) {
    return axios
      .get(
        dataProviderUrl() + "/projects/" + projectId() + "/selections/" + selection_id,
        requestConfig
      )
      .then((response) => response.data);
  },
  getModelResultsIdList(model_id) {
    return axios
      .get(dataProviderUrl() + "/projects/" + projectId() + "/models/" + model_id, requestConfig)
      .then((response) => response.data);
  },

  // Blocks
  getBlocksFromSampleIds(sampleIds, analysis) {
    return axios
      .post(
        dataProviderUrl() + "/projects/" + projectId() + "/blocksFromSampleIds",
        {
          sampleIds,
          analysis,
        },
        requestConfig
      )
      .then((response) => response.data);
  },

  // Models
  getModelResults(modelId, sampleIds) {
    return axios
      .post(
        dataProviderUrl() + "/projects/" + projectId() + "/models/" + modelId + "/getModelResults",
        { sampleIds },
        requestConfig
      )
      .then((response) => response.data);
  },
  delModel(modelId) {
    let code = startRequest("Deleting selection");
    return axios
      .delete(dataProviderUrl() + "/projects/" + projectId() + "/models/" + modelId, requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Selections
  getSelections() {
    let code = startRequest("Loading selections");
    return axios
      .get(dataProviderUrl() + "/projects/" + projectId() + "/selections/", requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addSelection(sampleHashList, selectionName) {
    let code = startRequest("Saving selection");
    return axios
      .post(
        dataProviderUrl() + "/projects/" + projectId() + "/selections/",
        {
          sampleHashList,
          selectionName,
        },
        requestConfig
      )
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
        dataProviderUrl() + "/projects/" + projectId() + "/selections/" + selectionId,
        requestConfig
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
    return getCachedRequest(apiDebiaiURL + "app/layouts/", "layouts", "Getting layouts").then(
      (data) => data.layouts
    );
  },
  saveLayout(body) {
    let code = startRequest("Saving layout");
    body.projectId = projectId();
    body.dataProviderId = dataProviderId();
    return axios
      .post(apiDebiaiURL + "app/layouts/", body, requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteLayout(layoutId) {
    let code = startRequest("Deleting layout");
    return axios
      .delete(apiDebiaiURL + "app/layouts/" + layoutId, requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Widget configurations
  getWidgetConfigurationsOverview() {
    return axios
      .get(apiDebiaiURL + "app/widget-configurations/", requestConfig)
      .then((response) => response.data);
  },
  getWidgetConfigurations(widgetKey) {
    let code = startRequest("Loading widget configurations");
    return axios
      .get(apiDebiaiURL + "app/widgets/" + widgetKey + "/configurations", requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  saveWidgetConfiguration(
    widgetKey,
    { projectId, dataProviderId, configuration, name, description }
  ) {
    let code = startRequest("Saving widget configuration");
    return axios
      .post(
        apiDebiaiURL + "app/widgets/" + widgetKey + "/configurations",
        {
          projectId,
          dataProviderId,
          configuration,
          name,
          description,
        },
        requestConfig
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteWidgetConfiguration(widgetKey, configurationId) {
    let code = startRequest("Deleting widget configuration");
    return axios
      .delete(
        apiDebiaiURL + "app/widgets/" + widgetKey + "/configurations/" + configurationId,
        requestConfig
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Exports
  getExportMethods() {
    let code = startRequest("Loading export methods");
    return axios
      .get(apiDebiaiURL + "app/exportMethods", requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addExportMethod(name, type, parameters) {
    let toExport = { name, type, parameters };

    let code = startRequest("Creating the export method");
    return axios
      .post(apiDebiaiURL + "app/exportMethods", toExport, requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteExportMethod(methodId) {
    let code = startRequest("Deleting the export method");
    return axios
      .delete(apiDebiaiURL + "app/exportMethods/" + methodId, requestConfig)
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
      .post(
        dataProviderUrl() + "/projects/" + projectId() + "/exportSelection",
        toSend,
        requestConfig
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  exportData(data, exportMethodId) {
    let code = startRequest("Exporting " + data.type);
    return axios
      .post(
        apiDebiaiURL + "app/exportMethods/" + exportMethodId + "/exportData",
        data,
        requestConfig
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Algo providers
  getAlgoProviders() {
    let code = startRequest("Loading algo providers");
    return axios
      .get(apiAlgoURL, requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addAlgoProvider(name, url) {
    let toExport = { name, url };
    let code = startRequest("Adding the algo provider");
    return axios
      .post(apiAlgoURL, toExport, requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteAlgoProvider(algoProviderName) {
    let code = startRequest("Deleting the algo provider");
    return axios
      .delete(apiAlgoURL + "/" + algoProviderName, requestConfig)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  useAlgorithm(algoProviderName, algoId, inputs) {
    let code = startRequest("The algorithm is running");
    return axios
      .post(
        apiAlgoURL + "/" + algoProviderName + "/algorithms/use/" + algoId,
        {
          inputs,
        },
        requestConfig
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
};
