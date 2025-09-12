import numpy as np
from scipy import stats
from debiaiServer.modules.algoProviders.integratedAlgoProvider.utils import (
    get_input_from_inputs,
)

# This algorithm calculates representativeness metrics for data quality
# assessment. Based on the dqm-ml library representativeness metrics
# It performs Chi-square goodness of fit test for normal and uniform
# distributions

# Technical details (must respect the algo-api format):
algorithm_description = {
    "name": "Representativeness Metric",
    "description": """Calculates representativeness metrics using Chi-square
goodness of fit test. Measures how well the dataset distribution conforms
to a theoretical distribution (normal or uniform).""",
    "author": "DQM-ml",
    "version": "1.0.0",
    "creationDate": "2025-09-12",
    "tags": ["metrics", "representativeness", "data-quality", "distribution"],
    "inputs": [
        {
            "name": "Data",
            "description": "List of numerical values to analyze",
            "type": "array",
            "arrayType": "number",
        },
        {
            "name": "Distribution",
            "description": "Theoretical distribution to test against",
            "type": "string",
            "default": "normal",
            "availableValues": ["normal", "uniform"],
        },
        {
            "name": "Number of bins",
            "description": "Number of bins for discretization",
            "type": "number",
            "default": 10,
            "min": 3,
            "max": 50,
        },
    ],
    "outputs": [
        {
            "name": "Chi-square statistic",
            "description": "Chi-square test statistic value",
            "type": "number",
        },
        {
            "name": "P-value",
            "description": "P-value from the Chi-square test "
            + "(higher values indicate better fit)",
            "type": "number",
        },
        {
            "name": "Degrees of freedom",
            "description": "Degrees of freedom for the Chi-square test",
            "type": "number",
        },
        {
            "name": "Representativeness score",
            "description": "Normalized representativeness score "
            + "(0-1, higher is better)",
            "type": "number",
        },
        {
            "name": "Distribution fit",
            "description": "Whether the data fits the theoretical "
            + "distribution (p-value > 0.05)",
            "type": "boolean",
        },
        {
            "name": "Observed frequencies",
            "description": "Observed frequencies in each bin",
            "type": "array",
            "arrayType": "number",
        },
        {
            "name": "Expected frequencies",
            "description": "Expected frequencies based on "
            + "theoretical distribution",
            "type": "array",
            "arrayType": "number",
        },
    ],
}


def get_algorithm_details():
    return algorithm_description


def _discretize_data(data, bins, distribution_type="normal"):
    """
    Discretize data into bins and calculate observed and expected frequencies
    """
    data_array = np.array(data)

    if distribution_type == "normal":
        # Calculate mean and std for normal distribution
        mean = np.mean(data_array)
        std = np.std(data_array, ddof=1)

        # Create bins based on normal distribution quantiles
        bin_edges = np.linspace(mean - 3 * std, mean + 3 * std, bins + 1)

        # Calculate observed frequencies
        observed, _ = np.histogram(data_array, bins=bin_edges)

        # Calculate expected frequencies for normal distribution
        expected = []
        for i in range(len(bin_edges) - 1):
            lower_prob = stats.norm.cdf(bin_edges[i], mean, std)
            upper_prob = stats.norm.cdf(bin_edges[i + 1], mean, std)
            expected_freq = (upper_prob - lower_prob) * len(data_array)
            expected.append(expected_freq)

        expected = np.array(expected)

    elif distribution_type == "uniform":
        # Create uniform bins
        min_val = np.min(data_array)
        max_val = np.max(data_array)
        bin_edges = np.linspace(min_val, max_val, bins + 1)

        # Calculate observed frequencies
        observed, _ = np.histogram(data_array, bins=bin_edges)

        # For uniform distribution, expected frequency is equal for all bins
        expected_freq = len(data_array) / bins
        expected = np.full(bins, expected_freq)

    else:
        raise ValueError(f"Unsupported distribution type: {distribution_type}")

    return observed, expected


def use_algorithm(inputs):
    # Get inputs
    data = get_input_from_inputs(inputs, "Data", "array", "number")
    distribution = get_input_from_inputs(inputs, "Distribution", "string")
    bins = get_input_from_inputs(inputs, "Number of bins", "number")

    # Validate inputs
    if len(data) < 10:
        raise ValueError(
            "Data must contain at least 10 values " + "for meaningful analysis"
        )

    if bins < 3:
        raise ValueError("Number of bins must be at least 3")

    if distribution not in ["normal", "uniform"]:
        raise ValueError("Distribution must be 'normal' or 'uniform'")

    # Convert to integer
    bins = int(bins)

    try:
        # Discretize data and get observed/expected frequencies
        observed, expected = _discretize_data(data, bins, distribution)

        # Remove bins with zero expected frequency to avoid division by zero
        mask = expected > 0
        observed_filtered = observed[mask]
        expected_filtered = expected[mask]

        if len(observed_filtered) < 2:
            raise ValueError("Not enough valid bins for Chi-square test")

        # Fix numerical precision issue by normalizing expected frequencies
        # to match the sum of observed frequencies exactly
        observed_sum = np.sum(observed_filtered)
        expected_sum = np.sum(expected_filtered)

        if expected_sum > 0:
            expected_filtered = expected_filtered * (observed_sum / expected_sum)

        # Perform Chi-square goodness of fit test
        chi2_stat, p_value = stats.chisquare(observed_filtered, expected_filtered)

        # Calculate degrees of freedom
        degrees_of_freedom = len(observed_filtered) - 1
        if distribution == "normal":
            degrees_of_freedom -= 2  # Subtract 2 for estimated mean and std
        elif distribution == "uniform":
            degrees_of_freedom -= 0  # No parameters estimated for uniform

        degrees_of_freedom = max(1, degrees_of_freedom)

        # Calculate representativeness score (normalize p-value to 0-1 scale)
        # Higher p-value means better fit, so we use p-value directly as score
        representativeness_score = min(p_value, 1.0)

        # Determine if distribution fits (common threshold is 0.05)
        distribution_fit = p_value > 0.05

        # Return outputs
        observed = observed.tolist()
        expected = expected.tolist()
        frequencies = [
            {
                "1.Expected freq.": int(expected[i]),
                "2.Observed freq.": int(observed[i]),
                "3.Diff": int(observed[i] - expected[i]),
            }
            for i in range(len(observed))
        ]
        return [
            {"name": "Chi-square statistic", "value": float(chi2_stat)},
            {"name": "P-value", "value": float(p_value)},
            {"name": "Degrees of freedom", "value": int(degrees_of_freedom)},
            {
                "name": "Representativeness score",
                "value": float(representativeness_score),
            },
            {"name": "Distribution fit", "value": bool(distribution_fit)},
            {"name": "Frequencies", "value": frequencies},
            # TODO: Add data from & to
        ]

    except Exception as e:
        raise ValueError(f"Error in representativeness calculation: {str(e)}")
