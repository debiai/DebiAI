#############################################################################
# Imports
#############################################################################
import debiaiServer.utils.layouts.layouts as layoutsUtils
from debiaiServer.api.v1.debiai.utils import make_hash

#############################################################################
# Analysis dashboard layout Management
#############################################################################


def get_layouts(prev_hash_content=None):
    layouts_overview = layoutsUtils.get_layouts()
    for layout in layouts_overview:
        layout.pop("dataProviderId", None)
        print(layout)

    new_hash = "layout_" + str(make_hash(layouts_overview))
    print(new_hash, " <=> ", prev_hash_content, new_hash == prev_hash_content)

    if new_hash == prev_hash_content:
        return None, 304
    else:
        layouts_answer = {
            "layouts": layouts_overview,
            "hash_content": new_hash,
        }
        return layouts_answer, 200


def post_layout(data):
    layoutsUtils.add_layout(data)
    return None, 204


def delete_layout(id):
    layoutsUtils.delete_layout(id)
    return None, 204
