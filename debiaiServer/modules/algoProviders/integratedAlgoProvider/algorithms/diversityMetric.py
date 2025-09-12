import numpy as np
from dqm.diversity.simpson import Simpson
from dqm.diversity.gini_simpson import GiniSimpson
from collections import Counter
from debiaiServer.modules.algoProviders.integratedAlgoProvider.utils import (
    get_input_from_inputs,
)

# This algorithm calculates diversity metrics for data quality assessment.
# Based on the dqm-ml library diversity metrics
# It calculates Simpson and Gini-Simpson diversity indices

# Technical details (must respect the algo-api format):
algorithm_description = {
    "name": "Diversity Metric",
    "description": """Calculates diversity metrics using Simpson and Gini-Simpson
indices. Measures the presence and distribution of different values in the dataset,
indicating how diverse the data is.""",
    "author": "DQM-ml",
    "version": "1.0.0",
    "creationDate": "2025-09-12",
    "tags": ["metrics", "diversity", "data-quality", "distribution"],
    "inputs": [
        {
            "name": "Data",
            "description": "List of values to analyze for diversity",
            "type": "array",
            "arrayType": "string",
        },
        {
            "name": "Metric type",
            "description": "Type of diversity metric to calculate",
            "type": "string",
            "default": "simpson",
            "availableValues": ["simpson", "gini-simpson", "both"],
        },
    ],
    "outputs": [
        {
            "name": "Simpson index",
            "description": "Simpson diversity index (0-1, lower values indicate higher diversity)",
            "type": "number",
        },
        {
            "name": "Gini-Simpson index",
            "description": "Gini-Simpson diversity index (0-1, higher values indicate higher diversity)",
            "type": "number",
        },
        {
            "name": "Number of unique values",
            "description": "Total number of unique values in the dataset",
            "type": "number",
        },
        {
            "name": "Total samples",
            "description": "Total number of samples analyzed",
            "type": "number",
        },
        {
            "name": "Most frequent value",
            "description": "The most frequently occurring value",
            "type": "string",
        },
        {
            "name": "Most frequent count",
            "description": "Count of the most frequent value",
            "type": "number",
        },
        {
            "name": "Value frequencies",
            "description": "Frequency distribution of all values",
            "type": "object",
        },
    ],
}


def get_algorithm_details():
    return algorithm_description


def use_algorithm(inputs):
    # Get inputs
    data = get_input_from_inputs(inputs, "Data", "array")
    metric_type = get_input_from_inputs(inputs, "Metric type", "string")

    # Validate inputs
    if len(data) == 0:
        raise ValueError("Data cannot be empty")

    if metric_type not in ["simpson", "gini-simpson", "both"]:
        raise ValueError("Metric type must be 'simpson', 'gini-simpson', or 'both'")

    try:
        # Convert data to strings and count frequencies
        data_str = [str(item) for item in data]
        frequencies = Counter(data_str)
        
        # Calculate basic statistics
        total_samples = len(data_str)
        unique_values = len(frequencies)
        most_frequent_value = frequencies.most_common(1)[0][0]
        most_frequent_count = frequencies.most_common(1)[0][1]

        # Prepare outputs based on requested metric type
        outputs = []
        
        if metric_type in ["simpson", "both"]:
            # Use dqm-ml Simpson diversity
            simpson_metric = Simpson()
            simpson_result = simpson_metric.compute(data_str)
            simpson_index = simpson_result.get('simpson_index', 0.0)
            
            outputs.append({
                "name": "Simpson index",
                "value": float(simpson_index)
            })
        
        if metric_type in ["gini-simpson", "both"]:
            # Use dqm-ml Gini-Simpson diversity
            gini_simpson_metric = GiniSimpson()
            gini_simpson_result = gini_simpson_metric.compute(data_str)
            gini_simpson_index = gini_simpson_result.get('gini_simpson_index', 0.0)
            
            outputs.append({
                "name": "Gini-Simpson index",
                "value": float(gini_simpson_index)
            })

        # Format frequency data for display
        frequency_table = [
            {
                "Value": str(value),
                "Count": int(count),
                "Proportion": round(count / total_samples, 4)
            }
            for value, count in frequencies.most_common()
        ]

        # Add common outputs
        outputs.extend([
            {"name": "Number of unique values", "value": int(unique_values)},
            {"name": "Total samples", "value": int(total_samples)},
            {"name": "Most frequent value", "value": str(most_frequent_value)},
            {"name": "Most frequent count", "value": int(most_frequent_count)},
            {"name": "Value frequencies", "value": frequency_table},
        ])

        return outputs

    except Exception as e:
        raise ValueError(f"Error in diversity calculation: {str(e)}")
