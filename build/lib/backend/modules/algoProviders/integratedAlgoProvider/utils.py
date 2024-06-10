def get_input_from_inputs(
    inputs, input_name, expected_input_type=None, expected_list_type=None
):
    # Get the input from of the inputs list from a given name
    # Check the type and the subtype if needed

    for i, input in enumerate(inputs):
        if "name" not in input:
            raise TypeError("Input n°{} has no name".format(i))

        if "value" not in input:
            raise TypeError("Input {} has no value".format(input["name"]))

        if input["name"] == input_name:
            # Check the type
            if expected_input_type == "number":
                if not isinstance(input["value"], (int, float)):
                    raise TypeError(
                        "Input {} is not a number, but a {}".format(
                            input_name, type(input["value"])
                        )
                    )
            elif expected_input_type == "string":
                if not isinstance(input["value"], str):
                    raise TypeError(
                        "Input {} is not a string but a {}".format(
                            input_name, type(input["value"])
                        )
                    )
            elif expected_input_type == "array":
                if not isinstance(input["value"], list):
                    raise TypeError(
                        "Input {} is not an array but a {}".format(
                            input_name, type(input["value"])
                        )
                    )

                # Check the subtype
                if expected_list_type == "number":
                    for value in input["value"]:
                        if not isinstance(value, (int, float)):
                            raise TypeError(
                                "Input {} is not an array of numbers but of {}".format(
                                    input_name, type(value)
                                )
                            )
                elif expected_list_type == "string":
                    for value in input["value"]:
                        if not isinstance(value, str):
                            raise TypeError(
                                "Input {} is not an array of strings but of {}".format(
                                    input_name, type(value)
                                )
                            )

            # Return the value
            return input["value"]

    raise TypeError("Input {} not found in inputs".format(input_name))
