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
    // config: Object { … }
    //  -> selectedColumns: Array(7) [ "Record", "Car", "person", … ]

    const dataBuilder = {
      columns: [],
      categories: [""],
      nbLines: explorationObject.combinations.length,
    };

    // Make some columns from the explorationObject config
    dataBuilder.columns = explorationObject.config.selectedColumns.map((colLabel, colIndex) => {
      // Build the column values for the combinations
      console.log("Building column:", colLabel, "at index:", colIndex);

      const colValues = explorationObject.combinations.map((combination) => {
        return combination.combination[colIndex];
      });
      return {
        label: colLabel,
        values: colValues,
        category: "context",
        typeIn: null,
        group: null,
      };
    });

    // Set the labels from the sample_ids
    dataBuilder.labels = explorationObject.config.selectedColumns;

    super(dataBuilder);

    this.combinations = explorationObject.combinations;
    this.mode = "exploration";
  }
}

export default { ExplorationData };
