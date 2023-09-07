# This service is used to cache data from the web data provider
# It's used to avoid multiple requests to the web data provider
# It will mainly save the id list of samples, selections and models results
# The ability to cache and the time to live are configurable in the config file

import time
from config.init_config import get_config


# Init cache
# def init_cache():


class Cache:
    def __init__(self):
        self.cache = {}
        self.config = get_config()

        self.cache_enabled = self.config["DATA_PROVIDERS_CONFIG"][
            "web_data_provider_cache"
        ]
        self.cache_ttl = self.config["DATA_PROVIDERS_CONFIG"][
            "web_data_provider_cache_duration"
        ]
        print("Cache enabled: {}".format(self.cache_enabled))
        print("Cache TTL: {}".format(self.cache_ttl))

    def get(self, key):
        if self.cache_enabled:
            if key in self.cache:
                cache_value = self.cache[key]
                if cache_value["timestamp"] + self.cache_ttl > time.time():
                    return cache_value["data"]
                else:
                    del self.cache[key]
        return None

    def set(self, key, value):
        if self.cache_enabled:
            self.cache[key] = {
                "data": value,
                "timestamp": time.time(),
            }
