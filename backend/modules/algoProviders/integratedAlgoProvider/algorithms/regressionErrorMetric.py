import os
from ..utils import get_input_from_inputs

# This algorithm is a simple regression metric calculator
# It takes a list of numbers corresponding to an error
# and a ceil corresponding to the maximum acceptable error

# It returns a list of True/False values corresponding to
# whether the error is acceptable or not

# It also returns the percentage of acceptable errors

# Technical details (must respect the algo-api format):
algorithm_description = {
    "id": os.path.basename(__file__)[:-3],  # Name of the file
    "name": "Regression Metric",
    "description": """Calculates the regression metric of an error list according to a ceil.""",
    "author": "DebiAI",
    "version": "1.0.0",
    "creationDate": "2023-05-23",
    "tags": ["metrics", "regression"],
    "inputs": [
        {
            "name": "list",
            "description": "List of errors to calculate the regression metric of",
            "type": "array",
            "arrayType": "number",
        },
        {
            "name": "ceil",
            "description": "Maximum acceptable error, depends on the use case",
            "type": "number",
            "default": 5,
            "availableValues": [0.1, 5, 100, 10000],
            "min": 0,
        },
    ],
    "outputs": [
        {
            "name": "regressionMetric",
            "description": "Regression metric of the input list, True if the error is acceptable, False otherwise",
            "type": "array",
            "arrayType": "boolean",
        },
        {
            "name": "percentage",
            "description": "Percentage of acceptable errors",
            "type": "number",
        },
    ],
}


def get_algorithm_details():
    return algorithm_description


def use_algorithm(inputs):
    # Get inputs
    list = get_input_from_inputs(inputs, "list", "array", "number")
    ceil = get_input_from_inputs(inputs, "ceil", "number")

    # Check inputs
    if ceil < 0:
        raise TypeError("Ceil must be positive")

    # Calculate regression metric
    regressionMetric = []
    for error in list:
        if abs(error) < ceil:
            regressionMetric.append(True)
        else:
            regressionMetric.append(False)

    percentage = regressionMetric.count(True) / len(regressionMetric)
    percentage = round(percentage * 100, 2)

    # Return outputs
    return [
        {
            "name": "regressionMetric",
            "value": regressionMetric,
        },
        {
            "name": "percentage",
            "value": percentage,
        },
    ]
