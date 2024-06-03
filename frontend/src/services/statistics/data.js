class Data {
  constructor(data) {
    console.log("Data constructor called");
    console.log(data);
    this.categories = data.categories;
    this.labels = data.labels;
    this.nbColumns = data.nbColumns;
    this.nbLines = data.nbLines;
    this.nbLinesOriginal = data.nbLines;
    this.sampleIdList = data.sampleIdList;
    this.columns = data.columns.map((column) => new Column(this, column));

    this.verticallyUnfoldedColumnsIndexes = []; // Ordered list of unfolded columns

    this.selectedData = [...Array(this.nbLines).keys()];
  }

  // Column unfold
  unfoldColumn(columnIndex) {
    if (this.columns[columnIndex].typeText === "Dict") this.unfoldHorizontally(columnIndex);
    else if (this.columns[columnIndex].typeText === "Array") this.unfoldVertically(columnIndex);
  }
  unfoldVertically(columnIndex) {
    console.log("Expand vertically: ", columnIndex);
    // Add column to the unfolded list
    // Remove it from the unfolded list if it is already unfolded

    if (this.verticallyUnfoldedColumnsIndexes.includes(columnIndex)) {
      this.verticallyUnfoldedColumnsIndexes = this.verticallyUnfoldedColumnsIndexes.filter(
        (index) => index !== columnIndex
      );
    } else {
      this.verticallyUnfoldedColumnsIndexes.push(columnIndex);
    }

    this.updateDataBasedOn();
  }

  updateDataBasedOn() {
    console.log("Update nbLines");
    if (this.verticallyUnfoldedColumnsIndexes.length === 0) {
      this.nbLines = this.nbLinesOriginal;
      return;
    }

    const unfoldedColumn = this.columns[this.verticallyUnfoldedColumnsIndexes[0]];

    this.nbLines = unfoldedColumn.values.reduce((acc, value) => {
      return acc + value.length;
    }, 0);
    console.log("New NbLines: ", this.nbLines);
  }
  unfoldHorizontally(columnIndex) {
    console.log("Expand Horizontally: ", columnIndex);
    // TODO
  }
}

class Column {
  constructor(data, column) {
    this.data = data;
    this.category = column.category;
    // this.values = column.values;
    this.label = column.label;
    this.index = column.index;
    this.min = column.min;
    this.max = column.max;
    this.nbOccurrence = column.nbOccurrence;
    this.type = column.type;
    this.typeText = column.typeText;
    this.valuesIndex = column.valuesIndex;
    this.valuesIndexUniques = column.valuesIndexUniques;
    this.uniques = column.uniques;

    this.values = new Proxy(column.values, {
      get: (target, prop) => {
        if (prop === "length") return this.data.nbLines;
        if (prop === "map") return target.map;
        if (prop === "reduce") return target.reduce;
        return column.values[prop];
      },
    });
  }
}

console.log(Data);

export default {
  Data,
  Column,
};
