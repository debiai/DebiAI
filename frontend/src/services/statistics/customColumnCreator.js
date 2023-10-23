// ======== Custom column creator ========

// create a column from a for the plotly par. coord.
var customColumnCreation = function (data, colName, firstColumnIndex, rules) {
  // creating the values from the rules with the eval function

  let firstColumnValues = data.columns.find((c) => c.index == firstColumnIndex).values;
  let values = [];

  for (const rule of rules) {
    let valuesToMerge = data.columns.find((c) => c.index == rule.colIndex).values;
    values.push(valuesToMerge);
  }

  let newColValues = firstColumnValues.map((v, i) => {
    let operation;
    if (data.columns[firstColumnIndex].type == "number") operation = "" + firstColumnValues[i];
    else operation = "'" + firstColumnValues[i] + "'";

    rules.forEach((rule, ruleNb) => {
      if (data.columns[rule.colIndex].type == Number)
        operation += " " + rule.operator.code + " " + values[ruleNb][i];
      else operation += " " + rule.operator.code + " '" + values[ruleNb][i] + "'";
    });

    try {
      return eval(operation);
    } catch (error) {
      console.log(error);
      console.warn(operation);
      throw new Error("Error in the custom column creation");
    }
  });

  // Creating the column object
  let col = {
    label: colName,
    index: data.columns.length,
    values: newColValues,
    type: null,
    typeText: "",
    category: "virtual",
  };

  col.uniques = [...new Set(col.values)];
  col.nbOccurrence = col.uniques.length;

  // Checking if the column is type text, number or got undefined values
  if (col.uniques.findIndex((v) => v === undefined || v === "" || v === null) >= 0) {
    // undefined Values
    col.type = undefined;
    col.typeText = "undefined";
    col.undefinedIndexes = col.values
      .map((v, i) => (v == undefined || v == "" || v == null ? i : -1))
      .filter((v) => v >= 0);
    console.warn("Undefined values : " + colName);
    console.warn(col.uniques);
    console.warn(col.values);
  } else if (col.uniques.find((v) => isNaN(v))) {
    // String Values
    col.type = String;
    col.typeText = "Class";
    col.valuesIndexUniques = col.uniques.map((str, i) => i);
    col.valuesIndex = col.values.map((str) => col.uniques.indexOf(str));
    col.min = Math.min(...col.valuesIndexUniques);
    col.max = Math.max(...col.valuesIndexUniques);
    if (col.uniques.length < 100) col.uniques.sort();
  } else {
    // Default Type
    col.type = Number;
    col.typeText = "Num";
    col.nbOccurrence = col.uniques.length;
    col.min = Math.min(...col.uniques);
    col.max = Math.max(...col.uniques);
    col.values = col.values.map((v) => +v);
    col.average = col.values.reduce((a, b) => a + b, 0) / data.nbLines || 0;
    if (col.uniques.length < 100) col.uniques.sort((a, b) => a - b);
  }

  return col;
};

export default {
  customColumnCreation,
};
