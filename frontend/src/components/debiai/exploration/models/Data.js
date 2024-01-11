// Data class for the exploration page
// Used by the different to display results

import { Column } from "./Column";
import { Combination } from "./Combination";

import backendDialog from "@/services/backendDialog";

export default class Data {
  constructor(columns) {
    // Init columns
    this.columns = columns.map((column, i) => {
      return new Column(column, i);
    });

    this.selectedColumns = [];

    // Init metrics
    this.globalMetrics = [{ name: "nbData", type: "number", index: 0 }];

    // Init combinations
    this.combinations = [];
  }

  async selectColumns(columnIndexes) {
    this.selectedColumns = columnIndexes.map((index) => {
      return this.columns[index];
    });
    await this.computeCombinations();
  }

  async computeCombinations() {
    // Compute combinations
    this.combinations = [];

    // Build request parameters
    const parameters = [];

    this.selectedColumns.forEach((column) => {
      parameters.push({
        name: column.name,
        nbChunks: column.nbChunks,
      });
    });

    const metrics = await backendDialog.getColumnsCombinatorialMetrics(parameters);
    this.combinations = metrics.combinations.map((combination, i) => {
      console.log(combination);
      return new Combination(i, combination.combination, combination.metrics.nbValues);
    });

    // if (metrics.totalCombinations > metrics.combinations.length)
    //   this.tooManyCombinationsWarning = true;

    // this.nbCombinations = metrics.totalCombinations;
    // this.nonNullCombinations = this.combinationsMetrics.filter((c) => c.metrics.nbValues > 0);
    // // Add an index to each combination
    // this.nonNullCombinations = this.nonNullCombinations.map((c, i) => {
    //   c.index = i;
    //   return c;
    // });

    // this.drawPlot();
  }
}
