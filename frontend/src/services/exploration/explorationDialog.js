import axios from "axios";
import config from "../../../config";
import b from "../backendDialog";
import cacheService from "../cacheService";

const apiURL = config.API_EXPLORATION_URL;

// Hash-based cache utility for exploration API requests
async function requestWithHashCache(url, cacheKey, requestOptions = {}) {
  try {
    // Get cached response if exists
    const cachedData = await cacheService.getHashResponse(cacheKey);

    // Prepare request parameters
    const params = { ...requestOptions.params };
    if (cachedData && cachedData.hash) {
      params.prev_hash_content = cachedData.hash;
    }

    const response = await axios.get(url, { ...requestOptions, params });

    // If status is 304 (Not Modified), return cached response
    if (response.status === 304 && cachedData) {
      console.log(`Cache hit for ${cacheKey} - using cached response`);
      return cachedData.response;
    }

    // If status is 200, save new hash and response
    if (response.status === 200 && response.data.hash_content) {
      await cacheService.saveHashResponse(cacheKey, response.data.hash_content, response.data);
      console.log(`Cache updated for ${cacheKey} with new hash: ${response.data.hash_content}`);
    }

    return response.data;
  } catch (error) {
    // If request fails and we have cached data, return it
    const cachedData = await cacheService.getHashResponse(cacheKey);
    if (cachedData) {
      console.warn(`API request failed for ${cacheKey}, using cached data`, error);
      return cachedData.response;
    }
    throw error;
  }
}

function getCachedRequest(url, cacheKey, requestName, requestOptions = {}) {
  let code = b.startRequest(requestName);
  return requestWithHashCache(url, cacheKey, requestOptions).finally(() => {
    b.endRequest(code);
  });
}

export default {
  // Explorations
  getExplorations(projectId, displayMessage = true) {
    const cacheKey = `explorations_${projectId}`;
    const requestOptions = {
      params: {
        project_id: projectId,
      },
    };

    if (displayMessage) {
      return getCachedRequest(
        `${apiURL}explorations`,
        cacheKey,
        "Getting explorations",
        requestOptions
      ).then((data) => data.explorations || data);
    } else {
      // For non-display requests, use the cache utility directly
      return requestWithHashCache(`${apiURL}explorations`, cacheKey, requestOptions).then(
        (data) => data.explorations || data
      );
    }
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
    // TODO : loic projectId not needed
    let code = b.startRequest("Deleting exploration");
    return axios
      .delete(`${apiURL}explorations/${explorationId}`, {
        params: {},
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
    const cacheKey = `exploration_${projectId}_${explorationId}`;
    const requestOptions = {
      params: {
        project_id: projectId,
      },
    };

    if (displayMessage) {
      return getCachedRequest(
        `${apiURL}explorations/${explorationId}`,
        cacheKey,
        "Getting exploration",
        requestOptions
      ).then((data) => data.exploration || data);
    } else {
      // For non-display requests, use the cache utility directly
      return requestWithHashCache(
        `${apiURL}explorations/${explorationId}`,
        cacheKey,
        requestOptions
      ).then((data) => data.exploration || data);
    }
  },
  updateExplorationConfig(projectId, explorationId, config, action = "updateConfig") {
    let code = b.startRequest("Updating exploration config");
    // TODO : loic projectId not needed
    return axios
      .put(`${apiURL}explorations/${explorationId}`, config, {
        params: {
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
    // TODO : loic projectId not needed
    return axios
      .put(`${apiURL}explorations/${explorationId}`, null, {
        params: {
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
    // TODO : Not needed to remove
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
    // TODO : loic projectId not needed
    return axios
      .post(
        `${apiURL}explorations/${explorationId}/selections`,
        {
          selection_name: selectionName,
          selected_combinations: selectedCombinationsIds,
        },
        {
          params: {},
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
