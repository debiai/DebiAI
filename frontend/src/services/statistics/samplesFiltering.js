// This service is used by the Filters component to
// get selected data samples ids from a filter list

let getSelected = (filters, data) => {
  let selectedSampleIds = [...Array(data.nbLines).keys()]; // Stars with 100%
  let filtersEffects = {}; // number of samples left for each filters

  filters.forEach((filter) => {
    let column = data.columns.find((c) => c.index == filter.columnIndex);

    if (!column) {
      console.error("Column index not found: " + filter.columnIndex);
      return;
    }

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

  return { selectedSampleIds, filtersEffects };
};

let getSelectedSamplesIdsFromValuesFilter = (filter, selectedSampleIds, column) => {
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

let getSelectedSamplesIdsFromIntervalsFilter = (filter, selectedSampleIds, col) => {
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

  if (filter.inverted)
    return selectedSampleIds.filter(
      (sampleId) => !selectedSampleIdsFromIntervals.includes(sampleId)
    );
  return selectedSampleIdsFromIntervals;
};

let getSelectedSamplesIdsFromIntervalFilter = (interval, selectedSampleIds, col, inverted) => {
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
};
