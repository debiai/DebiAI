const convertPlotlySelectionsToFilters = (data, intervals) => {
  const filters = [];

  intervals.forEach((inter) => {
    if (inter.constraintrange !== undefined) {
      const col = data.getColumnByLabel(inter.label);
      if (!col) return;

      const cr = inter.constraintrange;
      if (Array.isArray(cr[0]))
        cr.forEach((subInter) => {
          const newFilter = addIntervalSelection(col, subInter[0], subInter[1]);
          updateIntervals(filters, newFilter);
        });
      else {
        const newFilter = addIntervalSelection(col, cr[0], cr[1]);
        updateIntervals(filters, newFilter);
      }
    }
  });

  return filters;
};
export default {
  convertPlotlySelectionsToFilters,
};

const addIntervalSelection = (col, from, to) => {
  if (col.type == String) {
    const selectedString = col.uniques.filter((val, i) => i >= from && i <= to);
    return {
      type: "values",
      columnIndex: col.index,
      values: selectedString,
    };
  }

  return {
    type: "interval",
    columnIndex: col.index,
    min: from,
    max: to,
  };
};

const updateIntervals = (filters, newFilter) => {
  // Construct an interval list from a filter and the created filters
  const createdFilter = filters.find((filter) => filter.columnIndex === newFilter.columnIndex);

  if (!createdFilter) {
    if (newFilter.type === "interval")
      // Create a new intervals filter
      filters.push({
        type: "intervals",
        columnIndex: newFilter.columnIndex,
        intervals: [newFilter],
      });
    if (newFilter.type === "values") filters.push(newFilter);
  } else {
    if (newFilter.type === "interval")
      // Add the interval to the intervals filter
      createdFilter.intervals.push(newFilter);
    if (newFilter.type === "values")
      // Merge the values
      createdFilter.values = [...createdFilter.values, ...newFilter.values];
  }
};
