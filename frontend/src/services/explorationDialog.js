import axios from "axios";
import config from "../../config";
import b from "./backendDialog";

const apiURL = config.EXPLORATION_API_URL;

export default {
  // Explorations
  getExplorations(projectId) {
    let code = b.startRequest("Getting explorations");
    return axios
      .get(`${apiURL}explorations`, {
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
  getExploration(projectId, explorationId) {
    let code = b.startRequest("Getting exploration");
    return axios
      .get(`${apiURL}explorations/${explorationId}`, {
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
  }
};
