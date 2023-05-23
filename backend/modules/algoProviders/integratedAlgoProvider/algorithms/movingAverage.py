import os
from ..utils import get_input_from_inputs

# This algorithm is a simple moving average calculator
# It takes a list of numbers and a window size as input

# Technical details (must respect the algo-api format):
algorithm_description = {
    "id": os.path.basename(__file__)[:-3],  # Name of the file
    "name": "Moving Average",
    "description": """This algorithm calculates the moving average of a list of numbers.
The result will be a list of the same length as the two input lists.
This moving average is very basic and does not take into account time between each value.""",
    "author": "DebiAI",
    "version": "1.0.0",
    "creationDate": "2023-05-23",
    "tags": ["calculations"],
    "inputs": [
        {
            "name": "list",
            "description": "List of numbers to calculate the moving average of",
            "type": "array",
            "arrayType": "number",
        },
        {
            "name": "window",
            "description": "Window size for the moving average",
            "type": "number",
            "default": 5,
            "availableValues": [3, 5, 7, 9],
            "min": 3,
        },
    ],
    "outputs": [
        {
            "name": "movingAverage",
            "description": "Moving average of the input list",
            "type": "array",
            "arrayType": "number",
        }
    ],
}


def get_algorithm_details():
    return algorithm_description


def use_algorithm(inputs):
    # Get inputs
    list = get_input_from_inputs(inputs, "list", "array", "number")
    window = get_input_from_inputs(inputs, "window", "number")

    if window < 3:
        raise TypeError("Window size must be at least 3")
    if window > len(list):
        raise TypeError("Window size must be smaller than the list size")
    if len(list) < 3:
        raise TypeError("List must have at least 3 elements")

    # Calculate moving average
    movingAverage = []
    for i in range(len(list)):
        if i < window - 1:
            movingAverage.append(sum(list[: i + 1]) / (i + 1))
        else:
            movingAverage.append(sum(list[i - window + 1 : i + 1]) / window)

    # Return outputs
    return [{"name": "movingAverage", "value": movingAverage}]
