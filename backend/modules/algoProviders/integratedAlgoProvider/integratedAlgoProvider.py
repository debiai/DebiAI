import os

def _get_algorithm_python(algorithm_name):
    """Get the python file of the algorithm

    Args:
        algorithm_name (str): Name of the algorithm

    Returns:
        module: Python module of the algorithm
    """

    # Get the algorithm file
    algorithm_file = None
    for file in os.listdir(os.path.dirname(__file__) + "/algorithms"):
        if file.endswith(".py") and file[:-3] == algorithm_name:
            algorithm_file = file[:-3]
            break

    # Check if the file exists
    if algorithm_file is None:
        raise ValueError("Algorithm " + algorithm_name + " does not exists")

    # Import the algorithm
    algorithm_python = __import__(
        "modules.algoProviders.integratedAlgoProvider.algorithms." + algorithm_file,
        fromlist=["*"],
    )

    return algorithm_python


def get_algorithms():
    """Get all algorithms that DebiAI can provide

    Returns:
        list: List of algorithms
    """

    # List the .py files if the algorithms folder
    algorithm_files = []
    for file in os.listdir(os.path.dirname(__file__) + "/algorithms"):
        if file.endswith(".py") and file != "__init__.py":
            algorithm_files.append(file[:-3])

    # Import the algorithms
    algorithms_python = []
    for file in algorithm_files:
        print("Importing " + file)
        try:
            algorithms_python.append(_get_algorithm_python(file))
        except ModuleNotFoundError as e:
            print("Error importing " + file)
            print(e)

    # Get the algorithms (call the get_algorithm_details() function)
    algorithms = []
    for algorithm in algorithms_python:
        algorithms.append(algorithm.get_algorithm_details())

    return algorithms


def use_algorithm(algorithmId, data):
    """Use an algorithm

    Args:
        algorithmId (string): ID of the algorithm
        data (list): inputs

    Returns:
        list: outputs
    """

    # Get the algorithm
    algorithm = _get_algorithm_python(algorithmId)

    # Use the algorithm
    outputs = algorithm.use_algorithm(data["inputs"])

    return outputs
