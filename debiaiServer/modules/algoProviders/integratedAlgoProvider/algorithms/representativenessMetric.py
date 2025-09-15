import pandas as pd
from dqm.representativeness.metric import DistributionAnalyzer
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
            "name": "Frequencies",
            "description": "Detailed frequency analysis with intervals, "
            + "observed and expected frequencies",
            "type": "array",
            "arrayType": "object",
        },
    ],
}


def get_algorithm_details():
    return algorithm_description


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
        # Convert data to pandas Series
        data_series = pd.Series(data)

        # Use dqm-ml DistributionAnalyzer
        analyzer = DistributionAnalyzer(data_series, bins, distribution)

        # Perform chi-square test
        chi2_result = analyzer.chisquare_test()

        if chi2_result is None:
            raise ValueError("Chi-square test failed")

        # Extract p-value and intervals from result
        if isinstance(chi2_result, tuple) and len(chi2_result) >= 2:
            p_value = chi2_result[0]
            intervals_freq = chi2_result[1] if len(chi2_result) > 1 else {}
        else:
            p_value = chi2_result
            intervals_freq = {}

        # Calculate chi-square statistic (approximation from p-value)
        from scipy import stats

        degrees_of_freedom = bins - 1
        if distribution == "normal":
            degrees_of_freedom -= 2
        degrees_of_freedom = max(1, degrees_of_freedom)

        # Get chi2 statistic from p-value (inverse calculation)
        if p_value < 1.0:
            chi2_stat = stats.chi2.ppf(1 - p_value, degrees_of_freedom)
        else:
            chi2_stat = 0.0

        # Calculate representativeness score (normalize p-value to 0-1 scale)
        representativeness_score = min(p_value, 1.0)

        # Determine if distribution fits (common threshold is 0.05)
        distribution_fit = p_value > 0.05

        # Format frequencies for display, from dataframe to list of dicts
        frequencies = []
        # intervals_freq is a dataframe with columns:
        # lower_limit, upper_limit, obs_freq, exp_freq
        if isinstance(intervals_freq, pd.DataFrame):
            for _, row in intervals_freq.iterrows():
                lower = float(row["lower_limit"])
                upper = float(row["upper_limit"])
                obs_freq = int(row["obs_freq"])
                exp_freq = float(row["exp_freq"])
                frequencies.append(
                    {
                        "1. Interval": f"[{lower} ; {upper}]",
                        "2. Observed frequency": obs_freq,
                        "3. Expected frequency": exp_freq,
                        "4. Difference": obs_freq - exp_freq,
                    }
                )

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
        ]

    except Exception as e:
        raise ValueError(f"Error in representativeness calculation: {str(e)}")
