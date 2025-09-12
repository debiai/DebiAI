import numpy as np
from dqm.representativeness.chi_square import ChiSquareGoodnessOfFit
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
    This function is now handled by the dqm-ml library
    """
    pass


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
        # Convert data to numpy array
        data_array = np.array(data)
        
        # Use dqm-ml Chi-square goodness of fit test
        chi_square_test = ChiSquareGoodnessOfFit()
        
        # Perform the test
        result = chi_square_test.compute(
            data=data_array,
            bins=bins,
            distribution=distribution
        )
        
        # Extract results from dqm-ml output
        chi2_stat = result.get('chi2_statistic', 0.0)
        p_value = result.get('p_value', 0.0)
        degrees_of_freedom = result.get('degrees_of_freedom', bins - 1)
        observed_freq = result.get('observed_frequencies', [])
        expected_freq = result.get('expected_frequencies', [])
        
        # Calculate representativeness score (normalize p-value to 0-1 scale)
        representativeness_score = min(p_value, 1.0)

        # Determine if distribution fits (common threshold is 0.05)
        distribution_fit = p_value > 0.05

        # Format frequencies for display
        frequencies = []
        if len(observed_freq) == len(expected_freq):
            frequencies = [
                {
                    "1.Expected freq.": round(expected_freq[i], 2),
                    "2.Observed freq.": int(observed_freq[i]),
                    "3.Diff": round(observed_freq[i] - expected_freq[i], 2),
                }
                for i in range(len(observed_freq))
            ]

        # Return outputs
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
