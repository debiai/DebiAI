// This service is used by the columns selections components
// to filter the selected columns from a rule list

let getColumnStatus = (column, validColumnsProperties) => {
  // Verify if the column is valid from the validColumnsProperties
  // Example of validColoredColumnProperties: {
  //   // Valid properties details
  //   types: ["Class", Number, Boolean],
  //   maxUniqueValues: 10,
  //   // Warning properties details
  //   warningTypes: ["Dict", "Array"],
  //   warningMaxUniqueValues: 5,
  //   // Everything else is invalid
  // },
  // Returns "valid", "warning" or "invalid" and the reason

  const warnings = [];
  const errors = [];

  // Warnings
  // Check if the type is a warning
  if (
    validColumnsProperties.warningTypes &&
    validColumnsProperties.warningTypes.includes(column.typeText)
  ) {
    warnings.push(
      "The column type may not be supported, recommended types are: " +
        validColumnsProperties.types.join(", ")
    );
  }

  // Check if the number of unique values is a warning
  if (
    validColumnsProperties.warningMaxUniqueValues &&
    column.nbOccurrence > validColumnsProperties.warningMaxUniqueValues
  ) {
    warnings.push(
      "The number of unique values of the column may be too high, it should be below " +
        validColumnsProperties.warningMaxUniqueValues
    );
  }

  // Errors
  // Check if the column type is valid
  if (validColumnsProperties.types && !validColumnsProperties.types.includes(column.typeText)) {
    errors.push(
      "The column type is not supported for the action that you want to perform, valid column types are: " +
        validColumnsProperties.types.join(", ")
    );
  }

  // Check if the number of unique values is valid
  if (
    validColumnsProperties.maxUniqueValues &&
    column.nbOccurrence > validColumnsProperties.maxUniqueValues
  ) {
    errors.push(
      "The number of unique values of the column is too high, it should be below " +
        validColumnsProperties.maxUniqueValues
    );
  }

  // If there are errors, return the first error
  if (errors.length > 0) {
    return { status: "invalid", reason: errors.join("\n") };
  }

  // If there are no errors but warnings, return the first warning
  if (warnings.length > 0) {
    return { status: "warning", reason: warnings.join("\n") };
  }

  // If validColumnsProperties is empty, return valid
  if (Object.keys(validColumnsProperties).length === 0) {
    return { status: "valid", reason: "" };
  }

  // If no warnings or errors, return valid
  return { status: "valid", reason: "" };
};

export default {
  getColumnStatus,
};
