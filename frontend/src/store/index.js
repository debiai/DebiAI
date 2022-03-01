import Vue from 'vue'
import Vuex from 'vuex'

import Request from './request';
import services from "../services/services"

Vue.use(Vuex)

const Dashboard = {
  state: {
    // Global variables
    categoryList: ["inputs", "groundTruth", "contexts", "others", "tag"],

    // Dashboard
    isLoadding: false,
    messages: [], // List of messages for the user
    requests: [], // Request pending to the backend
  },
  mutations: {
    setLoading(state, val) {
      state.isLoadding = val
    },
    // message
    sendMessage(state, msg) {
      msg.id = services.uuid()
      state.messages.push(msg)
      setTimeout(() => {
        state.messages = state.messages.filter(m => m.id != msg.id)
      }, 5000)
    },
    removeMessage(state, msg) {
      state.messages = state.messages.filter(m => m != msg)
    },

    // request
    startRequest(state, { name, code, progress }) {
      let newRequest = new Request(name, code, progress)
      state.requests.push(newRequest)
    },
    endRequest(state, code) {
      state.requests = state.requests.filter(r => r.code !== code)
    },
    updateRequestProgress(state, { code, progress }) {
      state.requests.find(r => r.code == code).progress = progress
    },
  }
}

const ProjectPage = {
  state: {
    projectId: null,
    blockLevels: [],
    columns: [],
  },
  mutations: {
    setProjectId(state, projectId) {
      state.projectId = projectId
    },
    setBlockLevels(state, blockLevels) {
      state.blockLevels = blockLevels

      let blockCat = Dashboard.state.categoryList;

      let columns = [];
      if (blockLevels) {


        blockLevels.forEach((block) => {
          // Add id columns
          columns.push({ name: block.name, type: 'text', isId: true })

          // Add other columns
          blockCat.forEach((category) => {
            if (category in block) {
              block[category].forEach((column) => {
                columns.push(column);
              });
            }
          });
        });

        // sort columns by name
        // columns.sort((a, b) => {
        //   if (a.name.toUpperCase() > b.name.toUpperCase()) return 1;
        //   if (a.name.toUpperCase() < b.name.toUpperCase()) return -1;
        //   return 0;
        // });
      }


      state.columns = columns;
    }
  }
}

const SatisticalAnasysis = {
  state: {
    // Analysis
    projectId: null,
    // selectedSelectionIds: null,

    // Color
    coloredColumnIndex: 0,

    // Filters
    filters: [],
    filtersEffecs: []
  },
  mutations: {
    selectProjectId(state, projectId) {
      state.projectId = projectId
    },
    // setSelectedSelectionIds(state, selectionIds) {
    //   state.selectedSelectionIds = selectionIds
    // },
    setColoredColumnIndex(state, index) {
      state.coloredColumnIndex = state.coloredColumnIndex == index ? null : index
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

      let toSave = payload.filters.map(filter => {
        return {
          id: services.uuid(),
          from: payload.from,
          ...filter,
          creationDate: services.getTimestamp()
        }
      });

      // Find duplicate
      if (payload.removeExisting)
        state.filters = state.filters.filter(filter =>
          filter.from.widgetIndex !== payload.from.widgetIndex
        )

      state.filters = [...state.filters, ...toSave]
    },
    setFiltersEffects(state, filtersEffecs) {
      state.filtersEffecs = filtersEffecs
    },
    clearAllFilters(state) {
      state.filters = []
    },
    removeFilter(state, filterId) {
      state.filters = state.filters.filter(filter => filter.id !== filterId);
    },
    invertFilter(state, filterId) {
      let filter = state.filters.find(filter => filter.id === filterId);
      if (filter) {
        if (filter.inverted) filter.inverted = false;
        else filter.inverted = true;
        // Recreating the array to trigger event
        state.filters = [...state.filters]
      }
    },
    // Values filter
    addValueToFilter(state, { filterId, value }) {
      let filter = state.filters.find(filter => filter.id === filterId);
      if (filter && filter.type == "values") {
        filter.values.push(value)
        // TODO: check if no duplicates
        // Recreating the array to trigger event
        state.filters = [...state.filters]
      }
    },
    removeValueFromFilter(state, { filterId, value }) {
      let filter = state.filters.find(filter => filter.id === filterId);
      if (filter && filter.type == "values") {
        filter.values = filter.values.filter(val => val !== value)
        // Recreating the array to trigger event
        state.filters = [...state.filters]
      }
    },
    // Intervals filter
    addIntervalToFilter(state, { filterId, interval }) {
      if (interval.min !== null || interval.max !== null) {
        let filter = state.filters.find(filter => filter.id === filterId);
        if (filter && filter.type == "intervals") {
          filter.intervals.push(interval)
          // TODO: check if no duplicates or redondent
          // Recreating the array to trigger event
          state.filters = [...state.filters]
        }
      }
    },
    removeIntervalFromFilter(state, { filterId, intervalIndex }) {
      let filter = state.filters.find(filter => filter.id === filterId);
      if (filter && filter.type == "intervals") {
        filter.intervals.splice(intervalIndex, 1);
        // Recreating the array to trigger event
        state.filters = [...state.filters]
      }
    }
  }

}


export default new Vuex.Store({
  modules: {
    Dashboard,
    ProjectPage,
    SatisticalAnasysis
  }
})
