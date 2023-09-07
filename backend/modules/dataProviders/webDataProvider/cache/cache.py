# This service is used to cache data from the web data provider
# It's used to avoid multiple requests to the web data provider
# It will mainly save the id list of samples, selections and models results
# The ability to cache and the time to live are configurable in the config file

import time
from config.init_config import get_config


class Cache:
    def __init__(self):
        self.cache = {
            "project_id_list": {
                # <id_project>: {
                #   <from>_<to>: {
                #      id_list: [...],
                #      timestamp: <timestamp>
                #   },
                #   total: {
                #      id_list: [...],
                #      timestamp: <timestamp>
                #   }
                # }
            },
            "selection_id_list": {
                # <id_project>: {
                #   <id_selection>: {
                #      id_list: [...],
                #      timestamp: <timestamp>
                #   }
                # }
            },
            "model_result_id_list": {
                # <id_project>: {
                #   <id_model>: {
                #      id_list: [...],
                #      timestamp: <timestamp>
                #   }
                # }
            },
        }
        self.config = get_config()

        self.cache_enabled = self.config["DATA_PROVIDERS_CONFIG"][
            "web_data_provider_cache"
        ]
        self.cache_ttl = self.config["DATA_PROVIDERS_CONFIG"][
            "web_data_provider_cache_duration"
        ]

    # Project id list
    def get_id_list(self, id_project, _from=None, _to=None):
        if not self.cache_enabled:
            return None

        if id_project not in self.cache["project_id_list"]:
            return None

        project_cache = self.cache["project_id_list"][id_project]

        if _from is None or _to is None:
            if "total" not in project_cache:
                return None

            # Check if cache is still valid
            timestamp = project_cache["total"]["timestamp"]
            if time.time() - timestamp > self.cache_ttl:
                # Cache is not valid anymore
                # Delete cache
                del project_cache["total"]
                return None

            return project_cache["total"]["id_list"]

        else:
            key = "{}_{}".format(_from, _to)
            if key not in project_cache:
                return None

            # Check if cache is still valid
            timestamp = project_cache[key]["timestamp"]
            if time.time() - timestamp > self.cache_ttl:
                # Cache is not valid anymore
                # Delete cache
                del project_cache[key]
                return None

            return project_cache[key]["id_list"]

    def set_id_list(self, id_project, id_list, _from=None, _to=None):
        if not self.cache_enabled:
            return

        if id_project not in self.cache["project_id_list"]:
            self.cache["project_id_list"][id_project] = {}

        project_cache = self.cache["project_id_list"][id_project]

        if _from is None or _to is None:
            project_cache["total"] = {
                "id_list": id_list,
                "timestamp": time.time(),
            }
        else:
            key = "{}_{}".format(_from, _to)
            project_cache[key] = {
                "id_list": id_list,
                "timestamp": time.time(),
            }

    # Selection id list
    def get_selection_id_list(self, id_project, id_selection):
        if not self.cache_enabled:
            return None

        if id_project not in self.cache["selection_id_list"]:
            return None

        project_cache = self.cache["selection_id_list"][id_project]

        if id_selection not in project_cache:
            return None

        # Check if cache is still valid
        timestamp = project_cache[id_selection]["timestamp"]

        if time.time() - timestamp > self.cache_ttl:
            # Cache is not valid anymore
            # Delete cache
            del project_cache[id_selection]
            return None

        return project_cache[id_selection]["id_list"]

    def set_selection_id_list(self, id_project, id_selection, id_list):
        if not self.cache_enabled:
            return

        if id_project not in self.cache["selection_id_list"]:
            self.cache["selection_id_list"][id_project] = {}

        project_cache = self.cache["selection_id_list"][id_project]

        project_cache[id_selection] = {
            "id_list": id_list,
            "timestamp": time.time(),
        }

    # Model result id list
    def get_model_result_id_list(self, id_project, id_model):
        if not self.cache_enabled:
            return None

        if id_project not in self.cache["model_result_id_list"]:
            return None

        project_cache = self.cache["model_result_id_list"][id_project]

        if id_model not in project_cache:
            return None

        # Check if cache is still valid
        timestamp = project_cache[id_model]["timestamp"]
        if time.time() - timestamp > self.cache_ttl:
            # Cache is not valid anymore
            # Delete cache
            del project_cache[id_model]
            return None

        return project_cache[id_model]["id_list"]

    def set_model_result_id_list(self, id_project, id_model, id_list):
        if not self.cache_enabled:
            return

        if id_project not in self.cache["model_result_id_list"]:
            self.cache["model_result_id_list"][id_project] = {}

        project_cache = self.cache["model_result_id_list"][id_project]

        project_cache[id_model] = {
            "id_list": id_list,
            "timestamp": time.time(),
        }
