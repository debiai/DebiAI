import config from "../../config";

/**
 * Authentication service that handles bearer token from local storage
 */
export default {
  /**
   * Get the bearer token from local storage
   * @returns {string|null} The bearer token or null if not found
   */
  getAuthToken() {
    try {
      const token = localStorage.getItem(config.AUTH_TOKEN_LOCAL_STORAGE_KEY);
      return token;
    } catch (error) {
      console.warn("No auth token from local storage");
      return null;
    }
  },

  /**
   * Get the Authorization header for HTTP requests
   * @returns {object} Authorization header object or empty object
   */
  getAuthHeader() {
    const token = this.getAuthToken();
    if (token) {
      return {
        Authorization: `Bearer ${token}`,
      };
    }
    return {};
  },
};
