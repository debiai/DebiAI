from configparser import ConfigParser
import os, json


config_path = "config/config.ini"
config_parser = ConfigParser()
config_parser.optionxform = str  # To preserve the case

config = {}


def init_config():
    global config

    # Expected sections:
    # - DATA_PROVIDERS_CONFIG
    # - PYTHON_MODULE_DATA_PROVIDER
    # - WEB_DATA_PROVIDERS
    # - EXPORT_METHODS_CONFIG
    # - EXPORT_METHODS_LIST

    print("===================== CONFIG =======================")

    # Default config
    config = {
        "DATA_PROVIDERS_CONFIG": {"creation": True, "deletion": True},
        "PYTHON_MODULE_DATA_PROVIDER": {"enabled": True},
        "WEB_DATA_PROVIDERS": {},

        "ALGO_HUB_CONFIG": {"creation": True, "deletion": True},
        "ALGO_HUB_LIST": {},

        "EXPORT_METHODS_CONFIG": {"creation": True, "deletion": True},
        "EXPORT_METHODS_LIST": {},
    }

    # First, read the config file
    config_parser.read(config_path)

    for section in config_parser.sections():
        # Data providers
        if section == "DATA_PROVIDERS_CONFIG":
            if "creation" in config_parser[section]:
                if str.lower(config_parser[section]["creation"]) == "false":
                    print("Config file: Data Providers creation disabled")
                    config["DATA_PROVIDERS_CONFIG"]["creation"] = False

            if "deletion" in config_parser[section]:
                if str.lower(config_parser[section]["deletion"]) == "false":
                    print("Config file: Data Providers deletion disabled")
                    config["DATA_PROVIDERS_CONFIG"]["deletion"] = False
            continue

        if section == "PYTHON_MODULE_DATA_PROVIDER":
            if "enabled" in config_parser[section]:
                if str.lower(config_parser[section]["enabled"]) == "false":
                    print("Config file: Python Module Data Provider disabled")
                    config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = False
                elif str.lower(config_parser[section]["enabled"]) == "true":
                    print("Config file: Python Module Data Provider enabled")
                    config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = True
            continue

        if section == "WEB_DATA_PROVIDERS":
            for data_provider in config_parser[section]:
                print(
                    "Config file: detected data provider '"
                    + data_provider
                    + "' from config file"
                )
                config["WEB_DATA_PROVIDERS"][data_provider] = config_parser[section][
                    data_provider
                ]
            continue

        # AlgoHub
        if section == "ALGO_HUB_CONFIG":
            if "creation" in config_parser[section]:
                if str.lower(config_parser[section]["creation"]) == "false":
                    print("Config file: AlgoHub creation disabled")
                    config["ALGO_HUB_CONFIG"]["creation"] = False

            if "deletion" in config_parser[section]:
                if str.lower(config_parser[section]["deletion"]) == "false":
                    print("Config file: AlgoHub deletion disabled")
                    config["ALGO_HUB_CONFIG"]["deletion"] = False
            continue

        if section == "ALGO_HUB_LIST":
            for algo_hub in config_parser[section]:
                print(
                    "Config file: detected AlgoHub '"
                    + algo_hub
                    + "' from config file"
                )
                config["ALGO_HUB_LIST"][algo_hub] = config_parser[section][algo_hub]
            continue

        # Export methods
        if section == "EXPORT_METHODS_CONFIG":
            if "creation" in config_parser[section]:
                if str.lower(config_parser[section]["creation"]) == "false":
                    print("Config file: Export method creation disabled")
                    config["EXPORT_METHODS_CONFIG"]["creation"] = False

            if "deletion" in config_parser[section]:
                if str.lower(config_parser[section]["deletion"]) == "false":
                    print("Config file: Export method deletion disabled")
                    config["EXPORT_METHODS_CONFIG"]["deletion"] = False
            continue

        if section == "EXPORT_METHODS_LIST":
            for export_method in config_parser[section]:
                print(
                    "Config file: detected export method '"
                    + export_method
                    + "' from config file"
                )
                config["EXPORT_METHODS_LIST"][export_method] = config_parser[section][
                    export_method
                ]
            continue

        print("Config section '" + section + "' not recognized, skipping")

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
        
        # Deal with AlgoHub in env variables
        if env_var == "DEBIAI_ALGO_HUB_CREATION_ENABLED":
            # Env var format: DEBIAI_ALGO_HUB_CREATION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: AlgoHub creation disabled")
                config["ALGO_HUB_CONFIG"]["creation"] = False
            continue

        if env_var == "DEBIAI_ALGO_HUB_DELETION_ENABLED":
            # Env var format: DEBIAI_ALGO_HUB_DELETION_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: AlgoHub deletion disabled")
                config["ALGO_HUB_CONFIG"]["deletion"] = False
            continue

        # Deal with AlgoHub list in env variables
        if "DEBIAI_ALGO_HUB" in env_var:
            # Env var format: DEBIAI_ALGO_HUB_<name>=<url>
            if len(env_var.split("_")) != 4:
                print(
                    "Environment variables: invalid environment variable '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_ALGO_HUB_<name>=<url>")
                continue

            algo_hub_name = env_var.split("_")[3]
            algo_hub_url = os.environ[env_var]

            if len(algo_hub_name) == 0:
                print(
                    "Environment variables: invalid AlgoHub name '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_ALGO_HUB_<name>=<url>")
                continue

            print(
                "Environment variables: detected AlgoHub '"
                + algo_hub_name
                + "' from environment variables"
            )

            config["ALGO_HUB_LIST"][algo_hub_name] = algo_hub_url


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

            config["EXPORT_METHODS_LIST"][
                export_method_name
            ] = export_method_type_and_parameters

    print("Config loaded")
    print(json.dumps(config, sort_keys=True, indent=4))


def get_config():
    return config
