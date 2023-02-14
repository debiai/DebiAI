let convertPlotlySelectionsToFilters = (data, intervales) => {
  let filters = [];

  intervales.forEach((inter) => {
    if (inter.constraintrange !== undefined) {
      let col = data.columns.find((col) => col.label == inter.label);
      let cr = inter.constraintrange;
      if (Array.isArray(cr[0]))
        cr.forEach((subInter) => {
          let newFilter = addIntervalSelection(col, subInter[0], subInter[1]);
          updateIntervals(filters, newFilter);
        });
      else {
        let newFilter = addIntervalSelection(col, cr[0], cr[1]);
        updateIntervals(filters, newFilter);
      }
    }
  });

  return filters;
};
export default {
  convertPlotlySelectionsToFilters,
};

let addIntervalSelection = (col, from, to) => {
  if (col.type == String) {
    let selectedString = col.uniques.filter((val, i) => i >= from && i <= to);
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

let updateIntervals = (filters, newFilter) => {
  // Construct an interval list from a filter and the created filters
  let createdFilter = filters.find((filter) => filter.columnIndex === newFilter.columnIndex);

  if (!createdFilter) {
    if (newFilter.type === "interval")
      // Create a new intelvals filter
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
