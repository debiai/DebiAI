import services from "../services";
import store from "../../store";
import samplesFiltering from "./samplesFiltering";

class Data {
  constructor(data) {
    this.mode = "analysis";
    this.nbLinesOriginal = data.nbLines;
    this.sampleIdList = data.sampleIdList;

    // Register selected data variables
    this.nbLines = this.nbLinesOriginal;
    this.selectedData = [...Array(this.nbLinesOriginal).keys()];
    this.nbOriginalSelectedData = this.nbLinesOriginal;

    // Register unfold variables
    this.verticallyUnfoldedColumnsIndexes = []; // Ordered list of unfolded columns
    this.virtualIndexMapping = {}; // Mapping between virtual index and original index

    // Register the columns
    this.columns = [];

    data.columns.forEach((column) => {
      this.addColumn({
        label: column.label,
        values: column.values,
        category: column.category,
        typeIn: column.type,
        group: column.group,
      });
    });

    samplesFiltering.clearCache();
  }

  // Filters
  updateFilters(ignoreCache = false) {
    // Update the selected samples from the stored filters
    const filters = store.state.StatisticalAnalysis.filters;

    // Remove the filters that are on columns that don't exist anymore
    filters.forEach((filter) => {
      if (!this.columnExists(filter.columnIndex)) store.commit("removeFilter", filter.id);
    });

    try {
      // Update the selected samples based on the filters
      let { selectedSampleIds, filtersEffects } = samplesFiltering.getSelected(
        filters,
        this,
        ignoreCache
      );

      // Update the selected data only if the selected samples have changed
      const selectedDataChanged = (previousSelectedData, newSelectedData) => {
        if (previousSelectedData.length !== newSelectedData.length) return true;
        for (let i = 0; i < previousSelectedData.length; i++)
          if (previousSelectedData[i] !== newSelectedData[i]) return true;
        return false;
      };

      if (selectedDataChanged(this.selectedData, selectedSampleIds)) {
        this.selectedData = selectedSampleIds;
        store.commit("setFiltersEffects", filtersEffects);
      }
    } catch (error) {
      console.error(error);
      store.commit("sendMessage", {
        title: "error",
        msg: "Error while filtering the samples",
      });
    }

    this.nbOriginalSelectedData = this.getOriginalSelectedData().length;
  }
  getOriginalSelectedData() {
    // Unfolding the data will change the number of lines
    // This function will get the selected original data from the selected virtual data
    if (this.currentlyUnfoldedVertically()) {
      const originalSelectedData = {};
      this.selectedData.forEach((sampleNumber) => {
        let mapping = this.virtualIndexMapping[sampleNumber];
        while (mapping.depth > 0 || !mapping) mapping = mapping.parentMapping;
        if (mapping) originalSelectedData[mapping.originalIndex] = true;
      });
      return Object.keys(originalSelectedData);
    } else return this.selectedData;
  }

  // Column utils
  get nbColumns() {
    return this.columns.length;
  }
  columnExists(columnIndex) {
    return this.getColumn(columnIndex) !== undefined;
  }
  getColumn(columnIndex) {
    return this.columns.find((column) => column.index === columnIndex);
  }
  getColumnExistingColumns(columnIndexes) {
    return columnIndexes.map((index) => this.getColumn(index)).filter((column) => column);
  }
  getColumnExistingColumnsLabels(columnIndexes) {
    return this.getColumnExistingColumns(columnIndexes).map((column) => column.label);
  }
  getColumnByLabel(label) {
    return this.columns.find((column) => column.label === label);
  }
  getColumnByLabelAndCategory(label, category) {
    return this.columns.find((column) => column.label === label && column.category === category);
  }
  addColumn({ label, values, category, typeIn = null, group = null, parentColumnIndex = null }) {
    const unfoldedLevel = this.verticallyUnfoldedColumnsIndexes.length;
    const columnId = services.uuid();
    this.columns.push(
      new Column(
        this,
        columnId,
        label,
        values,
        category,
        typeIn,
        group,
        unfoldedLevel,
        parentColumnIndex
      )
    );
  }
  removeColumns(columnIndexes) {
    columnIndexes.forEach((columnIndex) => this.removeColumn(columnIndex));
  }
  removeColumn(columnIndex) {
    const column = this.getColumn(columnIndex);
    if (!column) return;

    // Remove from the unfolded list
    this.verticallyUnfoldedColumnsIndexes = this.verticallyUnfoldedColumnsIndexes.filter(
      (index) => index !== columnIndex
    );

    // Remove the column children
    this.removeColumns(this.columns.filter((column) => column.parentColumnIndex === columnIndex));

    // Remove the column
    this.columns = this.columns.filter((column) => column.index !== columnIndex);
    column.clean();
  }

  // Column unfold
  currentlyUnfoldedVertically() {
    // Return true if at least one column is unfolded
    return this.verticallyUnfoldedColumnsIndexes?.length > 0;
  }
  unfoldVertically(columnIndex) {
    // Get the column to unfold
    const unfoldedColumn = this.getColumn(columnIndex);
    if (!unfoldedColumn || unfoldedColumn.typeText !== "Array") return;

    // Check if we unfold at the end of the list or in the middle
    const currentUnfoldedLevel = this.verticallyUnfoldedColumnsIndexes.length;
    if (unfoldedColumn.unfoldedLevel === currentUnfoldedLevel) {
      // We can unfold the column
      // Add column to the unfolded list
      this.verticallyUnfoldedColumnsIndexes.push(columnIndex);
    } else if (unfoldedColumn.unfoldedLevel < currentUnfoldedLevel) {
      // We are unfolding a different column
      // Remove the columns that are unfolded after the selected column
      this.verticallyUnfoldedColumnsIndexes = this.verticallyUnfoldedColumnsIndexes.filter(
        (index) => {
          this.getColumn(index).unfoldedLevel <= unfoldedColumn.unfoldedLevel;
        }
      );

      // Add column to the unfolded list
      this.verticallyUnfoldedColumnsIndexes.push(columnIndex);
    }

    // Set / reset what columns are unfolded
    this.resetUnfoldedColumns();

    // Add the column that is generated by the unfolding
    const column_values = new Array(this.nbLines).fill(null).map((_, i) => {
      const originalIndex = this.virtualIndexMapping[i].originalIndex;
      const valueIndex = this.virtualIndexMapping[i].valueIndex;
      return unfoldedColumn.originalValues[originalIndex][valueIndex];
    });

    const new_label =
      unfoldedColumn.unfoldedLevel > 0 ? unfoldedColumn.label + "ᛨ" : unfoldedColumn.label + " ᛨ"; // Add a space before the arrow if first unfold

    this.addColumn({
      label: new_label,
      values: column_values,
      category: unfoldedColumn.category,
      typeIn: unfoldedColumn.typeText,
      group: null,
      parentColumnIndex: columnIndex,
    });
  }
  foldVertically(columnIndex) {
    // Get the column to fold
    const unfoldedColumn = this.getColumn(columnIndex);
    if (!unfoldedColumn || unfoldedColumn.typeText !== "Array") return;

    // Check if the column is unfolded
    if (!this.verticallyUnfoldedColumnsIndexes.includes(columnIndex)) return;

    // Remove it from the unfolded list if it is already unfolded
    // Also remove the column that have an unfolded level superior to the selected column
    this.verticallyUnfoldedColumnsIndexes = this.verticallyUnfoldedColumnsIndexes.filter(
      (index) =>
        index !== columnIndex && this.getColumn(index).unfoldedLevel <= unfoldedColumn.unfoldedLevel
    );

    // Reset what columns are unfolded
    this.resetUnfoldedColumns();
  }
  resetUnfoldedColumns() {
    // Set all columns to unfolded or not based on the unfolded list
    // Remove the columns that are generated by the unfolding
    this.columns.forEach((column) => {
      // We remove columns that have a parent column that is not in the unfolded list
      if (column.parentColumnIndex !== null) {
        const parentColumn = this.getColumn(column.parentColumnIndex);
        if (!parentColumn) {
          this.removeColumn(column.index);
          return;
        }

        // Ignore vertically unfolded columns
        if (!parentColumn.unfoldedHorizontally) {
          // Remove the column if the parent column is in the unfolded list
          if (!this.verticallyUnfoldedColumnsIndexes.includes(parentColumn.index)) {
            this.removeColumn(column.index);
            return;
          }
        }
      }
      // We remove columns that have an unfolded level superior to the selected column
      else if (column.unfoldedLevel > this.verticallyUnfoldedColumnsIndexes.length) {
        this.removeColumn(column.index);
        return;
      }

      // Set the unfolded property
      column.unfolded = this.verticallyUnfoldedColumnsIndexes.includes(column.index);
    });

    // Reset the virtual index mapping and selected data if no column is unfolded
    if (this.verticallyUnfoldedColumnsIndexes.length === 0) {
      this.virtualIndexMapping = {};
      this.nbLines = this.nbLinesOriginal;
      // Reapply filter
      this.updateFilters(true);
      return;
    }

    // Compute the new number of lines and link the virtual index to the original index
    const lastUnfoldedColumn = this.getColumn(this.verticallyUnfoldedColumnsIndexes.slice(-1)[0]);

    const newVirtualIndexMapping = {};
    let nbLines = 0;
    lastUnfoldedColumn.originalValues.forEach((value, i) => {
      // Check if the value is an array
      if (Array.isArray(value)) {
        // Register the virtual index mapping
        for (let j = 0; j < value.length; j++) {
          const newMapping = {
            originalIndex: i, // Point to the original index
            valueIndex: j, // The index of the value in the array
            depth: lastUnfoldedColumn.unfoldedLevel, // The depth of the unfolding
          };

          // Add the parent mapping if we are increasing the depth
          if (lastUnfoldedColumn.unfoldedLevel > this.virtualIndexMapping[i]?.depth)
            newMapping.parentMapping = this.virtualIndexMapping[i]; // The parent mapping

          newVirtualIndexMapping[nbLines + j] = newMapping;
        }
        nbLines += value.length;
      }
    });

    this.nbLines = nbLines;
    this.virtualIndexMapping = newVirtualIndexMapping;
    this.updateFilters(true);
  }
  unfoldDictHorizontally(columnIndex, columnsToUnfold) {
    const unfoldedColumn = this.getColumn(columnIndex);
    if (!unfoldedColumn || unfoldedColumn.typeText !== "Dict") return;

    // Unfold the column
    // Get the new columns values
    const newColumnsValues = {};
    columnsToUnfold.forEach((key) => {
      newColumnsValues[key] = [];
    });
    for (let i = 0; i < unfoldedColumn.originalValues.length; i++) {
      const dict = unfoldedColumn.originalValues[i];
      columnsToUnfold.forEach((key) => {
        newColumnsValues[key].push(dict[key]);
      });
    }

    // Create the new columns
    columnsToUnfold.forEach((key) => {
      const new_label = unfoldedColumn.label + "." + key;
      this.addColumn({
        label: new_label,
        values: newColumnsValues[key],
        category: unfoldedColumn.category,
        parentColumnIndex: columnIndex,
      });
    });

    unfoldedColumn.unfoldedHorizontally = true;
  }
  unfoldArrayHorizontally(columnIndex) {
    const unfoldedColumn = this.getColumn(columnIndex);
    if (
      !unfoldedColumn ||
      unfoldedColumn.typeText !== "Array" ||
      !unfoldedColumn.arrayColumnSizeNumber
    )
      return;

    // Unfold the column
    // Get the new columns values
    const newColumnsValues = {};

    for (let i = 0; i < unfoldedColumn.originalValues.length; i++) {
      const arr = unfoldedColumn.originalValues[i];
      for (let j = 0; j < arr.length; j++) {
        if (!newColumnsValues[j]) newColumnsValues[j] = [];
        newColumnsValues[j].push(arr[j]);
      }
    }

    // Create the new columns
    for (let i = 0; i < unfoldedColumn.arrayColumnSizeNumber; i++) {
      const new_label = unfoldedColumn.label + "[" + i + "]";
      this.addColumn({
        label: new_label,
        values: newColumnsValues[i],
        category: unfoldedColumn.category,
        parentColumnIndex: columnIndex,
      });
    }

    unfoldedColumn.unfoldedHorizontally = true;
  }
  foldHorizontally(columnIndex) {
    const unfoldedColumn = this.getColumn(columnIndex);
    if (!unfoldedColumn) return;

    // Fold the column if it is already unfolded
    if (!unfoldedColumn.unfoldedHorizontally) return;

    // Remove the columns that are generated by the unfolding
    this.removeColumns(
      this.columns
        .filter((column) => column.parentColumnIndex === columnIndex)
        .map((column) => column.index)
    );

    unfoldedColumn.unfoldedHorizontally = false;
    this.resetUnfoldedColumns();
  }

  // Other
  clean() {
    // Nullify references to arrays and objects to help garbage collection
    this.nbLinesOriginal = null;
    this.sampleIdList = null;

    // Clear and nullify selected data variables
    this.nbLines = null;
    this.selectedData.length = 0;
    this.selectedData = null;
    this.nbOriginalSelectedData = null;

    // Clear and nullify unfold variables
    this.verticallyUnfoldedColumnsIndexes.length = 0;
    this.verticallyUnfoldedColumnsIndexes = null;
    this.virtualIndexMapping = {};

    // Clear and nullify columns
    this.columns.forEach((column) => column.clean());
    this.columns.length = 0;
    this.columns = null;

    // Clear any additional caches or stored data
    samplesFiltering.clearCache();
  }
}

class Column {
  constructor(
    data,
    index,
    label,
    values,
    category,
    typeIn,
    group,
    unfoldedLevel = 0,
    parentColumnIndex = null
  ) {
    this.data = data;
    this.index = index;
    this.label = label;
    this.originalValues = values;
    this.category = category;
    this.group = group;
    this.unfoldedLevel = unfoldedLevel;
    this.parentColumnIndex = parentColumnIndex;
    this.unfolded = false;
    this.unfoldedHorizontally = false;

    // Override the values with a proxy to handle the unfolding
    this.values = new Proxy(this.originalValues, {
      get: (target, prop) => {
        // Return the value based on the original index
        if (!this.data.currentlyUnfoldedVertically()) {
          if (prop === "length") return this.data.nbLines;
          if (prop === "map") return target.map;
          if (prop === "reduce") return target.reduce;
          return this.originalValues[prop];
        }

        // Return the value based on the virtual index
        if (prop === "length") return this.data.nbLines;
        else if (prop === "map")
          return (callback) => {
            return this.data.selectedData.map((virtualIndex, i) => {
              return callback(target[this.data.virtualIndexMapping[virtualIndex].originalIndex], i);
            });
          };
        else if (prop === "reduce")
          return (callback, initialValue) => {
            return this.data.selectedData.reduce((acc, virtualIndex) => {
              return callback(
                acc,
                target[this.data.virtualIndexMapping[virtualIndex].originalIndex]
              );
            }, initialValue);
          };
        else if (prop === "slice")
          return (start, end) => {
            return this.data.selectedData.slice(start, end).map((virtualIndex) => {
              return target[this.data.virtualIndexMapping[virtualIndex].originalIndex];
            });
          };
        else if (prop === "_isVue") return true;
        else if (prop === "__ob__") return { dep: { id: 0 } };

        // If the data current unfolded level is the same as the column unfolded level
        // We can directly return the value
        if (this.unfoldedLevel === this.data.verticallyUnfoldedColumnsIndexes.length) {
          return target[prop];
        }

        // Else we need to return the value based on the virtual index
        // Find the good mapping
        let goodMapping = this.data.virtualIndexMapping[prop];
        // if (!goodMapping) return undefined;

        while (goodMapping.depth > this.unfoldedLevel) {
          goodMapping = goodMapping.parentMapping;
          if (!goodMapping) return undefined;
        }

        return target[goodMapping.originalIndex];
      },
    });

    this.defineColumnProperties(typeIn);
  }

  // Setup
  calculateMin(arr) {
    let min = Infinity;
    for (let i = 0; i < arr.length; i++) if (arr[i] < min) min = arr[i];
    return min;
  }
  calculateMax(arr) {
    let max = -Infinity;
    for (let i = 0; i < arr.length; i++) if (arr[i] > max) max = arr[i];
    return max;
  }
  defineColumnProperties(typeIn) {
    // Creating the column object
    this.uniques = [...new Set(this.originalValues)];
    // Sort the uniques
    this.uniques = this.uniques.sort();
    this.nbOccurrence = this.uniques.length;
    this.nbNullValues = this.originalValues.filter((v) => v === null).length;

    const isAllDictionaries = (arr) => {
      return arr.every((item) => item !== null && typeof item === "object" && !Array.isArray(item));
    };
    // Checking if the this.umn is type text, number or got undefined values
    if (!(this.uniques.findIndex((v) => !Array.isArray(v)) >= 0)) {
      // If all the values are arrays
      this.type = Array;
      this.typeText = "Array";
      this.arrayColumnSizeNumber = this.getArrayColumnSizeNumber();
    } else if (isAllDictionaries(this.uniques)) {
      // If all the values are dictionaries
      this.type = Object;
      this.typeText = "Dict";
    } else if (typeIn === "text" || this.uniques.find((v) => isNaN(v))) {
      // String Values
      this.type = String;
      this.typeText = "Class";
      let tmpUniqMap = {};
      this.valuesIndexUniques = this.uniques.map((str, i) => {
        tmpUniqMap[str] = i;
        return i;
      });

      const _valuesIndex = this.originalValues.map((str) => tmpUniqMap[str]);

      this.valuesIndex = new Proxy(_valuesIndex, {
        get: (target, prop) => {
          // Without unfolding
          if (!this.data.currentlyUnfoldedVertically()) {
            if (prop === "length") return this.data.nbLines;
            if (prop === "map") return target.map;
            if (prop === "reduce") return target.reduce;
            return target[prop];
          }

          // With unfolding
          if (prop === "length") return this.data.nbLines;
          else if (prop === "map")
            return (callback) => {
              return this.data.selectedData.map((virtualIndex) => {
                return callback(target[this.data.virtualIndexMapping[virtualIndex].originalIndex]);
              });
            };
          else if (prop === "reduce")
            return (callback, initialValue) => {
              return this.data.selectedData.reduce((acc, virtualIndex) => {
                return callback(
                  acc,
                  target[this.data.virtualIndexMapping[virtualIndex].originalIndex]
                );
              }, initialValue);
            };
          else if (prop === "_isVue") return true;
          else if (prop === "__ob__") return { dep: { id: 0 } };

          // If the data current unfolded level is the same as the column unfolded level
          // We can directly return the value
          if (this.unfoldedLevel === this.data.verticallyUnfoldedColumnsIndexes.length) {
            return target[prop];
          }

          // Else we need to return the value based on the virtual index
          // Find the good mapping
          let goodMapping = this.data.virtualIndexMapping[prop];
          if (!goodMapping) return undefined;

          while (goodMapping.depth > this.unfoldedLevel) {
            goodMapping = goodMapping.parentMapping;
            if (!goodMapping) return undefined;
          }

          return target[goodMapping.originalIndex];
        },
      });

      this.min = this.calculateMin(this.valuesIndexUniques);
      this.max = this.calculateMax(this.valuesIndexUniques);
    } else {
      // Default Type
      this.type = Number;
      this.typeText = "Num";
      this.originalValues = this.originalValues.map((v) => (v === null ? v : +v));
      this.uniques = this.uniques.map((v) => (v === null ? v : +v));
      this.nbOccurrence = this.uniques.length;
      this.min = this.calculateMin(this.uniques);
      this.max = this.calculateMax(this.uniques);
      this.average =
        this.originalValues.reduce((a, b) => a + b, 0) / this.originalValues.length || 0;
      if (this.uniques.length < 100) this.uniques.sort((a, b) => a - b);
    }
  }
  getArrayColumnSizeNumber() {
    // Iterate over the array values
    // Get the size of each array
    // Return null if at some point:
    //   The size is not the same, return null
    //   The is 0 or > to MAX_SUPPORTED_ARRAY_SIZE
    // Used for horizontal unfolding

    if (this.typeText !== "Array") return null;

    const MAX_SUPPORTED_ARRAY_SIZE = 8;
    let size = null;
    for (let i = 0; i < this.originalValues.length; i++) {
      const arr = this.originalValues[i];
      if (arr.length === 0 || arr.length > MAX_SUPPORTED_ARRAY_SIZE) return null;
      if (size === null) size = arr.length;
      else if (size !== arr.length) return null;
    }
    return size;
  }

  // Updates
  updateValues(newValues) {
    this.originalValues = newValues;
    this.defineColumnProperties();
  }
  canAddArrayLength() {
    if (this.typeText !== "Array") return false;
    // If a column with the same label already exists, we can't add the length
    if (this.data.getColumnByLabel(this.label + ".length")) return false;
    return true;
  }
  addArrayLength() {
    // Create a new column with the length of each array values
    if (!this.canAddArrayLength()) return;
    if (this.typeText !== "Array") return;

    const new_label = this.label + ".length";
    const column_values = new Array(this.data.nbLines)
      .fill(null)
      .map((_, i) => this.values[i].length);

    this.data.addColumn({
      label: new_label,
      values: column_values,
      category: this.category,
      typeIn: "num",
      group: null,
      parentColumnIndex: this.index,
    });
  }

  // Children
  hasChildren() {
    return this.getChildrenColumns().length > 0;
  }
  getChildrenColumns() {
    return this.data.columns.filter((column) => column.parentColumnIndex === this.index);
  }

  // Horizontal unfolding
  getPossibleColumnsToUnfold() {
    if (this.typeText !== "Dict")
      return {
        error: "The column is not a dictionary and cannot be unfolded horizontally.",
      };

    const keys = new Set();
    let nbKeys = null;

    for (let i = 0; i < this.originalValues.length; i++) {
      const dict = this.originalValues[i];
      const dictKeys = Object.keys(dict);

      if (nbKeys === null) nbKeys = dictKeys.length;
      else if (nbKeys !== dictKeys.length)
        return {
          error:
            "The number of keys in the dictionary is not the same for all the values (some dictionaries have " +
            nbKeys +
            " keys and some have " +
            dictKeys.length +
            " keys).",
        };

      if (nbKeys > 30)
        return {
          error:
            "The number of keys in the dictionary is too high to unfold horizontally (" +
            nbKeys +
            " > 30).",
        };

      const previousNbKeys = keys.size;
      dictKeys.forEach((key) => keys.add(key));

      if (keys.size === 0)
        return { error: "Some dictionary values are empty and cannot be unfolded horizontally." };

      if (previousNbKeys > 0 && keys.size !== previousNbKeys)
        return {
          error:
            "Some keys are not unique in the dictionary and cannot be used to unfold horizontally.",
        };
    }

    return {
      keys: Array.from(keys),
    };
  }

  // Other
  canBeDeleted() {
    return this.label !== "Data ID";
  }
  delete() {
    this.data.removeColumn(this.index);
  }
  clean() {
    this.data = null;
    this.index = null;
    this.label = null;
    this.originalValues.length = 0;
    this.originalValues = null;
    this.category = null;
    this.group = null;
    this.unfoldedLevel = null;
    this.parentColumnIndex = null;
    this.unfolded = null;

    this.values = null;

    // Clear any additional properties
    this.uniques.length = 0;
    this.uniques = null;
    this.nbOccurrence = null;
    if (this.undefinedIndexes?.length) this.undefinedIndexes.length = 0;
    this.undefinedIndexes = null;
    if (this.valuesIndexUniques?.length) this.valuesIndexUniques.length = 0;
    this.valuesIndexUniques = null;
    this.valuesIndex = null;
  }
}

export default {
  Data,
  Column,
};
