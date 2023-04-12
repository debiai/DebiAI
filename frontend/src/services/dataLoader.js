import store from "../store";
// import cacheService from './cacheService'
import services from "./services";

const backendDialog = require("./backendDialog");

//
//  Need to take position on wich columns stay availiable or not
//
const CATEGORIES = [
  { blName: "inputs", singleName: "input" },
  { blName: "groundTruth", singleName: "ground truth" },
  { blName: "contexts", singleName: "context" },
  { blName: "others", singleName: "other" },
  { blName: "features", singleName: "features" },
  { blName: "annotations", singleName: "annotations" },
];

// Requests functions
function startRequest(name) {
  let requestCode = services.uuid();
  store.commit("startRequest", { name, code: requestCode });
  return requestCode;
}
function startProgressRequest(name) {
  let requestCode = services.uuid();
  store.commit("startRequest", { name, code: requestCode, progress: 0 });
  return requestCode;
}
function updateRequestProgress(code, progress) {
  store.commit("updateRequestProgress", { code, progress });
}
function updateRequestQuantity(code, quantity) {
  store.commit("updateRequestQuantity", { code, quantity });
}
function endRequest(code) {
  store.commit("endRequest", code);
}
async function getDataProviderLimit() {
  try {
    let dataProviderInfo = await backendDialog.default.getSingleDataProvider();

    const dataProviderLimit = {
      maxIdLimit: dataProviderInfo.maxSampleIdByRequest || 10000,
      maxDataLimit: dataProviderInfo.maxSampleDataByRequest || 2000,
      maxResultLimit: dataProviderInfo.maxResultByRequest || 5000,
    };

    return dataProviderLimit;
  } catch (error) {
    console.log("Error while getting data provider limit, using default values");
    console.log(error);

    return {
      maxIdLimit: 10000,
      maxDataLimit: 2000,
      maxResultLimit: 5000,
    };
  }
}

// Get project samples Id list functions
async function getProjectSamplesIdList(
  projectMetadata,
  analysisId,
  selectionIds = [],
  selectionIntersection = false,
  modelIds = [],
  commonResults = false
) {
  // Returns the list of samples id for a project
  // this need to be done in a sequential way to avoid
  // too big requests
  const accepteSize = projectMetadata.dataProvider.maxIdLimit;
  const projectNbSamples = projectMetadata.nbSamples;

  // If we have no samples, we don't search for samples ID
  if (projectNbSamples === 0) return [];

  // If the project is small, we gather all ID at once
  // If we are analyzing selections or models, we don't split the request (not implemented yet)
  if (
    projectNbSamples !== null &&
    (projectNbSamples <= accepteSize || selectionIds.length > 0 || modelIds.length > 0)
  ) {
    // At the moment, we gather all ID when we deal with selections and models
    // If we have a small project, we gather all ID
    // Also, if we don't have the number of samples, we gather all ID
    const res = await backendDialog.default.getProjectSamples({
      analysis: { id: analysisId, start: true, end: true },
      selectionIds,
      selectionIntersection,
      modelIds,
      commonResults,
    });
    return res.samples;
  } else if (projectNbSamples === null) {
    // If we don't kwow the number of samples, we gather all ID by chunks
    // We stop when we get less samples than the chunk size
    let samplesIdList = [];
    let i = 0;
    console.warn("Project samples number is not known, loading samples ID list by chunks");
    let requestCode = startRequest("Step 1/2: Loading the data ID list");

    try {
      console.time("getProjectSamplesIdList");
      while (true) {
        const from = i * accepteSize;
        const to = (i + 1) * accepteSize - 1;

        // Deal with the analysis info
        const analysis = { id: analysisId, start: false, end: false };
        if (i === 0) analysis.start = true;

        // Send the request
        const res = await backendDialog.default.getProjectSamples({ analysis, from, to });

        if (res.samples.length === 0) {
          console.log("No samples found while loading project samples ID list");
          break;
        }

        // Add the samples to the list
        samplesIdList = samplesIdList.concat(res.samples);
        console.log("Current samples ID list length: ", samplesIdList.length);

        // If we get less samples than the chunk size, we stop
        if (res.samples.length < accepteSize) {
          console.log(
            "Last samples found while loading project samples ID list",
            res.samples.length,
            "<",
            accepteSize
          );
          break;
        }

        // Update a new progress bar counter
        updateRequestQuantity(requestCode, samplesIdList.length);

        i++;
      }
      console.timeEnd("getProjectSamplesIdList");
      endRequest(requestCode);
    } catch (error) {
      console.timeEnd("getProjectSamplesIdList");
      endRequest(requestCode);
      throw error;
    }

    console.log("Request done, ", samplesIdList.length, " samples found");
    return samplesIdList;
  } else {
    // We gather all the project samples ID
    // We need to split it in multiple requests
    let nbRequest = Math.ceil(projectNbSamples / accepteSize);
    let samplesIdList = [];

    console.log("Splitting ID list request in ", nbRequest, " requests");
    let requestCode = startProgressRequest("Step 1/2: Loading the data ID list");

    try {
      console.time("getProjectSamplesIdList");
      for (let i = 0; i < nbRequest; i++) {
        const from = i * accepteSize;
        const to = Math.min((i + 1) * accepteSize, projectNbSamples) - 1;

        // Deal with the analysis info
        const analysis = { id: analysisId, start: false, end: false };
        if (i === 0) analysis.start = true;
        if (i === nbRequest - 1) analysis.end = true;

        // Send the request
        const res = await backendDialog.default.getProjectSamples({ analysis, from, to });

        if (res.samples.length === 0)
          throw "No samples found while loading project samples ID list from " + from + " to " + to;
        if (res.samples.length !== to - from + 1)
          throw (
            "Wrong number of samples while loading project samples ID list from " +
            from +
            " to " +
            to +
            ", got " +
            res.samples.length +
            " instead of " +
            (to - from + 1)
          );

        // Add the samples to the list
        samplesIdList = samplesIdList.concat(res.samples);
        updateRequestProgress(requestCode, (i + 1) / nbRequest);
      }
      console.timeEnd("getProjectSamplesIdList");
      endRequest(requestCode);
    } catch (error) {
      console.timeEnd("getProjectSamplesIdList");
      endRequest(requestCode);
      throw error;
    }

    console.log(
      "Request done, ",
      samplesIdList.length,
      " samples found over ",
      projectNbSamples,
      " samples requested"
    );

    // Check unicity of samples ID
    let uniqueSamplesIdList = [...new Set(samplesIdList)];
    if (uniqueSamplesIdList.length !== samplesIdList.length)
      console.warn(
        "Samples ID list is not unique, ",
        samplesIdList.length - uniqueSamplesIdList.length,
        " duplicates found over ",
        samplesIdList.length,
        " samples"
      );

    return samplesIdList;
  }
}
async function getProjectMetadata({ considerResults }) {
  let projectInfo = await backendDialog.default.getProject();
  if (projectInfo.nbSamples === undefined) projectInfo.nbSamples = null;

  // Labels creation from project columns
  var metaData = {
    timestamp: projectInfo.creationDate,
    nbSamples: projectInfo.nbSamples,
    labels: ["Data ID"],
    categories: ["other"],
    type: ["auto"],
  };

  projectInfo.columns.forEach((column) => {
    metaData.labels.push(column.name);
    metaData.categories.push(column.category);
    metaData.type.push(column.type);
  });

  // In case we are loading the results
  if (considerResults && "resultStructure" in projectInfo) {
    // push model Name
    metaData.labels.push("model");
    metaData.categories.push("results");

    // push model expected results
    projectInfo.resultStructure.forEach((data) => {
      metaData.labels.push(data.name);
      metaData.categories.push("results");
    });
  }
  return metaData;
}
async function downloadSamplesData(projectMetadata, sampleIds, analysisId) {
  const CHUNK_SIZE = projectMetadata.dataProvider.maxDataLimit;
  let pulledData = 0;
  let nbSamples = sampleIds.length;

  // Create a request
  let requestCode = startProgressRequest("Loading the project data");
  console.time("Loading the project data");
  // Pull the tree
  let retArray = [];
  let retDataIdlist = [];

  try {
    while (pulledData < nbSamples) {
      const samplesToPull = sampleIds.slice(pulledData, pulledData + CHUNK_SIZE);

      // First, pull the samples from the browser memory
      // let cachedSamples = await cacheService.getSamplesByIds(projectMetadata.timestamp, samplesToPull)
      // let samplesToDownload = samplesToPull.filter(sampleId => !(sampleId in cachedSamples))
      // retArray = [...retArray, ...Object.values(cachedSamples)]
      // retDataIdlist = [...retDataIdlist, ...Object.keys(cachedSamples)]
      const samplesToDownload = samplesToPull;

      if (samplesToDownload.length) {
        // Then download the missing samples
        console.log(samplesToDownload.length + " samples to download");

        // Deal with the analysis info
        const analysis = { id: analysisId, start: false, end: false };
        if (pulledData === 0) analysis.start = true;
        if (pulledData + samplesToDownload.length === nbSamples) analysis.end = true;

        // Send the request
        const downloadedSamples = await backendDialog.default.getBlocksFromSampleIds(
          samplesToDownload,
          analysis
        );

        // We receive an map of samples:
        // {
        //   "id1": [0, 1, 2, 3, ...],
        //   "id2": [0, 1, 2, 3, ...],
        //   "id3": [0, 1, 2, 3, ...]
        //   ...
        // }
        const map = downloadedSamples.data;

        // Add the data ID to the samples
        for (let sampleId in map) map[sampleId].unshift(sampleId);

        // Stack the samples
        retArray = [...retArray, ...Object.values(map)];
        retDataIdlist = [...retDataIdlist, ...Object.keys(map)];

        // Store the samples in the cache
        // await cacheService.storeSamples(timestamp, map) TODO
      }

      // Update the progress
      pulledData += CHUNK_SIZE;
      updateRequestProgress(requestCode, pulledData / nbSamples);
    }
  } finally {
    endRequest(requestCode);
    console.timeEnd("Loading the project data");
  }
  return { dataArray: retArray, sampleIdList: retDataIdlist };
}

// Model results
async function downloadResults(projectMetadata, modelId, sampleIds) {
  const CHUNK_SIZE = projectMetadata.dataProvider.maxResultLimit;
  let pulledData = 0;
  // Create a request
  let requestCode = services.uuid();
  store.commit("startRequest", {
    name: modelId,
    code: requestCode,
    progress: 0,
  });
  let modelResultsRet = {};

  try {
    // Not done because more time is spent storing the cache : First, pull the tree from the browser memory
    // let cachedResults = await cacheService.getModelResultsByIds(timestamp, modelId, sampleIds)
    // let resutlsToDownload = sampleIds.filter(sampleId => !(sampleId in cachedResults))

    // add the cached results to our results without empty one
    // for (const sampleId in cachedResults)
    //   if (cachedResults[sampleId] !== null) modelResultsRet[sampleId] = cachedResults[sampleId]

    // Pull the tree
    // let nbSamples = resutlsToDownload.length
    // if (nbSamples) console.log(nbSamples + " results to download");

    let nbSamples = sampleIds.length;
    while (pulledData < nbSamples) {
      let samplesToPull = sampleIds.slice(pulledData, pulledData + CHUNK_SIZE);

      let modelResults = await backendDialog.default.getModelResults(modelId, samplesToPull);
      modelResultsRet = Object.assign({}, modelResultsRet, modelResults);

      // let resultsToSave = {}
      // samplesToPull.forEach(sampleId => {
      //   resultsToSave[sampleId] = sampleId in modelResultsRet ? modelResultsRet[sampleId] : null
      // });
      // cacheService.saveResults(timestamp, modelId, resultsToSave)

      pulledData += CHUNK_SIZE;
      store.commit("updateRequestProgress", {
        code: requestCode,
        progress: pulledData / nbSamples,
      });
    }
  } catch (error) {
    store.commit("endRequest", requestCode);
    throw error;
  }
  store.commit("updateRequestProgress", { code: requestCode, progress: 1 });
  store.commit("endRequest", requestCode);
  return modelResultsRet;
}

// Main methods :
async function loadData(selectionIds, selectionIntersection) {
  // Generate an analysis id
  let analysisId = services.uuid();

  // Downloading project meta data, requiered to interprate the tree
  let projectMetadata = await getProjectMetadata({ considerResults: false });

  // Get the data provider info (pull limitations)
  let dataProviderInfo = await getDataProviderLimit();
  projectMetadata["dataProvider"] = dataProviderInfo;

  // Get the samples to pull
  let samplesToPull = await getProjectSamplesIdList(
    projectMetadata,
    analysisId,
    selectionIds,
    selectionIntersection
  );

  // Download and convert the tree
  const { dataArray, sampleIdList } = await downloadSamplesData(
    projectMetadata,
    samplesToPull,
    analysisId
  );

  return {
    metaData: projectMetadata,
    array: [projectMetadata.labels, ...dataArray],
    sampleIdList,
  };
}
/**
 * @param {Array<string>} modelIds
 * @param {boolean} common get the common sample or not
 * @param {string?} selectionId Get model on the selection if provided
 */
async function loadDataAndModelResults(
  selectionIds,
  selectionIntersection,
  modelIds,
  commonResults
) {
  // Generate an analysis id
  let analysisId = services.uuid();

  // Downloading project meta data, requiered to interprate the tree
  let projectMetadata = await getProjectMetadata({ considerResults: true });

  // Get the data provider info (pull limitations)
  let dataProviderInfo = await getDataProviderLimit();
  projectMetadata["dataProvider"] = dataProviderInfo;

  // Get the samples ID to pull
  let samplesToPull = await getProjectSamplesIdList(
    projectMetadata,
    analysisId,
    selectionIds,
    selectionIntersection,
    modelIds,
    commonResults
  );

  // Download and convert the tree
  const { dataArray, sampleIdList } = await downloadSamplesData(
    projectMetadata,
    samplesToPull,
    analysisId
  );

  // =========== Then add the model results
  // Create a request
  let requestCode = startProgressRequest("Loading the model results");

  try {
    let dataArrayFull = [];
    let samplesToPullFull = [];

    for (let i = 0; i < modelIds.length; i++) {
      const modelId = modelIds[i];

      let modelResults = await downloadResults(projectMetadata, modelId, samplesToPull);

      // We now have a sample array and a list of results
      // We need to duplicate each one of the samples for each one of the sample results
      // ie : if a sample got evaluated on 3 models, the sample must be 3 time sample, each one
      // with his own model results

      const dataAndResultsArray = [];
      const modelsSamplesToPull = [];

      sampleIdList.forEach((sampleId, i) => {
        if (sampleId in modelResults) {
          dataAndResultsArray.push([...dataArray[i], modelId, ...modelResults[sampleId]]);
          modelsSamplesToPull.push(sampleId);
        }
      });

      dataArrayFull = [...dataArrayFull, ...dataAndResultsArray];
      samplesToPullFull = [...samplesToPullFull, ...modelsSamplesToPull];
      store.commit("updateRequestProgress", {
        code: requestCode,
        progress: (i + 1) / modelIds.length,
      });
    }
    store.commit("endRequest", requestCode);

    return {
      metaData: projectMetadata,
      array: [projectMetadata.labels, ...dataArrayFull],
      sampleIdList: samplesToPullFull,
    };
  } catch (error) {
    store.commit("endRequest", requestCode);
    throw error;
  }
}

// array to DebiAI analysis main data object
const min = (arr) => {
  let min = Infinity;
  for (let i = 0; i < arr.length; i++) if (arr[i] < min) min = arr[i];
  return min;
};
const max = (arr) => {
  let max = -Infinity;
  for (let i = 0; i < arr.length; i++) if (arr[i] > max) max = arr[i];
  return max;
};

async function arrayToJson(array, metaData) {
  let requestCode = startProgressRequest("Preparing the analysis");
  console.time("Preparing the analysis");

  let ret = {
    labels: [],
    nbLines: 0,
    nbColumns: 0,
    columns: new Array(metaData.labels.length).fill([]),
    categories: [...CATEGORIES.map((c) => c.singleName), "results"],
  };

  ret.labels = array[0];
  ret.nbLines = array.length - 1;
  ret.nbColumns = array[0].length;

  // deal with duplicate labels
  for (const [i, label] of ret.labels.entries()) {
    let dupInd = ret.labels.findIndex((l2, j) => label == l2 && i != j);
    let nbDup = 2;
    while (dupInd >= 0) {
      ret.labels[dupInd] = ret.labels[dupInd] + "_" + nbDup;
      dupInd = ret.labels.findIndex((l2, j) => label == l2 && i != j);
    }
  }

  for await (const [i, label] of ret.labels.entries()) {
    // Creating the column object
    let col = {
      label,
      index: i,
      values: [],
      type: null,
      typeText: "",
      category: "other",
    };

    // Filling the column
    for (let j = 1; j < ret.nbLines + 1; j++) col.values.push(array[j][i]);

    col.uniques = [...new Set(col.values)];
    col.nbOccu = col.uniques.length;

    // Cheking if the column is type text, number or got undefined values
    if (col.uniques.findIndex((v) => v === undefined || v === "" || v === null) >= 0) {
      // undefined Values
      col.type = undefined;
      col.typeText = "undefined";
      col.undefinedIndexs = col.values
        .map((v, i) => (v == undefined || v == "" || v == null ? i : -1))
        .filter((v) => v >= 0);
      console.warn("Undefined values : " + label);
      console.warn(col.uniques);
      console.warn(col.values);
    } else if (metaData.type[i] == "text" || col.uniques.find((v) => isNaN(v))) {
      // String Values
      col.type = String;
      col.typeText = "Class";
      let tmpUniqMap = {};
      col.valuesIndexUniques = col.uniques.map((str, i) => {
        tmpUniqMap[str] = i;
        return i;
      });

      col.valuesIndex = col.values.map((str) => tmpUniqMap[str]);
      col.min = min(col.valuesIndexUniques);
      col.max = max(col.valuesIndexUniques);
    } else {
      // Default Type
      col.type = Number;
      col.typeText = "Num";
      col.values = col.values.map((v) => +v);
      col.uniques = col.uniques.map((v) => +v);
      col.nbOccu = col.uniques.length;
      col.min = min(col.uniques);
      col.max = max(col.uniques);
      col.average = col.values.reduce((a, b) => a + b, 0) / ret.nbLines || 0;
      if (col.uniques.length < 100) col.uniques.sort((a, b) => a - b);
    }

    // deal with provided metaData
    col.category = metaData.categories[i];

    ret.columns[i] = col;

    updateRequestProgress(requestCode, (i + 1) / ret.nbColumns);
    console.timeLog(
      "Preparing the analysis",
      "Column " + label + " " + (i + 1) + " / " + ret.nbColumns
    );
  }

  endRequest(requestCode);
  console.timeEnd("Preparing the analysis");

  return ret;
}

async function loadProjectSamples({
  selectionIds = null,
  selectionIntersection = false,
  modelIds = null,
  commomModelResults = false,
}) {
  let requestCode = startRequest("The analysis is starting");

  // Load the project tree as an array
  let data, projectSamples;
  try {
    if (modelIds && modelIds.length > 0) {
      projectSamples = await loadDataAndModelResults(
        selectionIds,
        selectionIntersection,
        modelIds,
        commomModelResults
      );
    } else {
      projectSamples = await loadData(selectionIds, selectionIntersection);
    }
    let metaData = projectSamples.metaData;
    let array = projectSamples.array;
    let sampleIdList = projectSamples.sampleIdList;

    // Convert the the array in an column lists ready for analysing
    data = await arrayToJson(array, metaData);
    data.sampleIdList = sampleIdList;
  } finally {
    endRequest(requestCode);
  }

  return data;
}

export default { loadProjectSamples };
