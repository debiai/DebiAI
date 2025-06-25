import axios from "axios";
import config from "../../../config";
import b from "../backendDialog";

const apiURL = config.EXPLORATION_API_URL;

export default {
  // Explorations
  getExplorations(projectId, displayMessage = true) {
    let code;
    if (displayMessage) code = b.startRequest("Getting explorations");
    return axios
      .get(`${apiURL}explorations`, {
        params: {
          project_id: projectId,
        },
      })
      .finally(() => {
        if (displayMessage) b.endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  createExploration(projectId, explorationName, explorationDescription) {
    let code = b.startRequest("Creating exploration");
    return axios
      .post(
        `${apiURL}explorations`,
        {
          name: explorationName,
          description: explorationDescription,
        },
        {
          params: {
            project_id: projectId,
          },
        }
      )
      .finally(() => {
        b.endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  deleteExploration(projectId, explorationId) {
    let code = b.startRequest("Deleting exploration");
    return axios
      .delete(`${apiURL}explorations/${explorationId}`, {
        params: {
          project_id: projectId,
        },
      })
      .finally(() => {
        b.endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // Exploration
  getExploration(projectId, explorationId, displayMessage = true) {
    let code;
    if (displayMessage) code = b.startRequest("Getting exploration");

    return axios
      .get(`${apiURL}explorations/${explorationId}`, {
        params: {
          project_id: projectId,
        },
      })
      .finally(() => {
        if (displayMessage) b.endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  updateExplorationConfig(projectId, explorationId, config, action = "updateConfig") {
    let code = b.startRequest("Updating exploration config");
    return axios
      .put(`${apiURL}explorations/${explorationId}`, config, {
        params: {
          project_id: projectId,
          action,
        },
      })
      .finally(() => {
        b.endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
  computeRealCombinations(projectId, explorationId, config) {
    return this.updateExplorationConfig(projectId, explorationId, config, "start");
  },
  cancelRealCombinationsComputation(projectId, explorationId) {
    let code = b.startRequest("Cancelling real combinations computation");
    return axios
      .put(`${apiURL}explorations/${explorationId}`, null, {
        params: {
          project_id: projectId,
          action: "stop",
        },
      })
      .finally(() => {
        b.endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // Statistics
  getColumnsStatistics(dataProviderId, projectId) {
    let code = b.startRequest("Loading columns statistics");
    return axios
      .get(
        `${apiURL}statistics/data-providers/${dataProviderId}/projects/${projectId}/columnsStatistics`
      )
      .finally(() => {
        b.endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },

  // Selections
  createSelection(projectId, explorationId, selectedCombinationsIds, selectionName) {
    let code = b.startRequest("Creating selection");
    return axios
      .post(
        `${apiURL}explorations/${explorationId}/selections`,
        {
          selection_name: selectionName,
          selected_combinations: selectedCombinationsIds,
        },
        {
          params: {
            project_id: projectId,
          },
        }
      )
      .finally(() => {
        b.endRequest(code);
      })
      .then((response) => {
        return response.data;
      });
  },
};
