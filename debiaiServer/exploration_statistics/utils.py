from debiaiServer.modules.dataProviders.DataProvider import DataProvider


def get_samples_batch(
    data_provider: DataProvider, projectId, analysis, start, end
) -> dict:
    # Get the samples id list
    data_id_list = data_provider.get_id_list(
        projectId,
        analysis,
        start,
        end,
    )

    # Load the samples
    data = data_provider.get_samples(projectId, analysis, data_id_list)

    return data


def get_column_value_in_data(
    column_name: str, sample_data: list, project_columns: list
) -> any:
    for i, column in enumerate(project_columns):
        if column["name"] == column_name:
            return sample_data[i]
    raise ValueError(f"Column '{column_name}' not found in project columns.")


def get_samples_batch_by_columns(
    data_provider: DataProvider,
    projectId,
    analysis,
    start,
    end,
    project_columns: list,
    selected_columns: list,
) -> dict:
    """
    Returns a { column_name: [value1, value2, ...] }
    dictionary for the samples in the given range.
    """

    # Get the samples arrays
    data = get_samples_batch(data_provider, projectId, analysis, start, end)

    # Data:
    # {
    #     "sample_id": [
    #         "Value1",
    #         2,
    #         [...],
    #         ...
    #     ],
    #     ...
    # }

    # Get the index of the selected columns in the project columns
    column_indices = {
        column["name"]: i
        for i, column in enumerate(project_columns)
        if column["name"] in selected_columns
    }

    # Convert to a dictionary with column names as keys
    data_columns = {}
    for column_name in selected_columns:
        data_columns[column_name] = [None] * len(data)
        for data_index, sample_data in enumerate(data.values()):
            data_columns[column_name][data_index] = sample_data[
                column_indices[column_name]
            ]

    return data_columns


def get_data_batch(
    data_provider: DataProvider,
    projectId,
    analysis,
    start,
    end,
    project_columns: list,
    selected_columns: list,
) -> dict:
    """
    Returns a batch of dict:
    {'data_4': [1, 2, 3], 'data_5': [4, 5, 6], 'data_6': [7, 8, 9]},
    """

    # Get the samples arrays
    data = get_samples_batch(data_provider, projectId, analysis, start, end)

    # Data:
    # {
    #     "sample_id": [
    #         "Value1",
    #         2,
    #         [...],
    #         ...
    #     ],
    #     ...
    # }

    # Get the index of the selected columns in the project columns
    column_indices = {
        column["name"]: i
        for i, column in enumerate(project_columns)
        if column["name"] in selected_columns
    }

    # Convert to a dictionary with data id as keys
    data_columns = {}
    for data_id, sample_data in data.items():
        data_columns[data_id] = [
            sample_data[column_indices[column_name]] for column_name in selected_columns
        ]

    return data_columns
