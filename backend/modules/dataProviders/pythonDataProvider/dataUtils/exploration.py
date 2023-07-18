from modules.dataProviders.pythonDataProvider.dataUtils import (
    pythonModuleUtils,
)

DATA_PATH = pythonModuleUtils.DATA_PATH
DATA_TYPES = pythonModuleUtils.DATA_TYPES


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
