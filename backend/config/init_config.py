from configparser import ConfigParser
import os, json


config_path = "config/config.ini"
config_parser = ConfigParser()
config_parser.optionxform = str  # To preserve the case

config = {}


def init_config():
    global config

    # Expected sections:
    # - PYTHON_MODULE_DATA_PROVIDER
    # - WEB_DATA_PROVIDERS
    # - EXPORT_METHODS

    print("===================== CONFIG =======================")

    # First, read the config file
    config_parser.read(config_path)
    config = {
        "PYTHON_MODULE_DATA_PROVIDER": {"enabled": True},
        "WEB_DATA_PROVIDERS": {},
        "EXPORT_METHODS": {},
    }

    for section in config_parser.sections():
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

        if section == "EXPORT_METHODS":
            for export_method in config_parser[section]:
                print(
                    "Config file: detected export method '"
                    + export_method
                    + "' from config file"
                )
                config["EXPORT_METHODS"][export_method] = config_parser[section][
                    export_method
                ]
            continue

        print("Config section '" + section + "' not recognized, skipping")

    # Then deal with environment variables
    for env_var in os.environ:
        # Deal with PYTHON_MODULE_DATA_PROVIDER in env variables
        if env_var == "DEBIAI_PYTHON_MODULE_DATA_PROVIDER_ENABLED":
            # Env var format: DEBIAI_PYTHON_MODULE_DATA_PROVIDER_ENABLED=<True|False>
            if str.lower(os.environ[env_var]) == "false":
                print("Environment variables: Python Module Data Provider disabled")
                config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = False
            elif str.lower(os.environ[env_var]) == "true":
                print("Environment variables: Python Module Data Provider enabled")
                config["PYTHON_MODULE_DATA_PROVIDER"]["enabled"] = True

        # Deal with Data Providers in env variables
        if "DEBIAI_WEB_DATA_PROVIDER" in env_var:
            # Env var format: DEBIAI_DATA_PROVIDER_<name>=<url>
            if len(env_var.split("_")) != 5:
                print(
                    "Environment variables: invalid environment variable '"
                    + env_var
                    + "', skipping"
                )
                print("Expected format: DEBIAI_WEB_DATA_PROVIDER_<name>=<url>")
                continue

            data_provider_name = env_var.split("_")[3]
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

        # Deal with Export Methods
        if "DEBIAI_EXPORT_METHOD" in env_var:
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

            if "EXPORT_METHODS" not in config:
                config["EXPORT_METHODS"] = {}

            config["EXPORT_METHODS"][
                export_method_name
            ] = export_method_type_and_parameters

    print("Config loaded")
    print(json.dumps(config, sort_keys=True, indent=4))


def get_config():
    return config
