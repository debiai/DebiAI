// This service is used by the Filters component to
// get selected data samples ids from a filter list

let previouslyAppliedFilters = null;
let previousSelectedSampleIds = null;
let previousFiltersEffects = null;

function deepEqual(obj1, obj2) {
  if (obj1 === obj2) return true;

  if (obj1 && obj2 && typeof obj1 === "object" && typeof obj2 === "object") {
    if (Object.keys(obj1).length !== Object.keys(obj2).length) {
      return false;
    }

    for (let key in obj1) {
      if (Object.prototype.hasOwnProperty.call(obj1, key) && !deepEqual(obj1[key], obj2[key])) {
        return false;
      }
    }

    return true;
  }

  return false;
}

const extractRelevantParts = (filters) => {
  // Sort
  return filters.map((filter) => {
    const f = {
      columnIndex: filter.columnIndex,
    };
    if (filter.values) f.values = filter.values;
    if (filter.intervals) f.intervals = filter.intervals;
    return f;
  });
};

const sortFiltersByColumnIndex = (filters) => {
  return filters.slice().sort((a, b) => (a.columnIndex > b.columnIndex ? 1 : -1));
};

const shouldFilter = (newFilters) => {
  const newRelevantFilters = extractRelevantParts(newFilters);
  const sortedNewRelevantFilters = sortFiltersByColumnIndex(newRelevantFilters);

  if (deepEqual(previouslyAppliedFilters, sortedNewRelevantFilters)) {
    return false;
  } else {
    previouslyAppliedFilters = JSON.parse(JSON.stringify(newRelevantFilters)); // Deep copy the relevant parts of the new filters
    return true;
  }
};

const clearCache = () => {
  previouslyAppliedFilters = null;
  previousSelectedSampleIds = null;
  previousFiltersEffects = null;
};

const getSelected = (filters, data) => {
  if (!shouldFilter(filters))
    return { selectedSampleIds: previousSelectedSampleIds, filtersEffects: previousFiltersEffects };

  let selectedSampleIds = [...Array(data.nbLines).keys()]; // Stars with 100%
  const filtersEffects = {}; // number of samples left for each filters

  filters.forEach((filter) => {
    const column = data.getColumn(filter.columnIndex);
    if (!column) return;

    if (filter.type == "values")
      selectedSampleIds = getSelectedSamplesIdsFromValuesFilter(filter, selectedSampleIds, column);
    else if (filter.type == "intervals")
      selectedSampleIds = getSelectedSamplesIdsFromIntervalsFilter(
        filter,
        selectedSampleIds,
        column
      );
    else if (filter.type == "interval")
      selectedSampleIds = getSelectedSamplesIdsFromIntervalFilter(
        filter,
        selectedSampleIds,
        column
      );

    filtersEffects[filter.id] = selectedSampleIds.length;
  });

  // Save the selected samples ids and the filters effects for caching
  previousSelectedSampleIds = selectedSampleIds;
  previousFiltersEffects = filtersEffects;

  return { selectedSampleIds, filtersEffects };
};

const getSelectedSamplesIdsFromValuesFilter = (filter, selectedSampleIds, column) => {
  // Filter the selected samples ids
  // If one of the column value is in the filter values, the sample is selected
  if (filter.values.length > 0) {
    if (filter.inverted)
      return selectedSampleIds.filter(
        (sampleId) => !filter.values.includes(column.values[sampleId])
      );
    else
      return selectedSampleIds.filter((sampleId) =>
        filter.values.includes(column.values[sampleId])
      );
  }
  return selectedSampleIds;
};

const getSelectedSamplesIdsFromIntervalsFilter = (filter, selectedSampleIds, col) => {
  if (filter.intervals.length == 0) return selectedSampleIds;

  if (filter.intervals.length == 1)
    return getSelectedSamplesIdsFromIntervalFilter(
      filter.intervals[0],
      selectedSampleIds,
      col,
      filter.inverted
    );

  // Get all the selected samples from the requests
  let selectedSampleIdsFromIntervals = [].concat(
    ...filter.intervals.map((interval) =>
      getSelectedSamplesIdsFromIntervalFilter(interval, selectedSampleIds, col, false)
    )
  );

  // Remove duplicates
  const selectedSampleIdsFromIntervalsSet = new Set(selectedSampleIdsFromIntervals);
  selectedSampleIdsFromIntervals = [...selectedSampleIdsFromIntervalsSet];

  if (filter.inverted)
    return selectedSampleIds.filter(
      (sampleId) => !selectedSampleIdsFromIntervals.includes(sampleId)
    );
  return selectedSampleIdsFromIntervals;
};

const getSelectedSamplesIdsFromIntervalFilter = (interval, selectedSampleIds, col, inverted) => {
  if (inverted) {
    if (interval.max !== null && interval.min !== null)
      return selectedSampleIds.filter(
        (sampleId) => col.values[sampleId] < interval.min || col.values[sampleId] > interval.max
      );
    else if (interval.max !== null)
      return selectedSampleIds.filter((sampleId) => col.values[sampleId] > interval.max);
    else if (interval.min !== null)
      return selectedSampleIds.filter((sampleId) => col.values[sampleId] < interval.min);
    return selectedSampleIds;
  } else {
    if (interval.max !== null && interval.min !== null)
      return selectedSampleIds.filter(
        (sampleId) => col.values[sampleId] >= interval.min && col.values[sampleId] <= interval.max
      );
    else if (interval.max !== null)
      return selectedSampleIds.filter((sampleId) => col.values[sampleId] <= interval.max);
    else if (interval.min !== null)
      return selectedSampleIds.filter((sampleId) => col.values[sampleId] >= interval.min);
    return selectedSampleIds;
  }
};

export default {
  getSelected,
  clearCache,
};
