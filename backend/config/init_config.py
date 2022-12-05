from configparser import ConfigParser
import os


config_path = "config/config.ini"
config_parser = ConfigParser()
config_parser.optionxform = str  # To preserve the case

config = {}

def init_config():
    global config
    
    print("========= Starting setup config  ==========")
    # First, read the config file
    config_parser.read(config_path)
    config = {}
    
    for section in config_parser.sections():
        config[section] = {}
        for option in config_parser.options(section):
            config[section][option] = config_parser.get(section, option)
    
    print("Config sections from file " + config_path + " loaded")
    
    print(config)
    
    
    for env_var in os.environ:
        
        # Deal with Data Providers in env variables
        if "DEBIAI_DATA_PROVIDER" in env_var:
            # Env var format: DEBIAI_DATA_PROVIDER_<name>=<url>
            if len(env_var.split("_")) != 4:
                print("Invalid environment variable " + env_var + ", skipping")
                print("Expected format: DEBIAI_DATA_PROVIDER_<name>=<url>")
                continue

            data_provider_name = env_var.split("_")[3]
            data_provider_url = os.environ[env_var]

            if len(data_provider_name) == 0:
                print("Invalid data provider name " + env_var + ", skipping")
                print("Expected format: DEBIAI_DATA_PROVIDER_<name>=<url>")
                continue

            print(
                "Detected data provider '"
                + data_provider_name
                + "' from environment variables"
            )

            if "DATA_PROVIDERS" not in config:
                config["DATA_PROVIDERS"] = {}

            config["DATA_PROVIDERS"][data_provider_name] = data_provider_url
        # Deal with Export Methods
        if "DEBIAI_EXPORT_METHOD" in env_var:
            # Env var format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
            if len(env_var.split("_")) != 4:
                print("Invalid environment variable " + env_var + ", skipping")
                print(
                    "Expected format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
                )
                continue

            export_method_name = env_var.split("_")[3]
            export_method_type_and_parameters = os.environ[env_var]

            if len(export_method_name) == 0:
                print("Invalid export method name " + env_var + ", skipping")
                print(
                    "Expected format: DEBIAI_EXPORT_METHOD_<name>=<type>, <param1>, <param2>, ..."
                )
                continue

            print(
                "Detected export method '"
                + export_method_name
                + "' from environment variables"
            )

            if "EXPORT_METHODS" not in config:
                config["EXPORT_METHODS"] = {}

            config["EXPORT_METHODS"][
                export_method_name
            ] = export_method_type_and_parameters



def get_config():
    return config