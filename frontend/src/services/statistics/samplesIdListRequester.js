import backendDialog from "../backendDialog";
import services from "../services";

async function get_list(data) {
  // Get the list of samples ID of the project according to the chosen selection(s) and/or model(s)
  // Option 1 : get samples id list
  // Option 2 : get samples id list from selections (intersection or union)
  // Option 3 : get samples id list from model results (common or not)
  // Option 4 : Option 2 + 3
  // Return option : from and to for streaming purpose

  const code = services.startRequest("Getting samples ID list");

  let id_list = [];
  let nb_from_selection = 0;
  let nb_from_models = 0; // Number of samples from models, used to calculate
  // How many predictions will result from the models union

  // Option 1 : No selections or models, get samples id list
  if (
    (!data.selectionIds || data.selectionIds.length === 0) &&
    (!data.modelIds || data.modelIds.length === 0)
  ) {
    if (data.from && data.to)
      id_list = await backendDialog.get_id_list(data.analysis, data.from, data.to);
    else id_list = await backendDialog.get_id_list(data.analysis);

    nb_from_selection = id_list.length;
  }

  // Option 2 : get samples id list from selections (intersection or union)
  if (data.selectionIds && data.selectionIds.length > 0) {
    const selectionsIdCode = services.startProgressRequest("Getting selections ID list");
    const selection_intersection = data.selectionIntersection;

    try {
      let i = 0;
      for (const selection_id of data.selectionIds) {
        i++;
        services.updateRequestProgress(selectionsIdCode, i / data.selectionIds.length);

        // Get the selection id list
        const selection_sample_ids = await backendDialog.get_selection_id_list(selection_id);
        if (id_list.length === 0) {
          // Set the first selection id list
          id_list = selection_sample_ids;
        } else {
          // Get the intersection or union between
          // the current selection and the previous one
          if (selection_intersection) {
            const selection_sample_ids_set = new Set(selection_sample_ids);
            id_list = id_list.filter((sampleId) => selection_sample_ids_set.has(sampleId));
            if (id_list.length === 0) break;
          } else {
            id_list = [...new Set([...id_list, ...selection_sample_ids])];
          }
        }
      }

      nb_from_selection = id_list.length;
    } catch (e) {
      services.endRequest(code);
      throw e;
    } finally {
      services.endRequest(selectionsIdCode);
    }
  }

  // Option 3 : get id list from model results samples ID (common or not)
  if (data.modelIds && data.modelIds.length > 0) {
    if (data.selectionIds && data.selectionIds.length > 0) {
      // Option 4 : Option 2 + 3, intersection of selections and model results
      // If the selection id list is empty, the result will be empty
      if (id_list.length === 0) {
        nb_from_models = null;
        services.endRequest(code);
        return {
          samples: [],
          nbSamples: 0,
          nbFromSelection: 0,
          nbFromModels: 0,
        };
      }
    }

    const modelsIdCode = services.startProgressRequest("Getting models ID list");

    const common_results = data.commonResults;
    let model_result_ids = [];

    try {
      let i = 0;
      for (const model_id of data.modelIds) {
        i++;
        services.updateRequestProgress(modelsIdCode, i / data.modelIds.length);

        // First get the model results id list
        const model_sample_ids = await backendDialog.get_model_results_id_list(model_id);

        // Then get the common or not common samples id list
        if (model_result_ids.length === 0) {
          model_result_ids = model_sample_ids;
          nb_from_models += model_sample_ids.length;
        } else {
          if (common_results) {
            // Get the intersection between the current model results and the previous one
            const model_sample_ids_set = new Set(model_sample_ids);
            model_result_ids = model_result_ids.filter((sampleId) =>
              model_sample_ids_set.has(sampleId)
            );

            if (model_result_ids.length === 0) break;
          } else {
            nb_from_models += model_sample_ids.length;
            model_result_ids = [...new Set([...model_result_ids, ...model_sample_ids])];
          }
        }
      }

      if (data.selectionIds && data.selectionIds.length > 0) {
        // Option 4 : Option 2 + 3, intersection of selections and model results
        const selection_sample_ids_set = new Set(id_list);
        id_list = model_result_ids.filter((sampleId) => selection_sample_ids_set.has(sampleId));
      } else {
        // Option 3 : only model results
        id_list = model_result_ids;
        nb_from_selection = model_result_ids.length;
      }
    } catch (e) {
      services.endRequest(code);
      throw e;
    } finally {
      services.endRequest(modelsIdCode);
    }
  }

  services.endRequest(code);

  return {
    samples: id_list,
    nbSamples: id_list.length,
    nbFromSelection: nb_from_selection,
    nbFromModels: nb_from_models,
  };
}

export default {
  get_list,
};
