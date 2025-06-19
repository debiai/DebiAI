import Data from "@/services/statistics/data";

class ExplorationData extends Data.Data {
  constructor(explorationObject) {
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

      // Define the category of the column
      let category = "project column"
      if (col.aggregation) category = "aggregation"

      return {
        label: col.label,
        values: colValues,
        category: category,
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

    this.mode = "exploration";
    this.explorationId = explorationObject.id
    this.explorationName = explorationObject.name
    this.combinations = explorationObject.combinations;
    this.nbExplorationSelectedSamples = 0;
    this.nbSamplesMetric = explorationObject.metrics["Nb Samples"]["values"];
    this.projectNbSamples = this.nbSamplesMetric.reduce((acc, nbSamples) => acc + nbSamples, 0);
    this.calculateNbSelectedSamples();
  }

  calculateNbSelectedSamples() {
    // Count the 'Nb Samples' values of all of the selected combinations
    this.nbExplorationSelectedSamples = this.selectedData.reduce((acc, combinationIndex) => {
      return acc + this.nbSamplesMetric[combinationIndex];
    }, 0);
  }

  updateFilters(ignoreCache = false) {
    super.updateFilters(ignoreCache);

    this.calculateNbSelectedSamples();
  }
}

export default { ExplorationData };
