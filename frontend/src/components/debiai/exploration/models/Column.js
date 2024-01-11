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
