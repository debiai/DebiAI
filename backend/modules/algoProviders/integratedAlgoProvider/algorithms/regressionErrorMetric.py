from ..utils import get_input_from_inputs

# This algorithm is a simple regression metric calculator
# It takes a list of numbers corresponding to an error
# and a ceil corresponding to the maximum acceptable error

# It returns a list of True/False values corresponding to
# whether the error is acceptable or not

# It also returns the percentage of acceptable errors

# Technical details (must respect the algo-api format):
algorithm_description = {
    "name": "Regression Metric",
    "description": """Calculates the regression metric of an error list according to a ceil. 
    """,
    "author": "DebiAI",
    "version": "1.0.0",
    "creationDate": "2023-05-23",
    "tags": ["metrics", "regression"],
    "inputs": [
        {
            "name": "Ground truth",
            "description": "List of ground truth values",
            "type": "array",
            "arrayType": "number",
        },
        {
            "name": "Predictions",
            "description": "List of predictions, must have the same length as the ground truth list",
            "type": "array",
            "arrayType": "number",
        },
        {
            "name": "Ceil",
            "description": "Maximum acceptable error, depends on the use case, >= 0",
            "type": "number",
            "default": 5,
            "availableValues": [0.1, 5, 100, 10000],
            "min": 0,
        },
    ],
    "outputs": [
        {
            "name": "Binary error",
            "description": "Regression metric of the input list, False if abs(GDT - PRED) < ceil, True otherwise",
            "type": "array",
            "arrayType": "boolean",
        },
        {
            "name": "Error percentage",
            "type": "number",
        },
    ],
}


def get_algorithm_details():
    return algorithm_description


def use_algorithm(inputs):
    # Get inputs
    gdt = get_input_from_inputs(inputs, "Ground truth", "array", "number")
    predictions = get_input_from_inputs(inputs, "Predictions", "array", "number")
    ceil = get_input_from_inputs(inputs, "Ceil", "number")

    # Check inputs
    if ceil < 0:
        raise TypeError("Ceil must be positive")

    if len(gdt) != len(predictions):
        raise TypeError("Ground truth and predictions must have the same length")

    # Calculate regression metric
    regressionMetric = []
    for i in range(len(gdt)):
        error = gdt[i] - predictions[i]

        if abs(error) < ceil:
            regressionMetric.append(False)
        else:
            regressionMetric.append(True)

    percentage = regressionMetric.count(True) / len(regressionMetric)
    percentage = round(percentage * 100, 2)

    # Return outputs
    return [
        {
            "name": "Binary error",
            "value": regressionMetric,
        },
        {
            "name": "Error percentage",
            "value": percentage,
        },
    ]
