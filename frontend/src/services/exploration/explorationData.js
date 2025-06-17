import Data from "@/services/statistics/data";

class ExplorationData extends Data.Data {
  constructor(explorationObject) {
    console.log("Creating ExplorationData with explorationObject", explorationObject);

    // ExplorationObject important fields:
    // combinations: Array(109) [ {…}, {…}, {…}, … ]
    //  -> {
    //       combinations: Array(7) [ "2018", "508SW", "A", … ]
    //       sample_ids: Array(87) [ "A", "B", "C", … ]
    //     }
    //  The computed combinations of the exploration.
    // metrics: Object { … }
    //  -> {
    //       "Nb Samples": { values: Array(109) [ 87, 87, 87, … ] },
    //       ...
    //     }
    // config: Object { … }
    //  -> columns: Array(7) [ {…}, {…}, {…}, … ]
    //       -> {
    //            label: "Year",
    //            aggregation: {...},
    //          }

    const dataBuilder = {
      columns: [],
      nbLines: explorationObject.combinations.length,
    };

    // Make some columns from the explorationObject config
    dataBuilder.columns = explorationObject.config.columns.map((col, colIndex) => {
      // Build the column values for the combinations
      const colValues = explorationObject.combinations.map((combination) => {
        return combination.combination[colIndex];
      });
      return {
        label: col.label,
        values: colValues,
        category: "context",
        typeIn: null,
        group: null,
      };
    });

    // Add the metrics columns
    for (const metricLabel in explorationObject.metrics) {
      const metricValues = explorationObject.metrics[metricLabel].values;
      dataBuilder.columns.push({
        label: metricLabel,
        values: metricValues,
        category: "metric",
        typeIn: null,
        group: null,
      });
    }

    // Setup the Data class
    super(dataBuilder);

    this.combinations = explorationObject.combinations;
    this.mode = "exploration";
  }
}

export default { ExplorationData };
