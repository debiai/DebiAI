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
  startRequest,
  endRequest,
  dataProviderId,
  projectId,
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

  // Samples ID
  getProjectIdList(analysis, from = null, to = null) {
    let request =
      apiURL + "data-providers/" + dataProviderId() + "/projects/" + projectId() + "/dataIdList";

    const requestBody = { analysis, from, to };

    return axios.post(request, requestBody).then((response) => response.data);
  },
  getSelectionIdList(selection_id) {
    return axios
      .get(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/selections/" +
          selection_id
      )
      .then((response) => response.data);
  },
  getModelResultsIdList(model_id) {
    return axios
      .get(
        apiURL +
          "data-providers/" +
          dataProviderId() +
          "/projects/" +
          projectId() +
          "/models/" +
          model_id
      )
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
