import store from "../store";
import cacheService from "./cacheService";
import services from "./services";
import axios from "axios";
import { parquetRead } from "hyparquet";

const backendDialog = require("./backendDialog");
const samplesIdListRequester = require("./statistics/samplesIdListRequester").default;

let currentAnalysis = {};

function resetCurrentAnalysis() {
  currentAnalysis = {
    id: null,
    canceled: false,
    requestCodes: {
      analysisStarting: null,
      projectSamplesIdList: null,
      modelResults: null,
    },
  };
}

//  Need to take position on which columns stay available or not
const CATEGORIES = [
  { blName: "inputs", singleName: "input" },
  { blName: "groundTruth", singleName: "ground truth" },
  { blName: "contexts", singleName: "context" },
  { blName: "others", singleName: "other" },
  { blName: "features", singleName: "features" },
  { blName: "annotations", singleName: "annotations" },
];

async function getDataProviderLimit() {
  try {
    const dataProviderInfo = store.state.ProjectPage.dataProviderInfo;
    const dataProviderLimit = {
      maxIdLimit: dataProviderInfo?.maxSampleIdByRequest || 10000,
      maxDataLimit: dataProviderInfo?.maxSampleDataByRequest || 2000,
      maxResultLimit: dataProviderInfo?.maxResultByRequest || 5000,
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

async function getDataProviderBucketPath() {
  // TODO Tom: Complete
  return {
    project_path: "http://localhost:8000/data/parquet/10000/download", // Local path or S3 to read project parquets
    selection_path: null, // Local path or S3 to read selection parquet ($path/$selection_id)
    models_path: null, // Local path or S3 to read model parquet ($path/$model_id)
    id_column_label: "id", // Column label for the data ID
  };
}

// Get project samples Id list functions
async function getProjectSamplesIdList(
  projectMetadata,
  selectionIds = [],
  selectionIntersection = false,
  modelIds = [],
  commonResults = false
) {
  if (currentAnalysis.canceled) return;

  // Returns the list of samples id for a project
  // this need to be done in a sequential way to avoid
  // too big requests
  const acceptedSize = projectMetadata.dataProvider.maxIdLimit;
  const projectNbSamples = projectMetadata.nbSamples;

  // If we have no samples, we don't search for samples ID
  if (projectNbSamples === 0) return [];

  // If the project is small, we gather all ID at once
  // If we are analyzing selections or models, we don't split the request (not implemented yet)
  if (
    (projectNbSamples !== null && projectNbSamples <= acceptedSize) ||
    selectionIds.length > 0 ||
    modelIds.length > 0
  ) {
    // At the moment, we gather all ID when we deal with selections and models
    // If we have a small project, we gather all ID
    // Also, if we don't have the number of samples, we gather all ID
    const res = await samplesIdListRequester.getIdList({
      analysis: { id: currentAnalysis.id, start: true, end: true },
      selectionIds,
      selectionIntersection,
      modelIds,
      commonResults,
    });
    return res.samples;
  } else if (projectNbSamples === null) {
    // If we don't know the number of samples, we gather all ID by chunks
    // We stop when we get less samples than the chunk size
    let samplesIdList = [];
    let i = 0;
    console.warn("Project samples number is not known, loading samples ID list by chunks");
    let requestCode = services.startRequest("Step 1/2: Loading the data ID list");
    currentAnalysis.requestCodes.projectSamplesIdList = requestCode;

    try {
      console.time("getProjectSamplesIdList");
      while (true) {
        const from = i * acceptedSize;
        const to = (i + 1) * acceptedSize - 1;

        // Deal with the analysis info
        const analysis = { id: currentAnalysis.id, start: false, end: false };
        if (i === 0) analysis.start = true;

        // Send the request
        const res = await samplesIdListRequester.getIdList({ analysis, from, to });

        if (res.samples.length === 0) {
          console.log("No samples found while loading project samples ID list");
          break;
        }

        // Add the samples to the list
        samplesIdList = samplesIdList.concat(res.samples);
        console.log("Current samples ID list length: ", samplesIdList.length);

        // If we get less samples than the chunk size, we stop
        if (res.samples.length < acceptedSize) {
          console.log(
            "Last samples found while loading project samples ID list",
            res.samples.length,
            "<",
            acceptedSize
          );
          break;
        }

        // Check if the request has been canceled
        if (currentAnalysis.canceled) break;

        // Update a new progress bar counter
        services.updateRequestQuantity(requestCode, samplesIdList.length);

        i++;
      }
      console.timeEnd("getProjectSamplesIdList");
      services.endRequest(requestCode);
    } catch (error) {
      console.timeEnd("getProjectSamplesIdList");
      services.endRequest(requestCode);
      throw error;
    }

    console.log("Request done, ", samplesIdList.length, " samples found");
    return samplesIdList;
  } else {
    // We gather all the project samples ID
    // We need to split it in multiple requests
    let nbRequest = Math.ceil(projectNbSamples / acceptedSize);
    let samplesIdList = [];

    console.log("Splitting ID list request in ", nbRequest, " requests");
    let requestCode = services.startProgressRequest("Step 1/2: Loading the data ID list");
    currentAnalysis.requestCodes.projectSamplesIdList = requestCode;

    try {
      console.time("getProjectSamplesIdList");
      for (let i = 0; i < nbRequest; i++) {
        const from = i * acceptedSize;
        const to = Math.min((i + 1) * acceptedSize, projectNbSamples) - 1;

        // Deal with the analysis info
        const analysis = { id: currentAnalysis.id, start: false, end: false };
        if (i === 0) analysis.start = true;
        if (i === nbRequest - 1) analysis.end = true;

        // Send the request
        const idList = await backendDialog.default.getProjectIdList(analysis, from, to);

        if (idList.length === 0)
          throw "No samples found while loading project samples ID list from " + from + " to " + to;
        if (idList.length !== to - from + 1)
          throw (
            "Wrong number of samples while loading project samples ID list from " +
            from +
            " to " +
            to +
            ", got " +
            idList.length +
            " instead of " +
            (to - from + 1)
          );

        // Add the samples to the list
        samplesIdList = samplesIdList.concat(idList);
        services.updateRequestProgress(requestCode, (i + 1) / nbRequest);

        // Check if the request has been canceled
        if (currentAnalysis.canceled) break;
      }
      console.timeEnd("getProjectSamplesIdList");
      services.endRequest(requestCode);
    } catch (error) {
      console.timeEnd("getProjectSamplesIdList");
      services.endRequest(requestCode);
      throw error;
    }

    console.log(
      "Request done, ",
      samplesIdList.length,
      " samples found over ",
      projectNbSamples,
      " samples requested"
    );

    // Check Uniqueness of samples ID
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
    timestamp: projectInfo.updateDate,
    nbSamples: projectInfo.nbSamples,
    labels: ["Data ID"],
    categories: ["other"],
    type: ["auto"],
    groups: [null],
  };

  projectInfo.columns.forEach((column) => {
    metaData.labels.push(column.name);
    metaData.categories.push(column.category);
    metaData.type.push(column.type);
    metaData.groups.push(column.group);
  });

  // In case we are loading the results
  if (considerResults && "resultStructure" in projectInfo) {
    // push model Name
    metaData.labels.push("model");
    metaData.categories.push("results");
    metaData.type.push("auto");
    metaData.groups.push(null);

    // push model expected results
    projectInfo.resultStructure.forEach((resultColumn) => {
      metaData.labels.push(resultColumn.name);
      metaData.categories.push("results");
      metaData.type.push(resultColumn.type);
      metaData.groups.push(resultColumn.group);
    });
  }

  // Get information about cache
  const enableCache = store.state.ProjectPage.enableCache;
  // Remove the timestamp is enough to disable the cache
  if (!enableCache) metaData.timestamp = null;

  return metaData;
}
async function downloadSamplesData(projectMetadata, sampleIds) {
  if (currentAnalysis.canceled) return;

  const CHUNK_SIZE = projectMetadata.dataProvider.maxDataLimit;
  let pulledData = 0;
  let nbSamples = sampleIds.length;

  // Create a request
  let requestCode = services.startProgressRequest("Loading the project data");
  console.time("Loading the project data");
  // Pull the tree
  let retArray = [];
  let retDataIdList = [];

  try {
    while (pulledData < nbSamples) {
      let samplesToPull = sampleIds.slice(pulledData, pulledData + CHUNK_SIZE);

      // First, pull the samples from the browser memory
      if (projectMetadata.timestamp) {
        let cachedSamples = await cacheService.getSamplesByIds(
          projectMetadata.timestamp,
          samplesToPull
        );
        retArray = [...retArray, ...Object.values(cachedSamples)];
        retDataIdList = [...retDataIdList, ...Object.keys(cachedSamples)];

        // We ignore the samples that are already in the cache
        samplesToPull = samplesToPull.filter((sampleId) => !(sampleId in cachedSamples));
      }

      if (samplesToPull.length) {
        // Then download the missing samples
        console.log(samplesToPull.length + " samples to download");

        // Deal with the analysis info
        const analysis = { id: currentAnalysis.id, start: false, end: false };
        if (pulledData === 0) analysis.start = true;
        if (pulledData + samplesToPull.length === nbSamples) analysis.end = true;

        // Send the request
        const downloadedSamples = await backendDialog.default.getBlocksFromSampleIds(
          samplesToPull,
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
        retDataIdList = [...retDataIdList, ...Object.keys(map)];

        // Store the samples in the cache
        if (projectMetadata.timestamp)
          // Removing the await here does not change the execution time
          cacheService.saveSamples(projectMetadata.timestamp, map);
      }

      // Update the progress
      pulledData += CHUNK_SIZE;
      services.updateRequestProgress(requestCode, pulledData / nbSamples);

      // Check if the request has been canceled
      if (currentAnalysis.canceled) break;
    }
  } finally {
    services.endRequest(requestCode);
    console.timeEnd("Loading the project data");
  }
  return { dataArray: retArray, sampleIdList: retDataIdList };
}

// Model results
async function downloadResults(projectMetadata, modelId, sampleIds) {
  const CHUNK_SIZE = projectMetadata.dataProvider.maxResultLimit;
  let pulledData = 0;

  // Create a request
  let requestCode = services.startProgressRequest(modelId);
  currentAnalysis.requestCodes.modelResults = requestCode;

  let modelResultsRet = {};

  try {
    // Not done because more time is spent storing the cache : First, pull the tree from the browser memory
    // let cachedResults = await cacheService.getModelResultsByIds(timestamp, modelId, sampleIds)
    // let resultsToDownload = sampleIds.filter(sampleId => !(sampleId in cachedResults))

    // add the cached results to our results without empty one
    // for (const sampleId in cachedResults)
    //   if (cachedResults[sampleId] !== null) modelResultsRet[sampleId] = cachedResults[sampleId]

    // Pull the tree
    // let nbSamples = resultsToDownload.length
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
      services.updateRequestProgress(requestCode, pulledData / nbSamples);

      // Check if the request has been canceled
      if (currentAnalysis.canceled) break;
    }
    services.updateRequestProgress(requestCode, 1);
  } finally {
    services.endRequest(requestCode);
  }

  return modelResultsRet;
}

// Main methods :
async function loadData(selectionIds, selectionIntersection) {
  console.log("loadData", selectionIds, selectionIntersection);

  const parquetPaths = await getDataProviderBucketPath();
  if (parquetPaths.project_path)
    return await loadDataParquet(
      parquetPaths.project_path,
      parquetPaths.id_column_label,
      selectionIds,
      selectionIntersection
    );
  else return await loadDataJson(selectionIds, selectionIntersection);
}
async function loadDataJson(selectionIds, selectionIntersection) {
  // Downloading project meta data, required to interpret the tree
  let projectMetadata = await getProjectMetadata({ considerResults: false });

  // Get the data provider info (pull limitations)
  let dataProviderInfo = await getDataProviderLimit();
  projectMetadata["dataProvider"] = dataProviderInfo;

  // Get the samples to pull
  let samplesToPull = await getProjectSamplesIdList(
    projectMetadata,
    selectionIds,
    selectionIntersection
  );

  if (currentAnalysis.canceled) return;

  // Download and convert the tree
  const { dataArray, sampleIdList } = await downloadSamplesData(projectMetadata, samplesToPull);

  return {
    metaData: projectMetadata,
    array: [projectMetadata.labels, ...dataArray],
    sampleIdList,
  };
}
async function loadDataParquet(
  parquetDataPath,
  parquetIdColumnLabel,
  selectionIds,
  selectionIntersection
) {
  // First, get parquet file info
  const fileResponse = await axios.get(parquetDataPath, { responseType: "arraybuffer" });

  // Read parquet file
  let rows = [];
  let columns = [];
  await parquetRead({
    file: fileResponse.data,
    onChunk: (chunk) => {
      columns.push(chunk.columnName);
    },
    onComplete: (data) => {
      // Convert BigInt values to Number (int)
      rows = data.map((row) =>
        row.map((value) => (typeof value === "bigint" ? Number(value) : value))
      );
    },
  });

  // Check if we have an ID column
  if (!columns.includes(parquetIdColumnLabel))
    throw new Error("ID column " + parquetIdColumnLabel + " not found in parquet file");

  // Get the data id list
  const dataIdListColumnIndex = columns.indexOf(parquetIdColumnLabel);
  const sampleIdList = rows.map((row) => row[dataIdListColumnIndex]);

  // Add column labels as the first row
  const arrayWithLabels = [columns, ...rows];

  // Get the data provider info (pull limitations)
  let dataProviderInfo = await getDataProviderLimit();

  // Build metadata object compatible with the JSON loader format
  const metaData = {
    timestamp: Date.now(), // Current timestamp for caching purposes
    nbSamples: rows.length,
    labels: columns,
    categories: columns.map(() => "other"), // Default to "other" category for all columns
    type: columns.map(() => "auto"), // Default to "auto" type for all columns
    groups: columns.map(() => null), // Default to null group for all columns
    dataProvider: dataProviderInfo,
  };

  return {
    metaData,
    array: arrayWithLabels,
    sampleIdList,
  };
}
async function loadDataAndModelResults(
  selectionIds,
  selectionIntersection,
  modelIds,
  commonResults
) {
  // Downloading project meta data, required to interpret the tree
  let projectMetadata = await getProjectMetadata({ considerResults: true });

  // Get the data provider info (pull limitations)
  let dataProviderInfo = await getDataProviderLimit();
  projectMetadata["dataProvider"] = dataProviderInfo;

  // Get the samples ID to pull
  let samplesToPull = await getProjectSamplesIdList(
    projectMetadata,
    selectionIds,
    selectionIntersection,
    modelIds,
    commonResults
  );

  // Download and convert the tree
  const { dataArray, sampleIdList } = await downloadSamplesData(projectMetadata, samplesToPull);

  // =========== Then add the model results
  // Create a request
  let requestCode = services.startProgressRequest("Loading the model results");

  try {
    let dataArrayFull = [];
    let samplesToPullFull = [];

    for (let i = 0; i < modelIds.length; i++) {
      if (currentAnalysis.canceled) break;

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
      services.updateRequestProgress(requestCode, (i + 1) / modelIds.length);
    }

    return {
      metaData: projectMetadata,
      array: [projectMetadata.labels, ...dataArrayFull],
      sampleIdList: samplesToPullFull,
    };
  } catch (error) {
    console.error(error);
    throw error;
  } finally {
    services.endRequest(requestCode);
  }
}

// Array to DebiAI analysis main data object
async function arrayToJson(array, metaData) {
  let requestCode = services.startProgressRequest("Preparing the analysis");
  console.time("Preparing the analysis");

  let ret = {
    labels: [],
    nbLines: 0,
    nbColumns: 0,
    columns: new Array(metaData.labels.length).fill(null),
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
    const values = [];
    for (let j = 1; j < ret.nbLines + 1; j++) values.push(array[j][i]);
    const category = metaData.categories[i];
    const type = metaData.type[i];
    const group = metaData.groups[i];

    ret.columns[i] = {
      index: i,
      label,
      values,
      category,
      type,
      group,
    };

    services.updateRequestProgress(requestCode, (i + 1) / ret.nbColumns);
    console.timeLog(
      "Preparing the analysis",
      "Column " + label + " " + (i + 1) + " / " + ret.nbColumns
    );
  }

  services.endRequest(requestCode);
  console.timeEnd("Preparing the analysis");

  return ret;
}

async function loadProjectSamples({
  selectionIds = null,
  selectionIntersection = false,
  modelIds = null,
  commonModelResults = false,
}) {
  // Check if the analysis is already running
  if (isAnalysisLoading()) throw new Error("Analysis already running");

  // Setups the analysis
  resetCurrentAnalysis();
  let requestCode = services.startRequest("The analysis is starting", cancelCallback);
  currentAnalysis.requestCodes.analysisStarting = requestCode;
  currentAnalysis.id = services.uuid();

  // Load the project tree as an array
  let data, projectSamples;
  try {
    if (modelIds && modelIds.length > 0) {
      projectSamples = await loadDataAndModelResults(
        selectionIds,
        selectionIntersection,
        modelIds,
        commonModelResults
      );
    } else {
      projectSamples = await loadData(selectionIds, selectionIntersection);
    }

    if (!currentAnalysis.canceled) {
      let metaData = projectSamples.metaData;
      let array = projectSamples.array;
      let sampleIdList = projectSamples.sampleIdList;

      // Convert the the array in an column lists ready for analyzing
      data = await arrayToJson(array, metaData);
      data.sampleIdList = sampleIdList;
    }
  } catch (e) {
    console.error(e);
    resetCurrentAnalysis();
    throw e;
  } finally {
    services.endRequest(requestCode);
  }

  if (currentAnalysis.canceled) {
    // The analysis was canceled, we return null
    resetCurrentAnalysis();
    return;
  }

  // Got the samples, we return the data
  resetCurrentAnalysis();
  return data;
}

function cancelCallback() {
  console.log("cancelCallback");
  currentAnalysis.canceled = true;

  // Stop all the requests
  services.endRequest(currentAnalysis.requestCodes.analysisStarting);
  services.endRequest(currentAnalysis.requestCodes.projectSamplesIdList);
  services.endRequest(currentAnalysis.requestCodes.modelResults);
}
function isAnalysisLoading() {
  if (currentAnalysis.id == null || currentAnalysis.canceled) return false;
  return true;
}

export default {
  loadProjectSamples,
  cancelAnalysis: cancelCallback,
  isAnalysisLoading,
};
