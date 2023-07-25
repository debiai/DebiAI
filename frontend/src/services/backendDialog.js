import axios from "axios";
import config from "../../config";
import store from "../store";
import services from "./services";

const apiURL = config.API_URL;

function startRequest(name) {
  let requestCode = services.uuid();
  store.commit("startRequest", { name, code: requestCode });
  return requestCode;
}

function endRequest(code) {
  store.commit("endRequest", code);
}

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

export default {
  // ====== Menu

  // Projects
  getProjects() {
    let code = startRequest("Getting projects");
    return axios
      .get(apiURL + "projects")
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  getProject() {
    let code = startRequest("Getting project data");
    return axios
      .get(apiURL + "data-providers/" + dataProviderId() + "/projects/" + projectId())
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
      .delete(apiURL + "data-providers/" + dataProviderId() + "/projects/" + projectId())
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // Data providers
  getDataProviders() {
    let code = startRequest("Getting data providers");
    return axios
      .get(apiURL + "data-providers")
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  getSingleDataInfo() {
    let code = startRequest("Getting data provider info");
    return axios
      .get(apiURL + "data-providers/" + dataProviderId())
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  postDataProvider(type, name, url) {
    let code = startRequest("Creating data provider");
    return axios.post(apiURL + "data-providers", { type, name, url }).finally(() => {
      endRequest(code);
    });
  },
  deleteDataProvider(id) {
    let code = startRequest("Deleting data provider");
    return axios.delete(apiURL + "data-providers/" + id).finally(() => {
      endRequest(code);
    });
  },

  // Samples
  getProjectSamples({
    analysis,
    selectionIds = [],
    selectionIntersection = false,
    modelIds = [],
    commonResults = false,
    from = null,
    to = null,
  }) {
    let code;
    if (from === null) code = startRequest("Loading the project samples list");
    let request =
      apiURL + "data-providers/" + dataProviderId() + "/projects/" + projectId() + "/samples";

    const requestBody = {
      analysis,
      selectionIds,
      selectionIntersection,
      modelIds,
      commonResults,
    };
    if (from !== null && to !== null) {
      requestBody.from = from;
      requestBody.to = to;
    }

    return axios
      .post(request, requestBody)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Blocks
  getBlocksFromSampleIds(sampleIds, analysis) {
    return axios
      .post(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/blocksFromSampleIds",
        { sampleIds, analysis }
      )
      .then((response) => response.data);
  },

  // Models
  getModelResults(modelId, sampleIds) {
    return axios
      .post(
        apiURL +
          "data-providers/" +
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
      .delete(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/models/" +
          modelId
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Selections
  getSelections() {
    let code = startRequest("Loading selections");
    return axios
      .get(
        apiURL + "data-providers/" + dataProviderId() + "/projects/" + projectId() + "/selections/"
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addSelection(sampleHashList, selectionName, requestId = null) {
    let code = startRequest("Saving selection");
    return axios
      .post(
        apiURL + "data-providers/" + dataProviderId() + "/projects/" + projectId() + "/selections/",
        { sampleHashList, selectionName, requestId }
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
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/selections/" +
          selectionId
      )
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // Requests
  getRequests() {
    let code = startRequest("Loading requests");
    return axios
      .get(
        apiURL + "data-providers/" + dataProviderId() + "/projects/" + projectId() + "/requests/"
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  getRequest(requestId) {
    let code = startRequest("Loading request");
    return axios
      .get(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/requests/" +
          requestId
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addRequest(requestName, requestDescription, filters) {
    let code = startRequest("Saving the request");
    return axios
      .post(
        apiURL + "data-providers/" + dataProviderId() + "/projects/" + projectId() + "/requests/",
        { requestName, requestDescription, filters }
      )
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  createSelectionFromRequest(requestId, selectionName) {
    let code = startRequest("Creating a selection");
    return axios
      .post(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/requests/" +
          requestId +
          "/newSelection",
        { selectionName }
      )
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  delRequest(requestId) {
    let code = startRequest("Deleting request");
    return axios
      .delete(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/requests/" +
          requestId
      )
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // ====== Exploration
  getColumnsMetrics(columnLabels) {
    let code = startRequest("Loading columns metrics");
    return axios
      .post(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/exploration/columnsMetrics",
        { columnLabels }
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  getColumnsCombinatorialMetrics(columns) {
    let code = startRequest("Loading columns combinatorial metrics");
    return axios
      .post(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/exploration/combinatorialMetrics",
        { columns }
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  getDataIdListFromFilters(filters) {
    let code = startRequest("Loading data id list from filters");
    return axios
      .post(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/exploration/dataIdList",
        { filters }
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // ====== DataAnalysis

  // Operation center
  correlationMatrix(columnsData, matrixType) {
    let code = startRequest("Calculating " + matrixType + " correlation matrix");
    return axios
      .post(apiURL + "statisticalOperations/" + matrixType + "Correlation", columnsData)
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  mutualInformation(columnsData, matrixType) {
    let code = startRequest("Calculating " + matrixType + " correlation matrix");
    return axios
      .post(apiURL + "statisticalOperations/" + matrixType + "Correlation", columnsData)
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  higherDimensionMutualInformation(columnsData, k, base) {
    let code = startRequest("Calculating higher mutual information");
    return axios
      .post(apiURL + "statisticalOperations/higherDimensionMutualInformation", {
        X: columnsData,
        k,
        base,
      })
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  continuousAndHigherDimensionMutualInformation(
    list_continuous,
    list_discrete,
    k,
    base,
    normalise
  ) {
    let code = startRequest("Calculating mutual information");
    return axios
      .post(apiURL + "statisticalOperations/continuousAndHigherDimensionMutualInformation", {
        list_continuous,
        list_discrete,
        k,
        base,
        normalise,
      })
      .finally(() => {
        endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // Layouts
  getLayouts() {
    return axios.get(apiURL + "app/layouts/").then((response) => response.data);
  },
  saveLayout(body) {
    let code = startRequest("Saving layout");
    body.projectId = projectId();
    body.dataProviderId = dataProviderId();
    return axios
      .post(apiURL + "app/layouts/", body)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteLayout(layoutId) {
    let code = startRequest("Deleting layout");
    return axios
      .delete(apiURL + "app/layouts/" + layoutId)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Widget configurations
  getWidgetConfigurationsOverview() {
    return axios.get(apiURL + "app/widget-configurations/").then((response) => response.data);
  },
  getWidgetConfigurations(widgetKey) {
    let code = startRequest("Loading widget configurations");
    return axios
      .get(apiURL + "app/widgets/" + widgetKey + "/configurations")
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  saveWidgetConfiguration(
    widgetKey,
    { projectId, dataProviderId, configuration, name, description }
  ) {
    let code = startRequest("Saving widget configuration");
    return axios
      .post(apiURL + "app/widgets/" + widgetKey + "/configurations", {
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
      .delete(apiURL + "app/widgets/" + widgetKey + "/configurations/" + configurationId)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Exports
  getExportMethods() {
    let code = startRequest("Loading export methods");
    return axios
      .get(apiURL + "app/exportMethods")
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addExportMethod(name, type, parameters) {
    let toExport = { name, type, parameters };

    let code = startRequest("Creating the export method");
    return axios
      .post(apiURL + "app/exportMethods", toExport)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteExportMethod(methodId) {
    let code = startRequest("Deleting the export method");
    return axios
      .delete(apiURL + "app/exportMethods/" + methodId)
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
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/exportSelection",
        toSend
      )
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  exportData(data, exportMethodId) {
    let code = startRequest("Exporting " + data.type);
    return axios
      .post(apiURL + "app/exportMethods/" + exportMethodId + "/exportData", data)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },

  // Algo providers
  getAlgoProviders() {
    let code = startRequest("Loading algo providers");
    return axios
      .get(apiURL + "app/algo-providers")
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  addAlgoProvider(name, url) {
    let toExport = { name, url };
    let code = startRequest("Adding the algo provider");
    return axios
      .post(apiURL + "app/algo-providers", toExport)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  deleteAlgoProvider(algoProviderName) {
    let code = startRequest("Deleting the algo provider");
    return axios
      .delete(apiURL + "app/algo-providers/" + algoProviderName)
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
  useAlgorithm(algoProviderName, algoId, inputs) {
    let code = startRequest("The algorithm is running");
    return axios
      .post(apiURL + "app/algo-providers/" + algoProviderName + "/algorithms/use/" + algoId, {
        inputs,
      })
      .finally(() => endRequest(code))
      .then((response) => response.data);
  },
};
