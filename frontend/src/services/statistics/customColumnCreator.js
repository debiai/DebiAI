// ======== Custom column creator ========

// create a column from a for the plotly par. coord.
var customColumnCreation = function (data, colName, firstColumnIndex, rules) {
  // creating the values from the rules with the eval function

  const firstColumnValues = data.getColumn(firstColumnIndex).values;
  const values = [];

  for (const rule of rules) {
    values.push(data.getColumn(rule.colIndex).values);
  }

  const newColValues = firstColumnValues.map((v, i) => {
    let operation;
    if (data.getColumn(firstColumnIndex).type == Number) operation = "" + v;
    else operation = "'" + firstColumnValues[i] + "'";

    rules.forEach((rule, ruleNb) => {
      if (data.getColumn(rule.colIndex).type == Number)
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

  // Return the column object
  return {
    label: colName,
    values: newColValues,
    category: "virtual",
  };
};

export default {
  customColumnCreation,
};
