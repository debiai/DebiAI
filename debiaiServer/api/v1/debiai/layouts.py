#############################################################################
# Imports
#############################################################################
import debiaiServer.utils.layouts.layouts as layoutsUtils
from debiaiServer.api.v1.debiai.utils import make_hash

#############################################################################
# LAYOUTS Management with 304 support
#############################################################################


def get_layouts(prev_hash_content=None):
    """
    Get all layouts with hash-based caching support.
    Returns 304 if content hasn't changed, 200 with data if it has.
    """
    layouts_overview = layoutsUtils.get_layouts()

    # Create hash from the layouts data
    new_hash = "layouts_" + str(make_hash(layouts_overview))

    # Check if content has changed
    if new_hash == prev_hash_content:
        return None, 304
    else:
        response = {"layouts": layouts_overview, "hash_content": new_hash}
        return response, 200


def post_layout(data):
    """Create a new layout"""
    layoutsUtils.add_layout(data)
    return None, 204


def delete_layout(id):
    """Delete a layout by ID"""
    layoutsUtils.delete_layout(id)
    return None, 204
