// Data class for the exploration page
// Used by the different to display results

export default class Data {
  constructor(columns) {
    this.columns = columns.map((column, i) => {
      return new Column(column, i);
    });
    this.nbColumns = columns.length;

    this.globalMetrics = [{ name: "nbData", type: "number", index: 0}];
  }
}

export class Column {
  constructor(column, index) {
    this.name = column.name;
    this.index = index;
    this.type = column.type;
    this.category = column.category;
    this.nbUniqueValues = column.nbUniqueValues;
    this.nbUniqueAggregations = this.nbUniqueValues;
    this.nbMetrics = 0;
  }
}
