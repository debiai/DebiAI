from modules.dataProviders.pythonDataProvider.dataUtils import (
    pythonModuleUtils,
)

DATA_PATH = pythonModuleUtils.DATA_PATH
DATA_TYPES = pythonModuleUtils.DATA_TYPES
MAX_COMBINATORIAL = 3000


# Columns metrics
def get_columns_metrics(project_id, column_labels):
    """
    Return a list of metrics for each column
    """

    from time import sleep
    from random import randint

    # TODO: make the real function
    sleep(1)

    results = []
    for column_label in column_labels:
        results.append(
            {
                "label": column_label,
                "nbUniqueValues": randint(1, 35),
            }
        )

    return results


def get_combinatorial_metrics(project_id, columns):
    """
    Return a list of metrics for each columns combinatorial
    """

    from time import sleep
    from random import randint

    # First, get each columns unique values
    columns_unique_values = []

    for column in columns:
        unique_values = {
            "nbUniqueValues": randint(1, 20),
            "uniqueValues": [],
            "label": column["label"],
        }
        if "nbChunks" in column and column["nbChunks"] is not None:
            unique_values["nbUniqueValues"] = column["nbChunks"]

        # Generate unique values
        if randint(0, 1) == 1:
            # Numeric
            for i in range(unique_values["nbUniqueValues"]):
                unique_values["uniqueValues"].append(randint(1, 10) + 100 * i)
        else:
            # String
            for i in range(unique_values["nbUniqueValues"]):
                unique_values["uniqueValues"].append("value_" + str(i))

        columns_unique_values.append(unique_values)

    # Compute nb combinations
    nb_combinations = 1

    for column in columns_unique_values:
        if "nbChunks" in column and column["nbChunks"] is not None:
            nb_combinations *= column["nbChunks"]
        else:
            nb_combinations *= column["nbUniqueValues"]

    # Then, generate combinatorial
    combinations = _get_combinations_recur(0, columns_unique_values)
    if len(combinations) > MAX_COMBINATORIAL:
        # Too many combinations
        combinations = combinations[:MAX_COMBINATORIAL]

    # Add metrics
    results = []
    for combination in combinations:
        results.append(
            {
                "combination": combination,
                "metrics": {
                    "nbValues": pow(randint(1, 100), 2) if randint(1,10) == 1 else 0,
                    # "nbValues": 1
                },
            }
        )

    return {
        "combinations": results,
        "totalCombinations": nb_combinations,
    }


def _get_combinations_recur(index, columns_unique_values) -> list:
    unique_values = columns_unique_values[index]["uniqueValues"]

    if index == len(columns_unique_values) - 1:
        # Last column
        return [[value] for value in unique_values]

    next_unique_values = _get_combinations_recur(index + 1, columns_unique_values)

    combinations = []

    for value in unique_values:
        for next_value in next_unique_values:
            combinations.append([value] + next_value)

            if len(combinations) > MAX_COMBINATORIAL:
                # Too many combinations
                return combinations

    return combinations
