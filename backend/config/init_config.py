from configparser import ConfigParser
from termcolor import colored

import os
import json

config_path = "config/config.ini"
config_parser = ConfigParser()

DEBUG_MAIN_COLOR = "light_blue"
DEBUG_SECONDARY_COLOR = "blue"

# Default config
config = {
    "DATA_PROVIDERS_CONFIG": {
        "creation": True,
        "deletion": True,
    },
    "PYTHON_MODULE_DATA_PROVIDER": {
        "enabled": True,
        "allow_create_projects": True,
        "allow_delete_projects": True,
        "allow_create_selections": True,
        "allow_delete_selections": True,
        "allow_create_models": True,
        "allow_delete_models": True,
        "allow_insert_results": True,
    },
    "WEB_DATA_PROVIDERS_CONFIG": {
        "cache": True,
        "cache_duration": 120,
    },
    "WEB_DATA_PROVIDERS": {
        # "name": "url"
    },
    "ALGO_PROVIDERS_CONFIG": {
        "enable_integrated": True,
        "creation": True,
        "deletion": True,
    },
    "ALGO_PROVIDERS": {
        # "name": "url"
    },
    "EXPORT_METHODS_CONFIG": {
        "creation": True,
        "deletion": True,
    },
    "EXPORT_METHODS": {
        # "name": "type, param1, param2, ..."
    },
}

# Env vars mapping
ENV_VAR_MAPPING = {
    "DATA_PROVIDERS_CONFIG": {
        "creation": "DEBIAI_DATA_PROVIDERS_CREATION_ENABLED",
        "deletion": "DEBIAI_DATA_PROVIDERS_DELETION_ENABLED",
    },
    "PYTHON_MODULE_DATA_PROVIDER": {
        "enabled": "DEBIAI_PYTHON_MODULE_DATA_PROVIDER_ENABLED",
        "allow_create_projects": "DEBIAI_INTEGRATED_DP_ALLOW_CREATE_PROJECTS",
        "allow_delete_projects": "DEBIAI_INTEGRATED_DP_ALLOW_DELETE_PROJECTS",
        "allow_create_selections": "DEBIAI_INTEGRATED_DP_ALLOW_CREATE_SELECTIONS",
        "allow_delete_selections": "DEBIAI_INTEGRATED_DP_ALLOW_DELETE_SELECTIONS",
        "allow_create_models": "DEBIAI_INTEGRATED_DP_ALLOW_CREATE_MODELS",
        "allow_delete_models": "DEBIAI_INTEGRATED_DP_ALLOW_DELETE_MODELS",
        "allow_insert_results": "DEBIAI_INTEGRATED_DP_ALLOW_INSERT_RESULTS",
    },
    "WEB_DATA_PROVIDERS_CONFIG": {
        "cache": "DEBIAI_WEB_DATA_PROVIDERS_CACHE_ENABLED",
        "cache_duration": "DEBIAI_WEB_DATA_PROVIDERS_CACHE_DURATION",
    },
    "WEB_DATA_PROVIDERS": "DEBIAI_WEB_DATA_PROVIDERS_*",
    "ALGO_PROVIDERS_CONFIG": {
        "enable_integrated": "DEBIAI_ALGO_PROVIDERS_CONFIG_ENABLE_INTEGRATED",
        "creation": "DEBIAI_ALGO_PROVIDERS_CONFIG_CREATION",
        "deletion": "DEBIAI_ALGO_PROVIDERS_CONFIG_DELETION",
    },
    "ALGO_PROVIDERS": "DEBIAI_ALGO_PROVIDERS_*",
    "EXPORT_METHODS_CONFIG": {
        "creation": "DEBIAI_EXPORT_METHODS_CONFIG_CREATION",
        "deletion": "DEBIAI_EXPORT_METHODS_CONFIG_DELETION",
    },
    "EXPORT_METHODS": "DEBIAI_EXPORT_METHODS_*",
}


def get_config_value(section, key, config_parser):
    # Return the value of the key in the section of the config_parser
    # Or return the ENV_VAR if it exists

    value = None
    ENV_VAR = ENV_VAR_MAPPING[section][key]

    # Get the value from the config file
    if section in config_parser and key in config_parser[section]:
        value = config_parser[section][key]

    # Get the value from the environment variables
    if ENV_VAR in os.environ:
        value = os.environ[ENV_VAR]

    if value is None:
        print(
            "Key "
            + colored(section, DEBUG_SECONDARY_COLOR)
            + " / "
            + colored(key, DEBUG_SECONDARY_COLOR)
            + " in config or in "
            + colored(ENV_VAR, DEBUG_SECONDARY_COLOR)
            + " env var, using default"
        )
        return None

    return value


def set_config_value(section, key, value):
    global config

    if section in config and key in config[section]:
        if config[section][key] != value:
            # The default value is different from the one in the config file
            config[section][key] = value

            print(
                "Overriding "
                + colored(section, DEBUG_MAIN_COLOR)
                + " / "
                + colored(key, DEBUG_MAIN_COLOR)
                + " with value "
                + colored(value, DEBUG_MAIN_COLOR)
            )


def init_config():
    global config

    print("===================== CONFIG =======================")

    config_parser.read(config_path)

    for section in config.keys():
        # Deal with boolean, integer and string values
        for key in config[section].keys():
            # Get the value from the config file or the environment variables
            value = get_config_value(section, key, config_parser)

            if value is None:
                continue

            # Deal with booleans
            if type(config[section][key]) == bool:
                if str.lower(config_parser[section][key]) == "false":
                    set_config_value(section, key, False)
                elif str.lower(config_parser[section][key]) == "true":
                    set_config_value(section, key, True)
                else:
                    print(
                        "Invalid boolean value for "
                        + colored(key, DEBUG_MAIN_COLOR)
                        + ", using default value"
                    )
                    continue

            # Deal with integers
            elif type(config[section][key]) == int:
                try:
                    set_config_value(section, key, int(config_parser[section][key]))
                except ValueError:
                    print(
                        "Invalid integer value for "
                        + colored(key, DEBUG_MAIN_COLOR)
                        + ", using default value"
                    )
                    continue

            # Deal with strings
            elif type(config[section][key]) == str:
                set_config_value(section, key, str(config_parser[section][key]))

        # Deal with Web data-providers, Algo-providers and Export methods
        if section in ["WEB_DATA_PROVIDERS", "ALGO_PROVIDERS", "EXPORT_METHODS"]:
            for element_name in config_parser[section]:
                parameters = config_parser[section][element_name]
                print(
                    "Adding "
                    + section.lower().replace("_", "-")[0:-1]
                    + " "
                    + colored(element_name, DEBUG_MAIN_COLOR)
                    + " ("
                    + colored(parameters, DEBUG_MAIN_COLOR)
                    + ")"
                )

                config[section][element_name] = parameters

    print("done")
    exit()

    # Then deal with environment variables
    for env_var in os.environ:
        # Deal with DATA_PROVIDERS in env variables
        if env_var == "DEBIAI_DATA_PROVIDERS_CREATION_ENABLED":
            # Env var format: DEBIAI_DATA_PROVIDERS_CREATION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Data Providers creation disabled")
                config["DATA_PROVIDERS_CONFIG"]["creation"] = False
            continue

        if env_var == "DEBIAI_DATA_PROVIDERS_DELETION_ENABLED":
            # Env var format: DEBIAI_DATA_PROVIDERS_DELETION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Data Providers deletion disabled")
                config["DATA_PROVIDERS_CONFIG"]["deletion"] = False
            continue

        # Deal with PYTHON_MODULE_DATA_PROVIDER in env variables
        if env_var == "DEBIAI_PYTHON_MODULE_DATA_PROVIDER_ENABLED":
            # Env var format: DEBIAI_PYTHON_MODULE_DATA_PROVIDER_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Python Module Data Provider disabled")
                config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = False
            elif str.lower(os.environ[env_var]) == "true":
                print("Environment variables: Python Module Data Provider enabled")
                config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = True
            continue

        # Deal with Data Providers in env variables
        if env_var == "DEBIAI_WEB_DATA_PROVIDERS_CACHE_ENABLED":
            # Env var format: DEBIAI_WEB_DATA_PROVIDERS_CACHE_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Web Data Provider cache disabled")
                config["DATA_PROVIDERS_CONFIG"]["web_data_provider_cache"] = False
            continue

        if env_var == "DEBIAI_WEB_DATA_PROVIDERS_CACHE_DURATION":
            # Env var format: DEBIAI_WEB_DATA_PROVIDERS_CACHE_DURATION=<duration>
            try:
                config["DATA_PROVIDERS_CONFIG"][
                    "web_data_provider_cache_duration"
                ] = int(os.environ[env_var])
            except ValueError:
                print(
                    "Environment variables: Invalid Web Data Provider cache duration,",
                    "defaulting to 120 seconds",
                )
            continue

        if "DEBIAI_WEB_DATA_PROVIDER" in env_var:
            # Env var format: DEBIAI_WEB_DATA_PROVIDER_<name>=<url>
            if len(env_var.split("_")) != 5:
                print(
                    "Environment variables: invalid environment variable '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_WEB_DATA_PROVIDER_<name>=<url>")
                continue

            data_provider_name = env_var.split("_")[4]
            data_provider_url = os.environ[env_var]

            if len(data_provider_name) == 0:
                print(
                    "Environment variables: invalid data provider name '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_WEB_DATA_PROVIDER_<name>=<url>")
                continue

            print(
                "Environment variables: detected Web data provider '"
                + data_provider_name
                + "' from environment variables"
            )

            config["WEB_DATA_PROVIDERS"][data_provider_name] = data_provider_url

        # Deal with AlgoProvider in env variables
        if env_var == "DEBIAI_ALGO_PROVIDERS_ENABLE_INTEGRATED":
            # Env var format: DEBIAI_ALGO_PROVIDERS_ENABLE_INTEGRATED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Integrated Data Providers disabled")
                config["DATA_PROVIDERS_CONFIG"]["enable_integrated"] = False
            continue

        if env_var == "DEBIAI_ALGO_PROVIDERS_CREATION_ENABLED":
            # Env var format: DEBIAI_ALGO_PROVIDERS_CREATION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: AlgoProvider creation disabled")
                config["ALGO_PROVIDERS_CONFIG"]["creation"] = False
            continue

        if env_var == "DEBIAI_ALGO_PROVIDERS_DELETION_ENABLED":
            # Env var format: DEBIAI_ALGO_PROVIDERS_DELETION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: AlgoProvider deletion disabled")
                config["ALGO_PROVIDERS_CONFIG"]["deletion"] = False
            continue

        # Deal with AlgoProvider list in env variables
        if "DEBIAI_ALGO_PROVIDER" in env_var:
            # Env var format: DEBIAI_ALGO_PROVIDER_<name>=<url>
            if len(env_var.split("_")) != 4:
                print(
                    "Environment variables: invalid environment variable '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_ALGO_PROVIDER_<name>=<url>")
                continue

            algo_provider_name = env_var.split("_")[3]
            algo_provider_url = os.environ[env_var]

            if len(algo_provider_name) == 0:
                print(
                    "Environment variables: invalid AlgoProvider name '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_ALGO_PROVIDER_<name>=<url>")
                continue

            print(
                "Environment variables: detected AlgoProvider '"
                + algo_provider_name
                + "' from environment variables"
            )

            config["ALGO_PROVIDERS"][algo_provider_name] = algo_provider_url

        # Deal with Export Methods in env variables
        if env_var == "DEBIAI_EXPORT_METHODS_CREATION_ENABLED":
            # Env var format: DEBIAI_EXPORT_METHODS_CREATION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Export method creation disabled")
                config["EXPORT_METHODS_CONFIG"]["creation"] = False
            continue

        if env_var == "DEBIAI_EXPORT_METHODS_DELETION_ENABLED":
            # Env var format: DEBIAI_EXPORT_METHODS_DELETION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Export method deletion disabled")
                config["EXPORT_METHODS_CONFIG"]["deletion"] = False
            continue

        # Deal with Export Methods list in env variables
        if "DEBIAI_EXPORT_METHOD_" in env_var:
            # Env var format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
            if len(env_var.split("_")) != 4:
                print(
                    "Environment variables: invalid environment variable '"
                    + env_var
                    + "', skipping"
                )
                print(
                    "Expected format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
                )
                continue

            export_method_name = env_var.split("_")[3]
            export_method_type_and_parameters = os.environ[env_var]

            if len(export_method_name) == 0:
                print(
                    "Environment variables: Invalid export method name "
                    + env_var
                    + ", skipping"
                )
                print(
                    "Expected format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
                )
                continue

            print(
                "Environment variables: Detected export method '"
                + export_method_name
                + "' from environment variables"
            )

            config["EXPORT_METHODS"][
                export_method_name
            ] = export_method_type_and_parameters

    print("Config loaded")
    print(json.dumps(config, sort_keys=True, indent=4))


def get_config():
    return config
