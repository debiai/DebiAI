export default {
  API_DEBIAI_URL: "/api/v1/",
  API_DATA_URL: "/api/v1/data/",
  API_ALGO_URL: "/api/v0/app/algo-providers/",  
  API_EXPLORATION_URL: "/api/v1/exploration/",
  AUTH_TOKEN_LOCAL_STORAGE_KEY: process.env.VUE_APP_AUTH_TOKEN_KEY || "debiai_auth_token"
  // To connect to API V0
  //API_DEBIAI_URL: "/api/v0/",
  //API_DATA_URL: "/api/v0/data-providers/",
  //API_ALGO_URL: "/api/v0/app/algo-providers/",  
  //API_EXPLORATION_URL: "/api/v0/exploration/"  
};
