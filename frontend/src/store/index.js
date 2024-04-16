import Vue from "vue";
import Vuex from "vuex";

import Request from "./request";
import services from "../services/services";

Vue.use(Vuex);

const Dashboard = {
  state: {
    // Global variables
    categoryList: ["input", "groundtruth", "context", "other"],

    // Dashboard
    isLoading: false,
    messages: [], // List of messages for the user
    requests: [], // Request pending to the backend
  },
  mutations: {
    setLoading(state, val) {
      state.isLoading = val;
    },
    // message
    sendMessage(state, msg) {
      msg.id = services.uuid();
      state.messages.push(msg);
      setTimeout(() => {
        state.messages = state.messages.filter((m) => m.id != msg.id);
      }, 5000);
    },
    removeMessage(state, msg) {
      state.messages = state.messages.filter((m) => m != msg);
    },

    // request
    startRequest(state, { name, code, progress, cancelCallback }) {
      let newRequest = new Request(name, code, progress, cancelCallback);
      state.requests.push(newRequest);
    },
    endRequest(state, code) {
      state.requests = state.requests.filter((r) => r.code !== code);
    },
    updateRequestProgress(state, { code, progress }) {
      const request = state.requests.find((r) => r.code == code);
      if (!request) return;
      request.progress = progress;
    },
    updateRequestQuantity(state, { code, quantity }) {
      const request = state.requests.find((r) => r.code == code);
      if (!request) return;
      request.quantity = quantity;
    },
    cancelRequest(state, code) {
      const request = state.requests.find((r) => r.code == code);
      if (!request) return;
      request.cancel();
      // Remove request
      state.requests = state.requests.filter((r) => r.code !== code);
    },
  },
};

const ProjectPage = {
  state: {
    projectId: null,
    projectName: null,
    dataProviderId: null,
    selectionsIds: [],
    projectColumns: [],
    projectResultsColumns: [],
    dataProviderInfo: null,
    enableCache: true,
  },
  mutations: {
    setProjectId(state, projectId) {
      state.projectId = projectId;
    },
    setProjectName(state, projectName) {
      state.projectName = projectName;
    },
    setDataProviderId(state, dataProviderId) {
      state.dataProviderId = dataProviderId;
    },
    setProjectColumns(state, projectColumns) {
      state.projectColumns = projectColumns;
    },
    setProjectResultsColumns(state, projectResultsColumns) {
      state.projectResultsColumns = projectResultsColumns;
    },
    setSelectionsIds(state, selectionsIds) {
      if (selectionsIds) state.selectionsIds = selectionsIds;
      else state.selectionsIds = [];
    },
    setDataProviderInfo(state, dataProviderInfo) {
      state.dataProviderInfo = dataProviderInfo;
    },
    setUseCache(state, useCache) {
      state.enableCache = useCache;
    },
  },
};

const StatisticalAnalysis = {
  state: {
    // Color
    coloredColumnIndex: 0,

    // Filters
    filters: [],
    filtersEffects: [],

    // AlgoProviders
    experiments: {}, // Format: { algoProviderName: { algoId: [experiment]} }
    nbExperiments: 0, // To help with reactivity

    // Open widget id
    openedWidgetMenuId: null,
  },
  mutations: {
    setColoredColumnIndex(state, index) {
      state.coloredColumnIndex = state.coloredColumnIndex == index ? null : index;
    },

    // Filters
    addFilters(state, payload) {
      // payload :
      // {
      //   filters: [
      //     { type: "values",   columnIndex, values: [] },
      //     { type: "intervals", columnIndex, intervals: [] },
      //     { type: "interval", columnIndex, min, max },
      //   ]
      //   from: { widgetType, widgetName, widgetIndex },
      //   removeExisting: true
      // }

      // Storage
      // [{ id, from, type, creationDate, columnIndex, intervals, values, min, max}, ... ]

      if (!payload.filters) return;

      let toSave = payload.filters.map((filter) => {
        return {
          id: services.uuid(),
          from: payload.from,
          ...filter,
          creationDate: services.getTimestamp(),
        };
      });

      // Find duplicate
      if (payload.removeExisting)
        state.filters = state.filters.filter(
          (filter) => filter.from.widgetIndex !== payload.from.widgetIndex
        );

      state.filters = [...state.filters, ...toSave];
    },
    setFiltersEffects(state, filtersEffects) {
      state.filtersEffects = filtersEffects;
    },
    clearAllFilters(state) {
      state.filters = [];
    },
    removeFilter(state, filterId) {
      state.filters = state.filters.filter((filter) => filter.id !== filterId);
    },
    invertFilter(state, filterId) {
      let filter = state.filters.find((filter) => filter.id === filterId);
      if (filter) {
        if (filter.inverted) filter.inverted = false;
        else filter.inverted = true;
        // Recreating the array to trigger event
        state.filters = [...state.filters];
      }
    },
    // Values filter
    addValueToFilter(state, { filterId, value }) {
      let filter = state.filters.find((filter) => filter.id === filterId);
      if (filter && filter.type == "values") {
        // Check if value is not already in the array
        if (filter.values.find((val) => val === value)) return;

        filter.values.push(value);

        // Recreating the array to trigger event
        state.filters = [...state.filters];
      }
    },
    removeValueFromFilter(state, { filterId, value }) {
      let filter = state.filters.find((filter) => filter.id === filterId);
      if (filter && filter.type == "values") {
        filter.values = filter.values.filter((val) => val !== value);
        // Recreating the array to trigger event
        state.filters = [...state.filters];
      }
    },
    // Intervals filter
    addIntervalToFilter(state, { filterId, interval }) {
      if (interval.min !== null || interval.max !== null) {
        let filter = state.filters.find((filter) => filter.id === filterId);
        if (filter && filter.type == "intervals") {
          filter.intervals.push(interval);

          // Recreating the array to trigger event
          state.filters = [...state.filters];
        }
      }
    },
    removeIntervalFromFilter(state, { filterId, intervalIndex }) {
      let filter = state.filters.find((filter) => filter.id === filterId);
      if (filter && filter.type == "intervals") {
        filter.intervals.splice(intervalIndex, 1);
        // Recreating the array to trigger event
        state.filters = [...state.filters];
      }
    },

    // AlgoProviders
    addExperiment(state, { algoProviderName, algoId, experiment }) {
      state.nbExperiments++;
      if (!state.experiments[algoProviderName]) state.experiments[algoProviderName] = {};
      if (!state.experiments[algoProviderName][algoId])
        state.experiments[algoProviderName][algoId] = [];

      // add an id to the experiment
      experiment.id = services.uuid();
      experiment.nb = state.nbExperiments;
      state.experiments[algoProviderName][algoId].push(experiment);
    },

    deleteExperiment(state, experimentId) {
      // Delete experiment
      for (let algoProviderName in state.experiments) {
        for (let algoId in state.experiments[algoProviderName]) {
          state.experiments[algoProviderName][algoId] = state.experiments[algoProviderName][
            algoId
          ].filter((experiment) => experiment.id !== experimentId);
        }
      }

      // Update for reactivity
      state.experiments = { ...state.experiments };
    },

    // Open widget id
    setOpenedWidgetMenuId(state, widgetId) {
      state.openedWidgetMenuId = widgetId;
    },
  },
  getters: {
    getAlgoExperiments: (state) => (algoProviderName, algoId) => {
      if (state.experiments[algoProviderName] && state.experiments[algoProviderName][algoId])
        return state.experiments[algoProviderName][algoId];
      else return [];
    },
    getAlgoNbExperiments: (state) => (algoProviderName, algoId) => {
      if (state.experiments[algoProviderName] && state.experiments[algoProviderName][algoId])
        return state.experiments[algoProviderName][algoId].length;
      else return 0;
    },
  },
};

export default new Vuex.Store({
  modules: {
    Dashboard,
    ProjectPage,
    StatisticalAnalysis,
  },
});
