from configparser import ConfigParser

#############################################################################
#
# Config util
#
# Make the config file accessible to other modules
#
#############################################################################

config_path = "config/config.ini"
config_object = ConfigParser()
config = {}


def init_config():
    global config
    config_object.read(config_path)
    config

    for section in config_object.sections():
        config[section] = {}
        for option in config_object.options(section):
            config[section][option] = config_object.get(section, option)


def get_config():
    return config
